from aiohttp import web, WSMsgType, WSCloseCode
import asyncio
import json
import time
import os
import weakref

import aiomqtt
from paho.mqtt.client import MQTTMessage
from common.logger import Logger

# url to the compiled angular project containing the index.html
# file and the javascript files
static_file_url = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               '../../UI/angular/mini-sct-gui/dist/mini-sct-gui')


class MqttWsProxy:
    def __init__(self, ws, broker_host, broker_port):
        self._ws = ws
        self._broker_host = broker_host
        self._broker_port = broker_port
        self._subs = []
        self._client = None
        self._task = None
        self._log = Logger.get_logger()

    def start_task(self):
        if self._task is not None:
            raise RuntimeError('task already started')
        self._task = asyncio.create_task(self._run_task())

    async def stop_task(self):
        if self._task is not None:
            self._task.cancel()
            await self._task

    def sub(self, topic):
        self._subs.append(topic)
        if self._client is not None:
            self._client.subscribe(topic)

    def pub(self, topic, payload, qos=0, retain=False):
        if self._client is not None:
            self._client.publish(
                topic, payload=payload, qos=qos, retain=retain)
        else:
            self._log.warning('MqttWsProxy ignore publish request because not connected')

    def _send_initial_subs(self, c):
        for topic in self._subs:
            c.subscribe(topic)

    def _message_payload_to_json_value(self, payload):
        # only forward payloads that can be encoded as utf-8 without errors
        try:
            if isinstance(payload, bytes):
                return payload.decode('utf-8')
            elif isinstance(payload, str):
                return payload
            raise ValueError(type(payload).__name__)
        except Exception:
            self._log.exception("unexpected mqtt message payload")
        return None

    def _create_onmessage_message_for_ws(self, message: MQTTMessage):
        return {
            'type': 'mqtt.onmessage',
            'payload': {
                'topic': message.topic,
                'payload': self._message_payload_to_json_value(message.payload),
                'qos': message.qos,
                'retain': message.retain,
            }
        }

    async def _run_task(self):
        def on_connect(client, userdata, flags, rc):
            self._log.debug("MqttWsProxy connected!")
            self._send_initial_subs(client)
            self._client = client

        def on_subscribe(client, userdata, mid, granted_qos):
            self._log.debug("MqttWsProxy subscribed!")

        def on_message(client, userdata, message):
            self._log.debug("MqttWsProxy message: %s %s", message.topic, message.payload)
            ws_msg = self._create_onmessage_message_for_ws(message)
            if ws_msg is not None:
                asyncio.create_task(self._ws.send_json(ws_msg))

        def on_disconnect(client, userdata, rc):
            self._log.debug("MqttWsProxy disconnected!")

        self._log.debug(f"MqttWsProxy task start ({self._broker_host}:{self._broker_port})")

        c = aiomqtt.Client()
        c.on_connect = on_connect
        c.on_subscribe = on_subscribe
        c.on_message = on_message
        c.on_disconnect = on_disconnect
        c.loop_start()
        c.connect_async(self._broker_host, self._broker_port)
        self._client = c

        try:
            # TODO: maybe use an async generator here (yield) like aiohttp does for cleanup context?
            dummy_event_to_sleep_until_task_is_canceled = asyncio.Event()
            await dummy_event_to_sleep_until_task_is_canceled.wait()
        except asyncio.CancelledError:
            pass
        finally:
            self._client = None
            c.disconnect()
            await c.loop_stop()  # TODO: this is apparently interrupted by CancelledError again when a websocket is closed by the browser for some reason, how can we cleanup properly?

        self._log.debug("MqttWsProxy task end")


