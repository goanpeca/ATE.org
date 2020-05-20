# ATE.org Plugins
This document describes the Plugin Api (or "hookspec" in pluggy terms) of an ATE.org plugin.

Each ATE.org Plugin provides means to access its contents in different forms. Most notably:
- Identification of contents
- Instances of contents

## Design Rationale
The API Design in this document tries to take into account the way the IDE is structured as well as the way Pluggy works. We focus on the following points:
* Ease of integration
* Flexibility
* Extensibility

## Identification
We use the "identification" functions to discover the functionality provided by a given plugin. The plugin shall provide a number of functions, that allow us to query that functionality. 

### Plugin
```
get_plugin_identification() -> plugin_ident
```
This hook shall return a dictionary with the following layout:

```
    name: "Plugin Name"
    version: "Plugin Version"
```

### Plugin Functionality
A given plugin publishes its functionality by means of Importers/Exporters/Actuators/Instruments/Equipments. Each of these can be queried by means of a "get_x_names" function where x is the name of the respective functionality. The returnvalue of the get_x_names functions is always a list of dictionaries, where each dictionary has the following layout:
```
    display_name: "Display Name"
    version: "Object Version"
    name: "Object Name"
```
Where:
* display_name denotes the string, that is used to display the the object in the ATE.org UI.
* Version denotes the Version of the code, that is used for the respective object
* Name: Denotes the actual internal name by which the object is identified within the plugin. The plugin must be able to return an instance of the object when the get_x hook is called with the string name as x_name parameter.


#### Importers
An importer is an object that is able to import a wafermap from a given (importer-specific) datasource and in a given format. E.g. ther might be an importer that imports data as .CSV value from a database.

```
    get_importer_names() -> []
```

#### Exporters
An exporter is an object that is able to export a wafermap from to a given (exporter-specific) datasink and in a given format. E.g. ther might be an exporter that export to .CSV.

```
    get_exporter_names() -> []
```

#### Equipments
An equipment object is used to access the specific functionality of prober or handler.
```
    get_equipment_names() -> []
```

#### Devicepin Importer
A devicepin importer is used to import the pinset, that is accessible for a given device. 
```
    get_devicepin_importer_names() -> []
```


#### Actuators
An actuator is a piece of hardware, that controls some aspect of the test environment (e.g. magenetic field)

```
    get_actuator_names() -> []
```

#### Instruments
An instrument is a piece of hardware, that is used to measure a given aspect of the DUT. It is usually used in a lab context.

```
    get_instrument_names() -> []
```

## Instances
All hooks that deal with the instanciation of objects are provided the name of the plugin that should actually create the instance. The reason is, that pluggy will call each hook for all registered plugins, so a call to "get_importer" will be executed for each plugin, using the same parameter. Since we want to avoid nameclashes of objects we must uniquely identify the actual type of object we want created. E.g., given two plugins P1 and P2, each might contain an importer called "CSV Importer". If we wanted to create an instance of this importer we'd have to call get_importer with "CSV Importer" as importer name. However: Two plugins can provide such an importer, so we can never be sure, which kind of importer we'd get, resulting in possibly unintended behavior. Therefore we use the tuple of plugin_name and importer_name to uniquely identify an objecttype. This means, that each implementation of the hooks in this section will have to check the plugin_name parameter to make sure the call is intended for this plugin. 

A note on dependencies:
Importers and exporters are allowed to depend on PyQt to provide their own UI, if necessary. Actuators, Instruments and Equiments should not depend on PyQt - these objects are created by testcases and usually used in a headless environment (i.e. the tester itself!)

### Importers

```
get_importer(plugin_name, importer_name) -> Importer
```

This hook shall return an instance of an importer with the given name.
An importer is expected to have the following interface:

```
    do_import() -> data
    get_abort_reason() -> string
```

The importer shall show it's own import dialog (which may well be just a file chooser!), perform the import and return the imported data in an - as of now - not yet specified format. If the import fails/is canceled do_import() shall not propagate any exception to the application, but instead return "None". The plugin shall expose the reason, why no data was returned when get_abort_reason is called.

### Exporters
```
get_exporter(plugin_name, exporter_name) -> Exporter
```
This hook shall return an instance of an exporter with the given name. 

An importer is expected to have the following interface:
```
    do_export(data) -> bool
    get_abort_reason() -> string
```
The exporter shall show it's own export dialog (which may well be just a file chooser!) and perform the export. If the export fails/is canceled do_export() shall not propagate any exception to the application, but instead return ```False```. The plugin shall expose the reason, why no data was exported when get_abort_reason is called.

### Equipments
```
get_equipment(plugin_name, equipment_name) -> EquipmentInstance
```
This hook shall return an instance of a given equipment. The returned instance has no specified interface. This hook is intended for use in tests only.

