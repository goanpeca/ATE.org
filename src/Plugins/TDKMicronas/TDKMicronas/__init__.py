from ATE.org.plugins.hookspec import hookimpl


class BusinessObjectStandin:
    def do_import(self):
        return False

    def do_export(self):
        return False

    def get_abort_reason(self):
        return "This is a standin object without functionality"


class Plugin:

    @hookimpl
    def get_plugin_identification():
        return {
            "Name": "TDK.Micronas Reference Plugin",
            "Version": "0.01"
        }

    @hookimpl
    def get_importer_names():
        return [
            {"Display_name": "Dummy Importer",
             "version": "0.0",
             "name": "TDKMicronas.DummyImporter"}]

    @hookimpl
    def get_exporter_names():
        return [
            {"Display_name": "Dummy Exporter",
             "version": "0.0",
             "name": "TDKMicronas.DummyExporter"}]

    @hookimpl
    def get_equipment_names():
        return [
            {"Display_name": "Dummy Equipment",
             "version": "0.0",
             "name": "TDKMicronas.DummyEquipment"}]

    @hookimpl
    def get_devicepin_importer_names():
        return [
            {"Display_name": "Dummy Pinimport",
             "version": "0.0",
             "name": "TDKMicronas.DummyPinimport"}]

    @hookimpl
    def get_actuator_names():
        return [
            {"Display_name": "Dummy Actuator",
             "version": "0.0",
             "capabilities": (),
             "name": "TDKMicronas.DummyActuator"}]

    @hookimpl
    def get_instrument_names():
        return [
            {"Display_name": "Dummy Instrument",
             "version": "0.0",
             "name": "TDKMicronas.DummyInstrument"}]

    @hookimpl
    def get_importer(importer_name):
        if "TDKMicronas." in importer_name:
            return BusinessObjectStandin()

    @hookimpl
    def get_exporter(exporter_name):
        if "TDKMicronas." in exporter_name:
            return BusinessObjectStandin()

    @hookimpl
    def get_equipment(equipment_name):
        if "TDKMicronas." in equipment_name:
            return BusinessObjectStandin()

    @hookimpl
    def get_devicepin_importer(importer_name):
        if "TDKMicronas." in importer_name:
            return BusinessObjectStandin()

    @hookimpl
    def get_actuator(required_capability):
        return BusinessObjectStandin()

    @hookimpl
    def get_actuator_proxy(required_capability):
        return BusinessObjectStandin()

    @hookimpl
    def get_instrument(instrument_name):
        return BusinessObjectStandin()

    @hookimpl
    def get_instrument_proxy(instrument_name):
        return BusinessObjectStandin()