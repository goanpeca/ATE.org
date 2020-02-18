""" master App """

# External imports
from aiohttp import web
from transitions import Machine
import argparse
import asyncio
import json
import mimetypes
import sys
import logging
import platform
import os

# Internal imports
from common.logger import Logger
from masterApp.master_connection_handler import MasterConnectionHandler
from masterApp.master_webservice import webservice_setup_app
from masterApp.parameter_parser import parser_factory
from masterApp.sequence_container import SequenceContainer

INTERFACE_VERSION = 1


def assert_valid_system_mimetypes_config():
    """
    Perform sanity check for system/enfironment configuration and return
    result as boolean.

    Background info:

    aiohttp uses mimetypes.guess_type() to guess the content-type to be
    used in the http response headers when serving static files.

    If we serve javascript modules with "text/plain" instead
    of "application/javascript" the browser will not execute the file as
    javascript module and the angular frontend does not load.

    On windows mimetypes.init (called automatically by guess_type if not
    called before) will always read content types from registry in Python
    3.8.1 (e.g. "HKLM\\Software\\Classes\\.js\\Content Type"). The values
    stored there may not be standard because they have been changed on
    certain systems (reasons unknown).

    Apparently it was possible to avoid this in earlier python
    version by explicitly passing empty list to files, e.g.
    mimetypes.init(files=[]). But this does not work anymore in 3.8.1,
    where types from registry will always be loaded.
    """
    js_mime_type = mimetypes.guess_type('file.js')[0]
    if js_mime_type != 'application/javascript':
        print('FATAL ERROR: Invalid system configuration for .js type: '
              + 'expected "application/javascript" but got '
              + f'"{js_mime_type}".'
              + ' Please fix your systems mimetypes configuration.')
        sys.exit(1)

CONTROL_STATE_UNKNOWN = "unknown"
CONTROL_STATE_LOADING = "loading"
CONTROL_STATE_BUSY = "busy"
CONTROL_STATE_IDLE = "idle"
CONTROL_STATE_CRASH = "crash"

TEST_STATE_IDLE = "idle"
TEST_STATE_TESTING = "testing"
TEST_STATE_CRASH = "crash"
TEST_STATE_TERMINATED = "terminated"


