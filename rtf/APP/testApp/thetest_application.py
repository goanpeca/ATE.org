from enum import Enum
import json
import paho.mqtt.client as mqtt
import argparse
import sys
import time
from transitions import Machine
import concurrent.futures
import logging
import os
import threading

FRAMEWORK_VERSION = 1

logger = logging.getLogger(__name__)


# TODO: this is win32 only. implement linux/POSIX variant
# source: https://stackoverflow.com/a/23587108
def start_parent_process_death_watchdog(parent_pid):
    from ctypes import WinDLL
    from ctypes.wintypes import DWORD, BOOL, HANDLE
    # Magic value from http://msdn.microsoft.com/en-us/library/ms684880.aspx
    SYNCHRONIZE = 0x00100000
    kernel32 = WinDLL("kernel32.dll")
    kernel32.OpenProcess.argtypes = (DWORD, BOOL, DWORD)
    kernel32.OpenProcess.restype = HANDLE
    parent_handle = kernel32.OpenProcess(SYNCHRONIZE, False, parent_pid)

    def _threadproc(parent_handle):
        try:
            os.waitpid(parent_handle, 0)
        finally:
            print(f"PARENT PROCESS WATCHDOG TRIGGERED: process with pid {parent_pid} has died. killing this process ({os.getpid()}) as well...",
                  file=sys.stderr, flush=True)
            os._exit(1)

    t = threading.Thread(target=_threadproc,
                         args=(parent_handle,),
                         daemon=True)
    t.start()


class TheTestAppStatusAlive(Enum):
    DEAD = 0      # error/crash
    ALIVE = 1
    SHUTDOWN = 2  # graceful shutdown
    INITFAIL = 3  # init failed


class TheTestAppParameters:
    __slots__ = ["broker_host", "broker_port", "device_id", "site_id"]

    def __init__(self):
        self.broker_host = "10.9.1.6"
        self.broker_port = 1883
        self.device_id = "pebkac_device"
        self.site_id = "0"

    def to_json(self):
        return {key: getattr(self, key, None) for key in self.__slots__}

    def update_from_json(self, json_str: str):
        for key, v in json.loads(json_str).items():
            if key in self.__slots__:
                setattr(self, key, v)

    def update_from_kwargs(self, **kwargs):
        for key, v in kwargs.items():
            if key in self.__slots__ and v is not None:
                setattr(self, key, v)

    def update_from_file(self, filename):
        with open(filename, 'r') as infile:
            self.update_from_json(infile.read())

    def update_from_parsed_argparse_args(self, args):  # args = argparse.ArgumentParser().parse_args()
        self.update_from_kwargs(**vars(args))

    @classmethod
    def add_argparse_arguments(cls, parser: argparse.ArgumentParser):
        for key in cls.__slots__:
            parser.add_argument('--' + key)


class TopicFactory:

    def __init__(self, device_id, site_id):
        self._device_id = device_id
        self._site_id = site_id

    def master_status_topic(self):
        return f'ate/{self._device_id}/Master/status'

    def control_status_topic(self):
        return f'ate/{self._device_id}/ControlApp/status/site{self._site_id}'

    def test_status_topic(self):
        return f'ate/{self._device_id}/TestApp/status/site{self._site_id}'

    def test_cmd_topic(self):
        return f'ate/{self._device_id}/TestApp/cmd'

    def test_result_topic(self):
        return f'ate/{self._device_id}/TestApp/testresult/site{self._site_id}'

    def test_status_payload(self, alive: TheTestAppStatusAlive):
        return {
            "type": "status",
            "alive": alive.value,
            "framework_version": FRAMEWORK_VERSION,
            "test_version": "N/A"
        }

    def test_result_payload(self, ispass: bool, testdata: object):
        return {
            "type": "testresult",
            "pass": 1 if ispass else 0,
            "testdata": testdata  # any json serializable thing for now
        }

    @property
    def site_id(self):
        return self._site_id

    @property
    def mqtt_client_id(self):
        return f'testapp.{self._device_id}.{self._site_id}'


