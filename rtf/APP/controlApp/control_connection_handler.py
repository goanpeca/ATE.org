from common.connection_handler import ConnectionHandler
import asyncio
import os
import sys
from transitions import Machine
import json
from common.logger import Logger

DEAD = 0
ALIVE = 1
SOFTWARE_VERSION = 1
INTERFACE_VERSION = 1


class ControlAppMachine:

    def __init__(self, conhandler):
        self._conhandler = conhandler
        self._task = None

        states = ['idle', 'loading', 'busy', 'error']

        transitions = [
            {'trigger': 'load',            'source': 'idle',        'dest': 'loading',    'before': 'before_load'},
            {'trigger': 'testapp_active',  'source': 'loading',     'dest': 'busy',       'before': 'testapp_before_active'},
            {'trigger': 'testapp_exit',    'source': 'busy',        'dest': 'idle',       'before': 'testapp_before_exit'},
            {'trigger': 'error',           'source': '*',           'dest': 'error',      'before': 'before_error'},
            {'trigger': 'reset',           'source': 'error',       'dest': 'idle',       'before': 'before_reset'},
            {'trigger': 'reset',           'source': 'idle',        'dest': 'idle'},
        ]

        self.machine = Machine(model=self, states=states, transitions=transitions, initial='idle', after_state_change=self.publish_current_state)

    def publish_current_state(self, whatever=None):
        print('publish_current_state: ', self.state)
        self._conhandler.publish_state(self.state)

    async def _run_testapp_task(self, testapp_params: dict):
        proc = None
        error_info = None
        try:
            # TODO: windows only: we should explicitly load the correct
            #       virtualenv (or the same as ours). also check deamon
            #       flag for process.
            proc = await asyncio.create_subprocess_exec(
                'py', testapp_params['testapp_script_path'],
                '--device_id', self._conhandler.device_id,
                '--site_id', self._conhandler.site_id,
                '--broker_host', self._conhandler.broker_host,
                '--broker_port', str(self._conhandler.broker_port),
                '--parent-pid', str(os.getpid()),  # TODO: this should be configurable in future: it will make the testapp kill itself if this parent process dies
                *testapp_params.get('testapp_script_args', []),
                cwd=testapp_params.get('cwd'))
            self.testapp_active(proc.pid)
            await proc.wait()
            self.testapp_exit(proc.returncode)
            return
        except (Exception, asyncio.CancelledError):
            error_info = str(sys.exc_info())

            # TODO: terminate testapp when control is closed during
            #       test (CancelledError) or any other exception.
            #       Revisit this, it may not be good idea outside of
            #       development (or is it?)
            try:
                if proc is not None and proc.returncode is None:
                    proc.terminate()  # TODO: is kill better for linux? (on windows there is only terminate)
            except Exception:
                pass  # we only cleanup on best effort
        finally:
            self._task = None

        # only transition to error if we are not yet in error (avoid recursion from trigger)
        if self.state != 'error':
            self.error(error_info)

    def before_load(self, testapp_params: dict):
        print('load', str(testapp_params))
        self._task = asyncio.create_task(self._run_testapp_task(testapp_params))

    def testapp_before_active(self, pid):
        print('testapp_active: ', pid)

    def testapp_before_exit(self, returncode):
        print('testapp_exit: ', returncode)

    def before_error(self, info):
        print('error: ', info)

        if self._task is not None:
            self._task.cancel()

    def before_reset(self):
        print('reset')


class ControlConnectionHandler:

    """ handle connection """

    def __init__(self, host, port, site_id, device_id):
        self.broker_host = host
        self.broker_port = port
        self.site_id = site_id
        self.device_id = device_id
        self.log = Logger.get_logger()
        mqtt_client_id = f'controlapp.{device_id}.{site_id}'
        self.mqtt = ConnectionHandler(host, port, mqtt_client_id)
        self.mqtt.init_mqtt_client_callbacks(self._on_connect_handler,
                                             self._on_message_handler,
                                             self._on_disconnect_handler)

        self.commands = {
            "loadTest": self.__load_test_program,
            "reset": self.__reset_after_error,
        }
        self._statemachine = ControlAppMachine(self)

    def start(self):
        self.mqtt.set_last_will(
            self._generate_base_topic_status(),
            self.mqtt.create_message(
                self._generate_status_message(DEAD, 'crash')))
        self.mqtt.start_loop()

    async def stop(self):
        await self.mqtt.stop_loop()

    def publish_state(self, state, statedict=None):
        self.mqtt.publish(self._generate_base_topic_status(),
                          self.mqtt.create_message(
                              self._generate_status_message(ALIVE, state, statedict)),
                          retain=True)

    def __load_test_program(self, cmd_payload: dict):
        testapp_params = cmd_payload["testapp_params"]
        try:
            self._statemachine.load(testapp_params)
        except Exception as e:
            self._statemachine.error(str(e))
        return True

    def __reset_after_error(self, cmd_payload):
        try:
            self._statemachine.reset()
        except Exception as e:
            self._statemachine.error(str(e))
        return True

    def on_cmd_message(self, message):
        try:
            data = json.loads(message.payload.decode('utf-8'))
            assert data['type'] == 'cmd'
            cmd = data['command']
            sites = data['sites']

            if self.site_id not in sites:
                self.log.warning(f'ignoring TestApp cmd for other sites {sites} (current site_id is {self._topic_factory.site_id})')
                return

            to_exec_command = self.commands.get(cmd)
            if to_exec_command is None:
                self.log.warning("received command not found")
                return

            to_exec_command(data)

        except Exception as e:
            self._statemachine.error(str(e))

    def on_status_message(self, message):
        # TODO: handle status messages
        return

    def _on_connect_handler(self, client, userdata, flags, conect_res):
        self.log.info("mqtt connected")

        self.mqtt.subscribe(self._generate_base_topic_cmd())
        self._statemachine.publish_current_state()

    def _on_message_handler(self, client, userdata, message):
        if "status" in message.topic:
            self.on_status_message(message)
        elif "cmd" in message.topic:
            self.on_cmd_message(message)
        else:
            return

    def _on_disconnect_handler(self, client, userdata, distc_res):
        self.log.info("mqtt disconnected (rc: %s)", distc_res)

    def _generate_status_message(self, alive, state, statedict=None):
        message = {
            "type": "status",
            "alive": alive,
            "interface_version": INTERFACE_VERSION,
            "software_version": SOFTWARE_VERSION,
            "state": state,
        }
        if statedict is not None:
            message.update(statedict)
        return message

    def _generate_base_topic_status(self):
        return "ate/" + self.device_id + "/Control/status/site" + self.site_id

    def _generate_base_topic_cmd(self):
        return "ate/" + self.device_id + "/Control/cmd"
