import pytest
import sys
from masterApp import master_application
from masterApp import master_connection_handler


class TestApplication:

    def default_configuration(self):
        return {'broker_host': '192.168.0.1',
                'broker_port': '8991',
                'sites': ["0", "1"],
                'device_id': 'd',
                'jobsource': 'static',
                'jobformat': 'xml.micronas',
                'enable_timeouts': True,
                'environment': "abs"}

    def trigger_control_state_change(self, app: master_application.MasterApplication, site: str, newstate: str):
        app.on_control_status_changed(site, {"state": newstate, "interface_version": 1})

    def trigger_test_state_change(self, app: master_application.MasterApplication, site: str, newstate: str):
        app.on_testapp_status_changed(site, {"state": newstate, "interface_version": 1})

    def trigger_test_result_change(self, app: master_application.MasterApplication, site: str):
        app.on_testapp_testresult_changed(site, {"pass": 1, "testdata": "AgAACgIETAABCr1VXl69VV5eACAgIP//IAYxMjM0NTYGTXlQYXJ0Bk15Tm9kZQhNeVRlc3RlcgVNeUpvYgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAUKAQEmAA8KAQAAAAEBQQAAAABAAAD/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAmAA8KAgAAAAEBQAAAAEBAAAD/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAUAAUUAQEAAgABAP//AIAAgNEHAAAAAAAWAAEeAQEBAAAAAAAAAAAAAAABAAAA/////wcAARTBVV5eIAAA"})

    def test_masterapp_missed_broker_field_configuration(self):
        cfg = self.default_configuration()
        cfg.pop("broker_host")
        with pytest.raises(SystemExit):
            with pytest.raises(KeyError):
                _ = master_application.MasterApplication(cfg)

    def test_masterapp_correct_number_of_sites_triggers_initialized(self):
        cfg = self.default_configuration()
        app = master_application.MasterApplication(cfg)
        app.startup_done()
        print(app)
        assert(app.state == 'connecting')
        self.trigger_control_state_change(app, "0", "idle")
        assert(app.state == 'connecting')
        self.trigger_control_state_change(app, "1", "idle")
        assert(app.state == 'initialized')

    def test_masterapp_loadlot_triggers_load_commands(self, mocker):
        mocker.patch.object(master_connection_handler.MasterConnectionHandler, "send_load_test_to_all_sites")
        cfg = self.default_configuration()
        app = master_application.MasterApplication(cfg)
        app.startup_done()
        app.all_sites_detected()
        assert(app.state == 'initialized')
        cmd = {'command': 'load', 'lot_number': 4711}
        app.load_command(cmd)
        master_connection_handler.MasterConnectionHandler.send_load_test_to_all_sites.assert_called_once()

    def test_masterapp_siteloadcomplete_triggers_ready(self, mocker):
        mocker.patch.object(master_connection_handler.MasterConnectionHandler, "send_load_test_to_all_sites")
        cfg = self.default_configuration()
        app = master_application.MasterApplication(cfg)
        app.startup_done()
        app.all_sites_detected()
        assert(app.state == 'initialized')
        cmd = {'command': 'load', 'lot_number': 4711}
        app.load_command(cmd)

        self.trigger_control_state_change(app, "1", "loading")
        self.trigger_control_state_change(app, "0", "loading")

        assert(app.state == "loading")
        self.trigger_control_state_change(app, "0", "busy")
        assert(app.state == "loading")
        self.trigger_test_state_change(app, "0", "idle")

        self.trigger_control_state_change(app, "1", "busy")
        assert(app.state == "loading")
        self.trigger_test_state_change(app, "1", "idle")
        assert(app.state == "ready")

    def test_masterapp_next_triggers_test(self, mocker):
        cfg = self.default_configuration()
        app = master_application.MasterApplication(cfg)
        app.startup_done()
        app.all_sites_detected()
        cmd = {'command': 'load', 'lot_number': 4711}
        app.load_command(cmd)
        app.all_siteloads_complete()
        assert(app.state == "ready")
        mocker.patch.object(master_connection_handler.MasterConnectionHandler, "send_next_to_all_sites")
        app.next(None)
        assert(app.external_state == "testing")
        master_connection_handler.MasterConnectionHandler.send_next_to_all_sites.assert_called_once()

    def test_masterapp_testsdone_triggers_ready(self, mocker):
        cfg = self.default_configuration()
        app = master_application.MasterApplication(cfg)
        app.startup_done()
        app.all_sites_detected()
        cmd = {'command': 'load', 'lot_number': 4711}
        app.load_command(cmd)
        app.all_siteloads_complete()
        app.next(None)
        assert(app.external_state == "testing")
        self.trigger_test_state_change(app, "0", "testing")
        self.trigger_test_state_change(app, "1", "testing")

        self.trigger_test_state_change(app, "1", "idle")
        assert(app.external_state == "testing")
        self.trigger_test_result_change(app, "0")
        assert(app.external_state == "testing")
        self.trigger_test_state_change(app, "0", "idle")
        assert(app.external_state == "testing")
        self.trigger_test_result_change(app, "1")
        assert(app.state == "ready")

    def test_masterapp_crash_triggers_error(self):
        cfg = self.default_configuration()
        app = master_application.MasterApplication(cfg)
        app.startup_done()
        app.all_sites_detected()
        cmd = {'command': 'load', 'lot_number': 4711}
        app.load_command(cmd)
        app.all_siteloads_complete()
        app.testapp_disconnected(1, None)
        assert(app.state == "softerror")

    def test_masterapp_no_sites_configured_triggers_error(self):
        cfg = self.default_configuration()
        cfg['sites'] = []
        with pytest.raises(SystemExit):
            _ = master_application.MasterApplication(cfg)

    def test_masterapp_site_with_bad_interfaceversion_connects_triggers_error(self):
        cfg = self.default_configuration()
        app = master_application.MasterApplication(cfg)
        app.startup_done()
        app.on_control_status_changed("0", {"state": "idle", "interface_version": 120})
        assert (app.state == "error")

    def test_masterapp_testresult_accepted_if_testing(self):
        cfg = self.default_configuration()
        app = master_application.MasterApplication(cfg)
        app.startup_done()
        app.all_sites_detected()
        cmd = {'command': 'load', 'lot_number': 4711}
        app.load_command(cmd)
        app.all_siteloads_complete()
        app.next(None)
        assert(app.external_state == "testing")
        self.trigger_test_state_change(app, "0", "testing")
        self.trigger_test_state_change(app, "1", "testing")

        self.trigger_test_result_change(app, "0")
        self.trigger_test_result_change(app, "1")

        self.trigger_test_state_change(app, "1", "idle")
        assert(app.external_state == "testing")
        self.trigger_test_state_change(app, "0", "idle")
        assert(app.state == "ready")

    def test_masterapp_testresult_triggers_error_if_not_sent_during_test(self):
        cfg = self.default_configuration()
        app = master_application.MasterApplication(cfg)
        app.startup_done()
        app.all_sites_detected()
        cmd = {'command': 'load', 'lot_number': 4711}
        app.load_command(cmd)
        app.all_siteloads_complete()
        app.on_testapp_testresult_changed("0", None)
        assert(app.state == "softerror")

    def test_masterapp_error_state_testapp_crash(self):
        cfg = self.default_configuration()
        app = master_application.MasterApplication(cfg)
        app.startup_done()
        app.all_sites_detected()
        cmd = {'command': 'load', 'lot_number': 4711}
        app.load_command(cmd)
        app.all_siteloads_complete()
        app.on_testapp_testresult_changed("0", None)
        self.trigger_test_state_change(app, "0", "crash")
        assert(app.state == "softerror")
        cmd = {'command': 'reset'}
        app.reset(cmd)
        assert(app.state == "connecting")