class TheTestAppMachine:

    def __init__(self, mqtt):
        self._mqtt = mqtt

        states = ['starting', 'idle', 'testing', 'selftesting', 'terminated', 'error']

        transitions = [
            {'trigger': 'startup_done',    'source': 'starting',                  'dest': 'idle',             'before': 'on_startup_done'},
            {'trigger': 'cmd_init',        'source': 'idle',                      'dest': 'selftesting',      'before': 'on_cmd_init'},
            {'trigger': 'cmd_next',        'source': 'idle',                      'dest': 'testing',          'before': 'on_cmd_next'},
            {'trigger': 'cmd_terminate',   'source': 'idle',                      'dest': 'terminated',       'before': 'on_cmd_terminate'},
            {'trigger': 'cmd_done',        'source': ['testing', 'selftesting'],  'dest': 'idle',             'before': 'on_cmd_done'},
            {'trigger': 'fail',            'source': '*',                         'dest': 'error',            'before': 'on_fail'},
        ]

        self.machine = Machine(model=self, states=states, transitions=transitions, initial='starting', after_state_change=self.after_state_change)

    def after_state_change(self, whatever=None):
        logger.debug('publish_current_state: %s', self.state)

        if self.is_error() or self.is_terminated():
            dodisconnect = True
            alive = TheTestAppStatusAlive.DEAD
        else:
            dodisconnect = False
            alive = TheTestAppStatusAlive.ALIVE

        msginfo = self._mqtt.publish_status(alive, {'state': self.state})
        msginfo.wait_for_publish()

        # workaround: handle state after publishing status (which is done
        # in after_state_change, so we cannot put this logic into
        # before/after_transition or on_state handler)
        if dodisconnect:
            self._mqtt.disconnect()

    def on_startup_done(self):
        logger.debug('on_startup_done')

    def on_cmd_init(self):
        logger.debug('on_cmd_init')

    def on_cmd_next(self):
        logger.debug('on_cmd_next')

    def on_cmd_terminate(self):
        logger.debug('on_cmd_terminate')

    def on_cmd_done(self):
        logger.debug('on_cmd_done')

    def on_fail(self, info):
        logger.error('on_fail: %s', info)


