# ATE Sequencer Interface Specification

## Intro
The sequencer is a piece of software that controls how a given set of tests ("testprogram") is executed within the ATE runtime. The sequencer serves as the entrypoint into the ATE testharness, i.e. it synchronizes with the other members of the system.

## API as seen by the ATE Runtime
The sequencer is visible to two parts of the ATE Runtime: Control and Master. 

### Control
Control will launch the testprogram (and with that the sequencer) using the following commandline options:

* '--device_id', containing the device ID of the device on which the programm is started
* '--site_id', containing the site_id for the site (in case of a standalone MiniSCT this is always 0)
* '--broker_host', containing the IP address of the associated MQTT broker
* '--broker_port', containing the port of the MQTT broker
* '--parent-pid', containing the process ID of the MQTT broker

The testprogram shall pass all these parameters to the sequencer and the sequencer shall do the following:
* Connect to the broker on the provided IP/Port
* Subscribe to the topic \<device-id>/TestApp/cmd
* Post a statusmessage to \<device-id>/TestApp/status/site\<site-id> containing status "idle"

-> ToDo: These settings should actually only be passed to the harness. There is no need for the sequencer
         to know these settings. The testprogram should instanciate the harness and pass it to the sequencer
         on startup

### Master
After the master has received the "idle" state it will assume that the testprogram is ready to do it's duty. As soon as the master receives a test command (by means beyond the scope of this document) it will post a "Next" command to the TestApp/cmd topic, This message contains the sites that are supposed to do the actual testing as well as test options. The sequencer shall:
* Check if it is supposed to execute a test by means of checking the "sites" list for its own site-id.
* Emit a statusmessage containing the status "testing"
* Start the test using the provided parameters.

### Testoptions
Whenever the master emits a "Next" command it will append any usersettings to the command as a Key-Value dataset. These settings include
* Trigger On Test#
* Stop On Fail Setting
* Trigger On Fail Setting

and more. The master expects the testprogram to pay heed to these settings. Since the master sends these settings with every "Next" the testprogram/sequencer must be able to deal with "suddenly" changing settings.

## The Runtime as seen by the sequencer
Each and every instrument/actuator is either controlled by the TCC or the master.

### Proxies/Shims
All additional devices will usually be either controlled by the master or by an instance even higher up in the hierarchy. This means, that the testprogram will usually not be able to directly influence the behavior of such a device, instead it will have to send requests to the master which will - depending on the peripheral in question - either control the peripheral or relay the request to the next higher instance (i.e. TCC). In order to provide a readable and ergonomic interface for the test each peripheralimplementation shall come in two flavours:
* A proxy class that provides an easy to use interface for the test, but will - in the background - translate methodcalls to mqtt requests and block until the request has been fulfilled
* A concrete implementation, that will actually implement the interface to the peripheral. 

The proxy will be instanciated for each testprogramm (common.py), whereas the actual implementation will run on the master.

Example:
Suppose we have an object called the "K2000", which can be activated or deactivated. In the test we'd like an interface similar to the following:

```
k2000 = pluggy.get_equipment_proxy("k2000")
k2000.activate()
```

The proxy side of the activate method would be as follows:

```
activate(self):
    mqttclient.send("{cmd:activate"})
    mqttclient.wait_response("activate")
```

Whereas the code on the master would be:

```
resource = pluggy.get_equipment_instance("k2000")
resource.activate()


class k2000(object):
    activate(self):
        hdl = open("dev/tty0/")
        write(hdl, "do stuff)
```

To enable this behavior the hookspec for an ATE.org Plugin is changed as follows:
```
get_plugin_identification() -> plugin_ident
get_importer_names() -> []
get_exporter_names() -> []
get_equipment_names() -> []
get_devicepin_importer_names() -> []

get_instrument_names() -> []

get_importer(importer_name) -> Importer
get_exporter(exporter_name) -> Exporter
get_equipment(equipment_name) -> EquipmentInstance
get_devicepin_importer(importer_name) -> Importer

get_actuator(required_capability) -> ActuatorInstance
get_actuator_proxy(required_capability) -> ActuatorProxy

get_instrument(instrument_name) -> InstrumentInstance
get_instrument_proxy(required_capability) -> InstrumentProxy
```

The get_xx_proxy implementations shall be used by the testprogram to obtain a proxy implementation, whereas the get_xx implementations shall be used by the controlling instance (i.e. the master) to obtain actual implementations when the testprogram sends a request by proxy.
Note: Structuring the hookspec this way allows use to also use concrete implementations of actuators/instruments in the tests, should the need arise. In fact, one could go as far as to only generate testcode that uses proxies for hardwaresetups where parallelism is > 1. 

