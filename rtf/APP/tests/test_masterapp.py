import pytest
from masterApp import master_application
from masterApp import master_connection_handler

class TestApplication:

    def defaultConfiguration(self):
        return {'broker_host' : '192.168.0.1', 
                'broker_port' : '8991', 
                'sites':        ["0","1"], 
                'device_id':     'd',
                'jobsource':    'static', 
                'jobformat':    'xml.micronas'
                }

    def triggerControlStateChange(self, app: master_application.MasterApplication, site: str, newstate: str):
        app.on_control_status_changed(site, {"state": newstate, "interface_version" : 1})

    def triggerTestStateChange(self, app: master_application.MasterApplication, site: str, newstate: str):
        app.on_testapp_status_changed(site, {"state": newstate, "interface_version" : 1})

    def test_masterapp_correct_number_of_sites_triggers_initialized(self):
        cfg = self.defaultConfiguration()
        app = master_application.MasterApplication(cfg)
        app.startup_done()
        print(app)
        assert(app.state == 'connecting')
        self.triggerControlStateChange(app, "0", "idle")
        assert(app.state == 'connecting')        
        self.triggerControlStateChange(app, "1", "idle")
        assert(app.state == 'initialized')

    def test_masterapp_loadlot_triggers_load_commands(self, mocker):
        mocker.patch.object(master_connection_handler.MasterConnectionHandler, "send_load_test_to_all_sites")
        cfg = self.defaultConfiguration()
        app = master_application.MasterApplication(cfg)
        app.startup_done()
        app.all_sites_detected()
        assert(app.state == 'initialized')
        cmd = {'command' : 'load', 'lot_number': 4711}
        app.load_command(cmd)
        master_connection_handler.MasterConnectionHandler.send_load_test_to_all_sites.assert_called_once()

    def test_masterapp_siteloadcomplete_triggers_ready(self, mocker):
        mocker.patch.object(master_connection_handler.MasterConnectionHandler, "send_load_test_to_all_sites")
        cfg = self.defaultConfiguration()
        app = master_application.MasterApplication(cfg)
        app.startup_done()
        app.all_sites_detected()
        assert(app.state == 'initialized')
        cmd = {'command' : 'load', 'lot_number': 4711}
        app.load_command(cmd)

        self.triggerControlStateChange(app, "1", "loading")
        self.triggerControlStateChange(app, "0", "loading")

        assert(app.state == "loading")
        self.triggerControlStateChange(app, "0", "busy")
        assert(app.state == "loading")
        self.triggerTestStateChange(app, "0", "idle")

        self.triggerControlStateChange(app, "1", "busy")
        assert(app.state == "loading")
        self.triggerTestStateChange(app, "1", "idle")
        assert(app.state == "ready")
        
    def test_masterapp_next_triggers_test(self, mocker):
        cfg = self.defaultConfiguration()
        app = master_application.MasterApplication(cfg)
        app.startup_done()
        app.all_sites_detected()
        cmd = {'command' : 'load', 'lot_number': 4711}
        app.load_command(cmd)
        app.all_siteloads_complete()
        assert(app.state == "ready")
        mocker.patch.object(master_connection_handler.MasterConnectionHandler, "send_next_to_all_sites")
        app.next(None)
        assert(app.state == "testing")
        master_connection_handler.MasterConnectionHandler.send_next_to_all_sites.assert_called_once()
        
    def test_masterapp_testsdone_triggers_ready(self, mocker):
        cfg = self.defaultConfiguration()
        app = master_application.MasterApplication(cfg)
        app.startup_done()
        app.all_sites_detected()
        cmd = {'command' : 'load', 'lot_number': 4711}
        app.load_command(cmd)
        app.all_siteloads_complete()
        app.next(None)
        assert(app.state == "testing")
        self.triggerTestStateChange(app, "0", "testing")
        self.triggerTestStateChange(app, "1", "testing")

        self.triggerTestStateChange(app, "1", "idle")
        assert(app.state == "testing")
        self.triggerTestStateChange(app, "0", "idle")
        assert(app.state == "ready")

    def test_masterapp_crash_triggers_error(self):
        cfg = self.defaultConfiguration()
        app = master_application.MasterApplication(cfg)
        app.startup_done()
        app.all_sites_detected()
        cmd = {'command' : 'load', 'lot_number': 4711}
        app.load_command(cmd)
        app.all_siteloads_complete()
        app.testapp_disconnected(1, None)
        assert(app.state == "error")

    def test_masterapp_no_sites_configured_triggers_error(self):
        cfg = self.defaultConfiguration()
        cfg['sites'] = []
        app = master_application.MasterApplication(cfg)
        assert (app.state == "error")

    def test_masterapp_site_with_bad_interfaceversion_connects_triggers_error(self):
        cfg = self.defaultConfiguration()
        app = master_application.MasterApplication(cfg)
        app.startup_done()
        app.on_control_status_changed("0", {"state": "idle", "interface_version" : 120})
        assert (app.state == "error")

    def test_masterapp_testresult_accepted_if_testing(self):
        cfg = self.defaultConfiguration()
        app = master_application.MasterApplication(cfg)
        app.startup_done()
        app.all_sites_detected()
        cmd = {'command' : 'load', 'lot_number': 4711}
        app.load_command(cmd)
        app.all_siteloads_complete()
        app.next(None)
        assert(app.state == "testing")
        self.triggerTestStateChange(app, "0", "testing")
        self.triggerTestStateChange(app, "1", "testing")

        app.on_testapp_testresult_changed("0", None)
        app.on_testapp_testresult_changed("1", None)
        self.triggerTestStateChange(app, "1", "idle")
        assert(app.state == "testing")
        self.triggerTestStateChange(app, "0", "idle")
        assert(app.state == "ready")

    def test_masterapp_testresult_triggers_error_if_not_sent_during_test(self):
        cfg = self.defaultConfiguration()
        app = master_application.MasterApplication(cfg)
        app.startup_done()
        app.all_sites_detected()
        cmd = {'command' : 'load', 'lot_number': 4711}
        app.load_command(cmd)
        app.all_siteloads_complete()
        app.on_testapp_testresult_changed("0", None)
        assert(app.state == "error")