class TheTestAppMqttClient:
    _client: mqtt.Client
    _topic_factory: TopicFactory

    def __init__(self, broker_host, broker_port, topic_factory: TopicFactory, submit_callback):
        self._topic_factory = topic_factory
        self._client = self._create_mqtt_client(topic_factory)
        self._client.connect_async(broker_host, int(broker_port), 60)
        self._submit_callback = submit_callback

        # mqtt callbacks, excecuted in executor
        self.on_connect = None        # on_connect()        (only called when succcesfully (re-)connected)
        self.on_disconnect = None     # on_disconnect()     (only called after successful disconnect())
        self.on_message = None        # on_message(message: mqtt.MQTTMessageInfo)
        self.on_command = None        # on_command(cmd:string, payload: dict)

    def loop_forever(self):
        self._client.loop_forever()

    def disconnect(self):
        # note: disconnecting with will message (reasoncode=4) is MQTT5 only
        # in MQTT311 disconnect always tells the broker to discard the will message
        self._client.disconnect()

    def publish_status(self, alive: TheTestAppStatusAlive, statedict: dict = None) -> mqtt.MQTTMessageInfo:
        payload = self._topic_factory.test_status_payload(alive)
        if statedict is not None:
            payload.update(statedict)
        return self._client.publish(
            topic=self._topic_factory.test_status_topic(),
            payload=json.dumps(payload),
            qos=2,
            retain=alive != TheTestAppStatusAlive.ALIVE)

    def publish_result(self, ispass: bool, testdata: object) -> mqtt.MQTTMessageInfo:
        return self._client.publish(
            topic=self._topic_factory.test_result_topic(),
            payload=json.dumps(
                self._topic_factory.test_result_payload(ispass, testdata)),
            qos=2,
            retain=False)

    def _create_mqtt_client(self, topic_factory: TopicFactory) -> mqtt.Client:
        mqttc = mqtt.Client(client_id=topic_factory.mqtt_client_id)

        mqttc.on_connect = self._on_connect_callback
        mqttc.on_disconnect = self._on_disconnect_callback
        mqttc.on_message = self._on_message_callback

        mqttc.message_callback_add(self._topic_factory.test_cmd_topic(),
                                   self._on_message_cmd_callback)

        payload = self._topic_factory.test_status_payload(TheTestAppStatusAlive.DEAD)
        payload.update({'state': 'crash'})
        mqttc.will_set(
            topic=topic_factory.test_status_topic(),
            payload=json.dumps(payload),
            qos=2,
            retain=True)

        return mqttc

    def _on_connect_callback(self, client, userdata, flags, rc):
        if rc != 0:
            logger.error(f"mqtt connect error: {rc}")
            return

        logger.info("mqtt connected")

        self._client.subscribe([
                (self._topic_factory.test_cmd_topic(), 2)
            ])

        self._submit_callback(self.on_connect)

    def _on_disconnect_callback(self, client, userdata, rc):
        if rc != 0:
            logger.error(f"mqtt unexpected disconnect: {rc}")
            return

        logger.info("mqtt disconnected")

        self._submit_callback(self.on_disconnect)

    def _on_message_callback(self, client, userdata, message: mqtt.MQTTMessage):
        logger.info(f'mqtt message for topic {message.topic}')

        self._submit_callback(self.on_message, message)

    def _on_message_cmd_callback(self, client, userdata, message: mqtt.MQTTMessage):
        logger.info(f'mqtt message for topic {message.topic}')

        # there is no exception handling here, because any exceptions
        # in paho main loop should be handled there
        data = json.loads(message.payload.decode('utf-8'))
        assert data['type'] == 'cmd'
        cmd = data['command']
        sites = data['sites']

        if self._topic_factory.site_id not in sites:
            logger.warning(f'ignoring TestApp cmd for other sites {sites} (current site_id is {self._topic_factory.site_id})')
            return

        self._submit_callback(self.on_command, cmd, data)