### Capability based actuators
While instruments denote concrete implementations of a given device actuators - from the perspective of the test -
describe a concept, e.g. "a thing, that can act as a power source" or "a thing, that can genereate a magentic field".
All plugins anounce the capabilities of their actuators by means of a list of capability strings:

```
{
    display_name:"STL Quelle",
    name: "stl.quelle",
    capabilities: ("MagField")
}
````

The testprogram will request actuators based on the aspect of the testenvironment it needs to modified, i.e. it will request a "MagField" actuator. This means, that the sequencer has to provide means to resolve this kind of actuator and to return a proxy object to the test.

### Testresults and Testend
The sequencer is free to send testresult as fragments at any time during a testrun. Sending a testresult is archieved by posting an mqtt message to "ate/\<device-id>/TestApp/stdf/sitesite\<site-id>" containing the STDF data encoded as Base64 string.

After the complete testprogram has run its course, i.e. all tests for the dut in question have either passed or the testing was stopped due to a test failing, the testprogramm shall change its state to "idle", indicating, that it is ready to test the next dut.

Note: As soon as the sequencer changes its state from "testing" to "idle" the master may begin to process the testresults received by that point. Any testresults emitted after this statetransition will cause a system error (this is by design, as it hints at a testprogram that does not behave as expected!).

Also Note: The sequencer is expected to deliver a testresult within 15 seconds. This is currently not a configurable value.

### Batch End
The master may - at any time when no testing is in progress - send a "Terminate" command. The testprogram/sequencer shall cease execution and exit upon receiving this command. It shall further advertise a clean shutdown by publishing the state "Shutdown".

## Tests as seen by the sequencer
The sequencer expects to be fed instances of objects that inherit from itest_case and implement the interface of itest_case:

```
class itest_case():
    def run(self, ennvironment) -> (bool, sbin, list):
        pass
```

The sequencer makes the following assumptions regarding run:
* The testinstances shall need no further configuration after being added to the sequencer
* run shall be stateless, i.e.: the sequencer shall be able to call run as often as necessary, without state from previous calls interfering with the testexecution
* the testcase shall need no explicit cleanup.
* the sequencer will inject the environment containing all external resources into the testcase instance.
* the test is expected to return a tuple containing a "fail" value, a soft-bin, and a list of bytes containing the STDF encoded data of the testrun

## The sequencer as seen by the testprogram
This class is responsible for all basic operations regarding the management of testcases. Specialised derivates (FixedTemperatureSequencer, VariableTemperatureSequencer, etc.) implement specific sequencer behaviors.

### Interface of sequencer_base

```
def register_test(test_case_instance)
def run(execution_policy_instance, environment)
```

### Environments
The environemnt provides the means for a testcase to interact with the testenvironment, i.e.: All instruments and actuators available for the test are stored in the environment. The testprogram is responsible for setting up an environment instance that matches the physical hardware available and to provide it to the sequencer, which will in turn pass it to each testcase.

### Execution Policies
An execution policy controls how the testcases attached to a given sequencer are executed.
* SingleShotExecutionPolicy: This policy will execute each testcase exactly once
* LoopCylceExecutionPolicy: This policy will cylce N times through all testcases

Each policy will call the function "after_test_cb" after a testcase was completed and "after_cycle_cb" after a cycle through all testcases was completed. The callbacks are intended to allow custom sequencers to add extra behavior (e.g. one sequencer might change the temperature of the testchamber after each run)

#### The after_test_cb method
```
def after_test_cb(self, test_instance, test_index, test_result) -> bool
```

This function is called by the execution policy after each test in the testlist. The execution policy pases the concrete testintsance, that was executed, the index of the instance (i.e. its position in the testprogram!) and the testresult to the callback, where the testresult is a tuple of (bool, int, list), as defined in the testinterface.

The sequencer is expected to:
* Check any special settings such as trigger_on_test and obey these settings.
* Send the testresult to the master in the testresult topic.
* Return either TRUE if the execution policy should continue testing or FALSE if the execution policy should abort testing (e.g. if stop_on_fail is set to TRUE)

Note that sequencer_base already has an implementation that behaves as specified, so all deriving sequencers should always call the base implemenation after they have done the special stuff they need to do.

#### The after_test_cycle method
This method is not called, if a testcycle was aborted by the sequencer

#### Propagating STDF data
Each unique testcase is responsible for generating STDF fragments. The sequencer will have to propagate these fragments in the after_test_cb. Furthermore, the sequencer will have to generate a valid STDF header beforehand and propagate it to the leading system.