class WebsocketCommunicationHandler:
    def __init__(self, app):
        self._app = app
        self._websockets = weakref.WeakSet()
        self._log = Logger.get_logger()

    def get_current_master_state(self):
        master_app = self._app['master_app']
        return master_app.state

    def get_broker_from_master_config(self):
        master_app = self._app['master_app']
        return (master_app.configuration.get('broker_host'),
                master_app.configuration.get('broker_port'))

    def get_mqtt_handler(self):
        return self._app['mqtt_handler']

    async def send_message_to_all(self, data):
        for ws in set(self._websockets):
            await ws.send_json(data)

    async def send_status_to_all(self, state):
        status_message = self._create_status_message(state)
        await self.send_message_to_all(status_message)

    async def send_testresults_to_all(self, siteidtoarrayoftestresultsdicts):
        testresults_message = {
            'type': 'testresults',
            'payload': siteidtoarrayoftestresultsdicts,
        }
        await self.send_message_to_all(testresults_message)

    def _create_status_message(self, state):
        return {
            'type': 'status',
            'payload': {
                'device_id': self._app['master_app'].device_id,
                'systemTime': time.strftime("%b %d %Y %H:%M:%S"),
                'sites': self._app['master_app'].configuredSites,
                'state': state,
                'env': self._app['master_app'].env,
                #'handler': self._app['master_app'].connection_handler,
            }
        }

    async def close_all(self):
        for ws in set(self._websockets):
            await ws.close(code=WSCloseCode.GOING_AWAY,
                           message='Server shutdown')

    async def receive(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        # send initial status message
        await ws.send_json(self._create_status_message(
            self.get_current_master_state()))

        self._websockets.add(ws)
        mqttproxy = None

        # handle in-comming messages
        try:
            async for msg in ws:
                if msg.type == WSMsgType.TEXT:
                    response_message = self.handle_client_message(msg.data)
                    if response_message:
                        await ws.send_json(response_message)
                    else:
                        json_data = json.loads(msg.data)

                        is_sub = json_data.get('type') == 'mqtt.subscribe'
                        is_pub = json_data.get('type') == 'mqtt.publish'
                        if is_sub or is_pub:
                            msgpayload = json_data['payload']
                            if mqttproxy is None:
                                mqttproxy = MqttWsProxy(ws, *self.get_broker_from_master_config())
                                mqttproxy.start_task()
                            if is_sub:
                                mqttproxy.sub(topic=msgpayload['topic'])
                            elif is_pub:
                                mqttproxy.pub(topic=msgpayload['topic'],
                                              payload=json.dumps(
                                                  msgpayload['payload']),
                                              qos=msgpayload.get('qos', 0),
                                              retain=msgpayload.get('retain',
                                                                    False))

                    # send something over mqtt
                    mqtt_handler = self.get_mqtt_handler()
                    if mqtt_handler is not None:
                        mqtt_handler.mqtt.publish("TEST/lastwebsocketmsg", msg.data)

                elif msg.type == WSMsgType.ERROR:
                    self._log.error('ws connection closed with exception: %s', ws.exception())
        finally:
            if mqttproxy is not None:
                await mqttproxy.stop_task()
            self._websockets.discard(ws)

        self._log.debug('websocket connection closed.')

    def handle_client_message(self, message_data: str):
        json_data = json.loads(message_data)
        self._log.debug('Server received message %s', json_data)

        if json_data.get('type') == 'cmd':
            self._app["master_app"].dispatch_command(json_data)


async def index_handler(request):
    return web.FileResponse(f'{static_file_url}/index.html')


async def webservice_init(app):
    ws_comm_handler = WebsocketCommunicationHandler(app)
    app.add_routes([web.get('/', index_handler),
                   web.get('/ws', ws_comm_handler.receive)])
    # From the aiohttp documentation it is known to use
    # add_static only when developing things
    # normally static content should be processed by
    # webservers like (nginx or apache)
    # In the case of MiniSCT it is okay to use add_static
    app.router.add_static('/', path=static_file_url, name='static')
    app['ws_comm_handler'] = ws_comm_handler


async def webservice_cleanup(app):
    ws_comm_handler = app['ws_comm_handler']
    if ws_comm_handler is not None:
        await ws_comm_handler.close_all()
        app['ws_comm_handler'] = None


def webservice_setup_app(app):
    app.on_startup.append(webservice_init)
    app.on_cleanup.append(webservice_cleanup)