class TheTestAppApplication:
    _statemachine: TheTestAppMachine
    _mqtt: TheTestAppMqttClient

    def __init__(self, params: TheTestAppParameters = None):
        self.params = params if params is not None else TheTestAppParameters()
        self._statemachine = None
        self._mqtt = None
        self._disconnected = False

    @staticmethod
    def init_from_command_line(argv):
        parser = argparse.ArgumentParser(prog=argv[0])

        TheTestAppParameters.add_argparse_arguments(parser)
        parser.add_argument('config_file', metavar='config-file', nargs='?')
        parser.add_argument("-v", "--verbose",
                            help="increase output verbosity",
                            action="store_true")
        parser.add_argument('--parent-pid')
        args = parser.parse_args(argv[1:])

        if args.verbose:
            logger.addHandler(logging.StreamHandler())
            logger.setLevel(logging.DEBUG)

        # kill this process when the parent dies
        # this is mostly a temporary solution to get rid of
        # zombie processes when the control app dies
        if args.parent_pid is not None:
            logger.warning('PARENT PROCESS WATCHDOG enabled for pid %s',
                           args.parent_pid)
            start_parent_process_death_watchdog(int(args.parent_pid))

        params = TheTestAppParameters()
        # note: values specified on command line always override values loaded
        #       from config file, no matter where the config_file option is
        if args.config_file is not None:
            params.update_from_file(args.config_file)


        params.update_from_parsed_argparse_args(args)

        return params

    @classmethod
    def run_from_command_line(cls, argv):
        params = cls.init_from_command_line(argv)
        testApp = TheTestAppApplication(params)
        testApp.run()

    def run(self):
        topic_factory = TopicFactory(self.params.device_id,
                                     self.params.site_id)
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

        def submit_callback(cb, *args, **kwargs):
            # ignore unbound callbacks
            if cb is None:
                return

            # handle exceptions in all callbacks
            def wrapped_callback():
                try:
                    cb(*args, **kwargs)
                except Exception as e:
                    if self._statemachine is not None:
                        self._statemachine.fail(str(e))
                    else:
                        raise

            # this is called in any thread, not necessarily in the executor
            def handle_uncaught_exceptions_from_executor(f):
                try:
                    f.result()
                except Exception:
                    logger.exception("executor exception")
                    # TODO: we probably don't want to keep running if any
                    #       exception escapesed. using os._exit may not be
                    #       the best way to do this (because no cleanup/io
                    #       flushing at all)
                    os._exit(1)

            f = executor.submit(wrapped_callback)
            f.add_done_callback(handle_uncaught_exceptions_from_executor)

        mqtt = TheTestAppMqttClient(self.params.broker_host,
                                    self.params.broker_port,
                                    topic_factory,
                                    submit_callback)
        mqtt.on_connect = self._on_connect
        mqtt.on_disconnect = self._on_disconnect
        mqtt.on_command = self._on_command

        self._mqtt = mqtt
        self._statemachine = TheTestAppMachine(mqtt)

        try:
            self._mqtt.loop_forever()
        except KeyboardInterrupt:
            pass
        executor.shutdown(wait=True)

    def _on_connect(self):
        # transition to idle state on first connect
        # TODO: subsequent connects are currently not really handled here and
        #       and unexpected disconnects should probably be an error (?)
        if self._statemachine.is_starting():
            self._statemachine.startup_done()
        else:
            # TODO: else is here to avoid publishing the initial idle state
            #       twice (which howver should not be a problem eventually
            #       after fixing problems in subsribers)
            self._mqtt.publish_status(TheTestAppStatusAlive.ALIVE, {'state': self._statemachine.state})

    def _on_disconnect(self):
        self._disconnected = True

    def _on_command(self, cmd, payload):
        self._execute_command(cmd, payload)

    def _execute_command(self, cmd: str, payload: dict):
        if cmd == 'init':
            self._statemachine.cmd_init()
            self._execute_cmd_init(payload.get('mock_result', True),
                                   payload.get('mock_duration_secs', 1.5))
            self._statemachine.cmd_done()
        elif cmd == 'next':
            self._statemachine.cmd_next()
            self._execute_cmd_next(payload.get('mock_result', True),
                                   payload.get('mock_duration_secs', 2.5))
            self._statemachine.cmd_done()
        elif cmd == 'terminate':
            self._statemachine.cmd_terminate()
            self._execute_cmd_terminate()
        else:
            raise Exception(f'invalid command: "{cmd}"')

    def _execute_cmd_init(self, mock_result: bool, mock_duration_secs: int):
        logger.debug('COMMAND: init')

        logger.info('running self test...')
        time.sleep(mock_duration_secs)
        selftest_result = mock_result
        logger.info(f'self test completed: {selftest_result}')

        # TODO: how to report positive init command results? we could also write the testresult
        # self.publish_result(selftest_result, "<insert init result data here>")
        # note that currently once "init" failed the status will not be restored to ALIVE
        if not selftest_result:
            self._mqtt.publish_status(TheTestAppStatusAlive.INITFAIL)

    def _execute_cmd_next(self, mock_result: bool, mock_duration_secs: int):
        logger.debug('COMMAND: next')

        logger.info('executing next test...')
        time.sleep(mock_duration_secs)
        test_result = mock_result
        logger.info(f'test completed: {test_result}')

        self._mqtt.publish_result(test_result, "<insert STDF data here>")

    def _execute_cmd_terminate(self):
        logger.debug('COMMAND: terminate')

        # TODO: code commented: this is currently done in state matching
        # logger.info('publishing shutdown status...')
        # msginfo = self._mqtt.publish_status(TheTestAppStatusAlive.SHUTDOWN)
        # msginfo.wait_for_publish()
        # logger.info('shutdown status published!')
        # logger.info('disconnecting and shutting down...')
        # self._mqtt.disconnect()  # loop_forever() will return after this call


def main():
    return TheTestAppApplication.run_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