class MasterApplication:

    states = [
    'startup',
    'connecting',
    'initialized',
    'loading',
    'ready',
    'testing',
    'finished',
    'unloading',
    'error']

    transitions = [
        {'source': 'startup',       'dest': 'connecting',   'trigger': "startup_done"},
        {'source': 'startup',       'dest': 'error',        'trigger': 'configuration_error'},
        {'source': 'connecting',    'dest': 'initialized',  'trigger': 'all_sites_detected',          'after': "on_allsitesdetected"},
        {'source': 'connecting',    'dest': 'error',        'trigger': 'bad_interface_version'},

        {'source': 'initialized',   'dest': 'loading',      'trigger': 'load_command',                'after': 'on_loadcommand_issued'},
        {'source': 'loading',       'dest': 'ready',        'trigger': 'all_siteloads_complete'},

        {'source': 'ready',         'dest': 'testing',      'trigger': 'next',                      'after': 'on_next_command_issued'},
        {'source': 'testing',       'dest': 'testing',      'trigger': 'testapp_testresult_received', 'after': 'on_site_test_result_received'},
        {'source': 'ready',         'dest': 'unloading',    'trigger': 'unload',                    'after': 'on_unload_command_issued'},
        {'source': 'testing',       'dest': 'ready',        'trigger': 'all_sitetests_complete',      'after': "on_allsitetestscomplete"},
        {'source': 'unloading',     'dest': 'initialized',  'trigger': 'all_siteunloads_complete',    'after': "on_allsiteunloadscomplete"},

        {'source': '*',             'dest': 'error',        'trigger': 'testapp_disconnected',       'after': 'on_disconnect_error'},
        {'source': '*',             'dest': 'error',        'trigger': 'timeout',                   'after': 'on_timeout'},
        {'source': '*',             'dest': 'error',        'trigger': 'on_error',                  'after': 'on_error_occured'}
    ]

    """ MasterApplication """

    def __init__(self, configuration):
        self.fsm = Machine(model = self, states = MasterApplication.states, transitions = MasterApplication.transitions, initial = "startup", after_state_change='publish_state')
        self.configuration = configuration
        self.configuredSites = configuration['sites']
        self.siteStates = [*map(lambda x: (x, CONTROL_STATE_UNKNOWN), self.configuredSites)]
        
        self.receivedSiteTestResults = {}  # key: site_id, value: [testresult topic payload dicts]
        self.device_id = configuration['device_id']
        self.env = None
        self.log = Logger.get_logger()
        self.create_handler( configuration["broker_host"], configuration["broker_port"])
        self.enableTimeouts = configuration.get("enable_timeouts", False)
        self.errorMessage = ""
        self.pendingTransitionsControl = SequenceContainer([CONTROL_STATE_IDLE], self.configuredSites,  lambda: self.all_sites_detected(), lambda site, state: self.on_unexpected_control_state(site, state))
        self.pendingTransisionsTest = SequenceContainer([TEST_STATE_IDLE], self.configuredSites,  lambda: self.all_siteloads_complete(), lambda site, state: self.on_unexpected_control_state(site, state))

        # Sanity check for bad configurations:
        if len(self.configuredSites) == 0:
            self.configuration_error({'reason': 'No sites configured'})
        
        self.timeoutHandle = None
        self.arm_timeout(300, lambda: self.timeout("Not all sites connected."))


    def disarm_timeout(self):
        if self.enableTimeouts:
            if not self.timeoutHandle == None:
                self.timeoutHandle.cancel()
                self.timeoutHandle = None

    def arm_timeout(self, timeout_in_seconds: float, callback: callable):
        if self.enableTimeouts:
            self.disarm_timeout()
            self.timeoutHandle = asyncio.get_event_loop().call_later(timeout_in_seconds, callback)

    def on_timeout(self, message):
        self.errorMessage = message
        self.log.error(message)

    def on_disconnect_error(self, siteId, data):
        self.log.error(f"Entered state error due to disconnect of site {siteId}")

    def on_unexpected_control_state(self, siteId, state):
        self.log.warning(f"Site {siteId} reported state {state}. This state is ignored during startup.")

    def on_error_occured(self, message):
        self.log.error(f"Entered state error, reason: {message}")

    def on_allsitesdetected(self):
        self.disarm_timeout()

    def publish_state(self, siteId = None, paramData = None):
        self.log.info("Master state is " + self.state)
        self.connectionHandler.publish_state(self.state)

    def on_loadcommand_issued(self, paramData: dict):
        jobname = paramData['lot_number']
        jobformat = self.configuration.get('jobformat')
        parser = parser_factory.CreateParser(jobformat)
        source = parser_factory.CreateDataSource(jobname,
                                                 self.configuration,
                                                 parser)

        if self.configuration.get('skip_jobdata_verification', False):
            data = {"DEBUG_OPTION": "no content because skip_jobdata_verification enabled"}
        else:
            param_data = source.retrieve_data()
            if param_data is None:
                # TODO: report error: file could not be loaded (currently only logged)
                return

            if not source.verify_data(param_data):
                # TODO: report error: file was loaded but contains invalid data (currently only logged)
                return
                
            data = source.get_test_information(param_data)

        self.arm_timeout(180, lambda: self.timeout("not all sites loaded the testprogram"))
        self.pendingTransitionsControl = SequenceContainer([CONTROL_STATE_LOADING, CONTROL_STATE_BUSY], self.configuredSites,  lambda: None, lambda site, state: self.on_error(f"Bad statetransition of control {site} during load to {state}"))
        self.pendingTransitionsTest = SequenceContainer([TEST_STATE_IDLE], self.configuredSites,  lambda: self.all_siteloads_complete(), lambda site, state: self.on_error(f"Bad statetransition of testapp {site} during load to {state}"))
        testapp_params = {
            'testapp_script_path': './testApp/thetest_application.py',                  # required
            'testapp_script_args': ['--verbose'],                                       # optional
            'cwd': os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'),     # optional
            'XML': data                                                                 # optional/unused for now
        }
        self.connectionHandler.send_load_test_to_all_sites(testapp_params)

    def on_allsiteloads_complete(self, siteId: str, paramData: dict):
        self.disarm_timeout()

    def on_next_command_issued(self, paramData: dict):
        self.sitesWithCompleteTests = []
        self.receivedSiteTestResults = {}
        self.arm_timeout(30, lambda: self.timeout("not all sites completed the active test"))
        self.pendingTransitionsTest = SequenceContainer( [TEST_STATE_TESTING, TEST_STATE_IDLE], self.configuredSites, lambda: self.all_sitetests_complete(), lambda site, state: self.on_error(f"Bad statetransition of control during test"))
        self.connectionHandler.send_next_to_all_sites()

    def on_unload_command_issued(self, paramData: dict):
        self.arm_timeout(60, lambda: self.timeout("not all sites unloaded the testprogram"))
        self.pendingTransitionsControl = SequenceContainer([CONTROL_STATE_IDLE], self.configuredSites,  lambda: self.all_siteunloads_complete(), lambda site, state: self.on_error(f"Bad statetransition of control {site} during unload to {state}"))
        self.pendingTransitionsTest = SequenceContainer([TEST_STATE_TERMINATED], self.configuredSites,  lambda: None, lambda site, state: None)
        self.connectionHandler.send_terminate_to_all_sites()

    def on_allsiteunloadscomplete(self):
        self.disarm_timeout()

    def on_allsitetestscomplete(self):
        self.disarm_timeout()

    def on_site_test_result_received(self, siteId: str, paramData: dict):
        # simply store testresult so it can be forwarded to UI on the next tick
        self.receivedSiteTestResults.setdefault(siteId, []).append(paramData)

    def create_handler(self, host, port):
        self.connectionHandler = MasterConnectionHandler(host,
                                                          port,
                                                          self.configuredSites,
                                                          self.device_id,
                                                          self)

    def on_control_status_changed(self, siteid: str, status_msg: dict):
        newstatus = status_msg['state']

        if(status_msg['interface_version'] != INTERFACE_VERSION):
            self.bad_interface_version({'reason': f'Bad interfaceversion on site {siteid}'})

        if int(siteid) < len(self.siteStates):
            self.siteStates[int(siteid)] = (int(siteid), newstatus)
        self.pendingTransitionsControl.trigger_transition(siteid, newstatus)

    def on_testapp_status_changed(self, siteid: str, status_msg: dict):
        newstatus = status_msg['state']

        self.pendingTransitionsTest.trigger_transition(siteid, newstatus)

    def on_testapp_testresult_changed(self, siteid: str, status_msg: dict):
        try:
            self.testapp_testresult_received(siteid, status_msg)
        except:
            self.on_error(f"received unexpected testresult from site {siteid}")

    def dispatch_command(self, json_data):
        cmd = json_data.get('command')
        try:
            {
                'load' : lambda paramData: self.load_command(paramData),
                'next' : lambda paramData: self.next(paramData),
                'unload' : lambda paramData: self.unload(paramData)
            }[cmd](json_data)
        except Exception as e:
            self.log.error(f'Failed to execute command {cmd}: {e}')

    async def _mqtt_loop_ctx(self, app):
        self.connectionHandler.start()
        app['mqtt_handler'] = self.connectionHandler  # TODO: temporarily exposed so websocket can publish

        yield

        app['mqtt_handler'] = None
        await self.connectionHandler.stop()

    async def _master_background_task(self, app):

        def is_mqtt_connected():
            return (self.connectionHandler is not None
                    and self.connectionHandler.connected_flag)

        def get_alive_sites():
            if self.connectionHandler is None:
                return
            return filter( (lambda x: x not in [CONTROL_STATE_UNKNOWN, CONTROL_STATE_CRASH]), self.siteStates)

        def all_sites_alive():
            aliveSites = list(get_alive_sites())
            for siteid in self.sites:
                if siteid not in aliveSites:
                    return False

            return True

        def all_sites_loaded():
            return self.state == "initialized"

        try:
            counter = 0
            oldstate = 'unknown'
            while True:
                # push state change via ui/websocket
                oldstate = self.state
                ws_comm_handler = app['ws_comm_handler']
                if ws_comm_handler is not None:
                    await ws_comm_handler.send_status_to_all(self.state)

                if len(self.receivedSiteTestResults) != 0:
                    ws_comm_handler = app['ws_comm_handler']
                    if ws_comm_handler is not None:
                        await ws_comm_handler.send_testresults_to_all(
                            self.receivedSiteTestResults)
                    self.receivedSiteTestResults = {}


                await asyncio.sleep(1)

        except asyncio.CancelledError:
            if self.connectionHandler is not None:
                self.connectionHandler.mqtt.publish('TEST/tick', 'dead')
                # TODO: would we need wait for on_published here to ensure the mqqt loop is not stopped?

    async def _master_background_task_ctx(self, app):
        task = asyncio.create_task(self._master_background_task(app))

        yield

        task.cancel()
        await task

    def run(self):
        app = web.Application()
        app['master_app'] = self

        webservice_setup_app(app)
        app.cleanup_ctx.append(self._mqtt_loop_ctx)
        app.cleanup_ctx.append(self._master_background_task_ctx)        

        host = self.configuration.get('webui_host', "localhost")
        port = self.configuration.get('webui_port', 8081)
        web.run_app(app, host=host, port=port)