If the plugin is unable to resolve the equipment name it shall *immediatly* throw an exception containing the missing equipment's name. Do not return None in this case as it makes diagnostics harder than a well thought out error string.

### Devicepins
```
get_devicepin_importer(plugin_name, importer_name) -> Importer
```
This hook shall return an instance of a given importer. The returned instance has no specified interface. This hook is intended for use in tests only.

If the plugin is unable to resolve the importer name it shall *immediatly* throw an exception containing the missing importer's name. Do not return None in this case as it makes diagnostics harder than a well thought out error string.

An importer is expected to have the following interface:
```
    do_import() -> data
    get_abort_reason() -> string
```

The importer shall show it's own import dialog (which may well be just a file chooser!), perform the import and return the imported data in an - as of now - not yet specified format. If the import fails/is canceled do_import() shall not propagate any exception to the application, but instead return "None". The plugin shall expose the reason, why no data was returned when get_abort_reason is called.

### Actuators
```
get_actuator(plugin_name, actuator_name) -> ActuatorInstance
```
This hook shall return an instance of a given actuator. The returned instance has no specified interface. This hook is intended for use in tests only.

If the plugin is unable to resolve the actuator name it shall *immediatly* throw an exception containing the missing actuator's name. Do not return None in this case as it makes diagnostics harder than a well thought out error string.

### Instruments
```
get_instrument(plugin_name, instrument_name) -> InstrumentInstance
```
This hook shall return an instance of a given instrument. The returned instance has no specified interface. This hook is intended for use in tests only.

If the plugin is unable to resolve the instrument name it shall *immediatly* throw an exception containing the missing instrument's name. Do not return None in this case as it makes diagnostics harder than a well thought out error string.

## Configuration
At this point we assume, that no plugin will need any kind of central configuration and therefore no method of storing configuration data (e.g. in the project database) is specified for the plugin API.


## Complete Hookspec

```
get_plugin_identification() -> plugin_ident
get_importer_names() -> []
get_exporter_names() -> []
get_equipment_names() -> []
get_devicepin_importer_names() -> []
get_actuator_names() -> []
get_instrument_names() -> []

get_importer(plugin_name, importer_name) -> Importer
get_exporter(plugin_name, exporter_name) -> Exporter
get_equipment(plugin_name, equipment_name) -> EquipmentInstance
get_devicepin_importer(plugin_name, importer_name) -> Importer
get_actuator(plugin_name, actuator_name) -> ActuatorInstance
get_instrument(plugin_name, instrument_name) -> InstrumentInstance
```

The hookspecmarker is "ate.org"


### As basic example plugin
The example in this chapter containes the most basic plugin possible.

__File__: PluginSrc\PluginB\\_\_init__.py
```
import pluggy
import hookspec.ate

class ThePlugin(object):

    @hookspec.ate.hookimpl
    def get_plugin_identification() -> dict:
        return {}
    
    @hookspec.ate.hookimpl
    def get_importer_names() -> []:
        return []

    @hookspec.ate.hookimpl
    def get_exporter_names() -> []:
        return []

    @hookspec.ate.hookimpl
    def get_equipment_names() -> []:
        return []

    @hookspec.ate.hookimpl
    def get_devicepin_importer_names() -> []:
        return []

    @hookspec.ate.hookimpl
    def get_actuator_names() -> []:
        return []

    @hookspec.ate.hookimpl
    def get_instrument_names() -> []:
        return []

    @hookspec.ate.hookimpl
    def get_importer(plugin_name, importer_name) -> Importer:
        throw NotImplementedError

    @hookspec.ate.hookimpl
    def get_exporter(plugin_name, exporter_name) -> Exporter:
        throw NotImplementedError

    @hookspec.ate.hookimpl
    def get_equipment(plugin_name, equipment_name) -> EquipmentInstance:
        throw NotImplementedError

    @hookspec.ate.hookimpl
    def get_devicepin_importer(plugin_name, importer_name) -> Importer:
        throw NotImplementedError
    
    @hookspec.ate.hookimpl
    def get_actuator(plugin_name, actuator_name) -> ActuatorInstance:
        throw NotImplementedError

    @hookspec.ate.hookimpl
    def get_instrument(plugin_name, instrument_name) -> InstrumentInstance:
        throw NotImplementedError
```

### Plugin Installation
Plugins are installed by means of setuptools (Pluggy supports plugin discovery through setuptools entrypoints). For this to work we need a setup.py for each plugin:

__File__: PluginSrc\setup.py
```
from setuptools import setup
setup( 
    name="SomeAtePlugin", 
    install_requires="ate.org", 
    entry_points={"ate.org": ["plug = PluginB:ThePlugin"]}, 
    py_modules=["PluginB"],
)
```