# `TODO.md` files

- [ATE/apps/TODO.md](ATE/apps/TODO.md)
- [ATE/equipment/TCC/TODO.md](ATE/equipment/TCC/TODO.md)
- [ATE/org/TODO.md](ATE/org/TODO.md)
- [ATE/org/actions_on/TODO.md](ATE/org/actions_on/TODO.md)
- [ATE/org/actions_on/device/TODO.md](ATE/org/actions_on/device/TODO.md)
- [ATE/org/actions_on/die/TODO.md](ATE/org/actions_on/die/TODO.md)
- [ATE/org/actions_on/hardwaresetup/TODO.md](ATE/org/actions_on/hardwaresetup/TODO.md)
- [ATE/org/actions_on/maskset/TODO.md](ATE/org/actions_on/maskset/TODO.md)
- [ATE/org/actions_on/package/TODO.md](ATE/org/actions_on/package/TODO.md)
- [ATE/org/actions_on/product/TODO.md](ATE/org/actions_on/product/TODO.md)
- [ATE/org/actions_on/tests/TODO.md](ATE/org/actions_on/tests/TODO.md)
- [ATE/org/sequencers/TODO.md](ATE/org/sequencers/TODO.md)
- [ATE/org/Templates/TODO.md](ATE/org/Templates/TODO.md)
- [ATE/ui/TODO.md](ATE/ui/TODO.md)
- [SpyderMockUp/TODO.md](SpyderMockUp/TODO.md)

# `README.md` files

- [ATE/equipment/README.md](ATE/equipment/README.md)
- [ATE/Instruments/README.md](ATE/Instruments/README.md)
- [ATE/org/README.md](ATE/org/README.md)
- [ATE/org/actions_on/flow/HTOL/README.md](ATE/org/actions_on/flow/HTOL/README.md)
- [ATE/org/plugins/README.md](ATE/org/plugins/README.md)
- [ATE/org/Templates/README.md](ATE/org/Templates/README.md)
- [ATE/org/Templates/documentation/AEC/README.md](ATE/org/Templates/documentation/AEC/README.md)
- [ATE/testers/README.md](ATE/testers/README.md)
- [ATE/ui/angular/mini-sct-gui/README.md](ATE/ui/angular/mini-sct-gui/README.md)
- [SpyderMockUp/ScreenCasting/README.md](SpyderMockUp/ScreenCasting/README.md)

 # `TODO` items

- [ATE/actuators/magnetic_field/STL/DCS1K.py](ATE/actuators/magnetic_field/STL/DCS1K.py)

	11 : [add the communication 'datasheet' to the doc tree](ATE/actuators/magnetic_field/STL/DCS1K.py#L11)

- [ATE/actuators/magnetic_field/STL/DCS6K.py](ATE/actuators/magnetic_field/STL/DCS6K.py)

	11 : [add the communication 'datasheet' to the doc tree](ATE/actuators/magnetic_field/STL/DCS6K.py#L11)

- [ATE/actuators/temperature/MPI/TA3000A.py](ATE/actuators/temperature/MPI/TA3000A.py)

	12 : [add the communication 'datasheet' to the doc tree](ATE/actuators/temperature/MPI/TA3000A.py#L12)

- [ATE/actuators/temperature/TempTronic/ATS710.py](ATE/actuators/temperature/TempTronic/ATS710.py)

	13 : [add the communication 'datasheet' to the doc tree](ATE/actuators/temperature/TempTronic/ATS710.py#L13)

- [ATE/actuators/temperature/TempTronic/XStream4300.py](ATE/actuators/temperature/TempTronic/XStream4300.py)

	11 : [add the communication 'datasheet' to the doc tree](ATE/actuators/temperature/TempTronic/XStream4300.py#L11)

- [ATE/apps/auto_script.py](ATE/apps/auto_script.py)

	141 : [only one master is supported for now](ATE/apps/auto_script.py#L141)

- [ATE/apps/controlApp/control_connection_handler.py](ATE/apps/controlApp/control_connection_handler.py)

	46 : [as a simple workaround we assume 'python' in current PATH](ATE/apps/controlApp/control_connection_handler.py#L46)

	56 : [this should be configurable in future: it will make the testapp kill itself if this parent process dies](ATE/apps/controlApp/control_connection_handler.py#L56)

	70 : [terminate testapp when control is closed during](ATE/apps/controlApp/control_connection_handler.py#L70)

	76 : [is kill better for linux? (on windows there is only terminate)](ATE/apps/controlApp/control_connection_handler.py#L76)

	186 : [handle status messages](ATE/apps/controlApp/control_connection_handler.py#L186)

- [ATE/apps/handlerApp/handler_connection_handler.py](ATE/apps/handlerApp/handler_connection_handler.py)

	76 : [should master have an explicit id](ATE/apps/handlerApp/handler_connection_handler.py#L76)

	94 : [should master be the only app who communication with the handler](ATE/apps/handlerApp/handler_connection_handler.py#L94)

- [ATE/apps/handlerApp/handler_statemachine_component.py](ATE/apps/handlerApp/handler_statemachine_component.py)

	31 : [error states](ATE/apps/handlerApp/handler_statemachine_component.py#L31)

- [ATE/apps/integration_tests/test_integrate.py](ATE/apps/integration_tests/test_integrate.py)

	45 : [add a better way to configure the test environment (dedicated json file?)](ATE/apps/integration_tests/test_integrate.py#L45)

	59 : [currently this is done to increase code coverage and inlcude STDF processing at all. but there are no assertions of the generated data yet (as they only affect websocket messages for now)](ATE/apps/integration_tests/test_integrate.py#L59)

	63 : [Implement a graceful shutdown for subprocesses (linux can simply use SIGTERM, a portable soluation for windows is a pita)](ATE/apps/integration_tests/test_integrate.py#L63)

	66 : [start a 'parent process watchdog' (see testapp) here as well to ensure we get rid of zombie processes when tests are cancelled? maybe we should do a killall all python processes from our virtualenv on CI as well.](ATE/apps/integration_tests/test_integrate.py#L66)

	79 : [verification should eventually be enabled, but currently the lot number in the xml is invalid](ATE/apps/integration_tests/test_integrate.py#L79)

	192 : [log some information about failures, maybe return two sets (done, fail)](ATE/apps/integration_tests/test_integrate.py#L192)

	426 : [this assertion is commented out, because we don't see 'loading' reliably as well.](ATE/apps/integration_tests/test_integrate.py#L426)

	433 : [If 'tests' are finished too fast, we also don't seetesting (same as the problem with 'loading' above)](ATE/apps/integration_tests/test_integrate.py#L433)

	435 : [Add an issue that short state changes are properly sent to the frontend (needs fix in master background task loop)](ATE/apps/integration_tests/test_integrate.py#L435)

	438 : [assert message with type=testresult is received. not sure if received before or after ready status message.](ATE/apps/integration_tests/test_integrate.py#L438)

	446 : [commented out TEMPORARILY because it fails and we want to start with a green test (reason unclear, master has exception because of event controldisconnected)](ATE/apps/integration_tests/test_integrate.py#L446)

	950 : [Note that eventually the master must publish the combined testresult and we should](ATE/apps/integration_tests/test_integrate.py#L950)

	964 : [commented out, because master does not handle this case correctly right now and makes the test fail (which we dont want right now)](ATE/apps/integration_tests/test_integrate.py#L964)

	1167 : [Check ATE-82 against actual requiremens.](ATE/apps/integration_tests/test_integrate.py#L1167)

- [ATE/apps/masterApp/master_application.py](ATE/apps/masterApp/master_application.py)

	221 : [properly limit source states to valid states where usersettings are allowed to be modified](ATE/apps/masterApp/master_application.py#L221)

	225 : [properly limit source states to valid states where usersettings are allowed to be modified](ATE/apps/masterApp/master_application.py#L225)

	326 : [notify UI of changes/initial settings. Should we send individual messages to all connected websockets or should we rely on mqtt proxy usages (UI just has to subscribe to Master/usersettings topic)?](ATE/apps/masterApp/master_application.py#L326)

	388 : [HACK for quick testing/development: allow to specify the](ATE/apps/masterApp/master_application.py#L388)

	408 : [report error: file could not be loaded (currently only logged)](ATE/apps/masterApp/master_application.py#L408)

	412 : [report error: file was loaded but contains invalid data (currently only logged)](ATE/apps/masterApp/master_application.py#L412)

	472 : [all sorts of error handling (but how do we handle sites from which we cannot process test results, whatever the reason may be)?](ATE/apps/masterApp/master_application.py#L472)

	480 : [this sucks: we need an integer for site number, the id is not guaranteed to be an integer! need other way of configurable lookup for remapping](ATE/apps/masterApp/master_application.py#L480)

	532 : [we probably need to check again if we are still in valid state. an error may occurred by now. also resource configuration may fail.](ATE/apps/masterApp/master_application.py#L532)

	554 : [temporarily exposed so websocket can publish](ATE/apps/masterApp/master_application.py#L554)

	625 : [would we need wait for on_published here to ensure the mqqt loop is not stopped?](ATE/apps/masterApp/master_application.py#L625)

	641 : [the default value of the static file path (here and config template) should](ATE/apps/masterApp/master_application.py#L641)

- [ATE/apps/masterApp/stdf_aggregator.py](ATE/apps/masterApp/stdf_aggregator.py)

	47 : [SDR](ATE/apps/masterApp/stdf_aggregator.py#L47)

- [ATE/apps/testApp/thetestzip_mock.py](ATE/apps/testApp/thetestzip_mock.py)

	113 : [result_ispass](ATE/apps/testApp/thetestzip_mock.py#L113)

	180 : [workaround, need to explicitly set this or serialization raises exception](ATE/apps/testApp/thetestzip_mock.py#L180)

	212 : [this is wrong, need to keep track of passes](ATE/apps/testApp/thetestzip_mock.py#L212)

	391 : [will we change the approach to always publish a full stdf as dut test result](ATE/apps/testApp/thetestzip_mock.py#L391)

	393 : [stdf prolog contains info from all dut tests since load on purpose for now, but this is not meant to stay like this](ATE/apps/testApp/thetestzip_mock.py#L393)

	419 : [do we need nested configs, i.e. restore the previously active config? if yes this needs to be implemented](ATE/apps/testApp/thetestzip_mock.py#L419)

	448 : [should we add records for the non-executed tests here?](ATE/apps/testApp/thetestzip_mock.py#L448)

- [ATE/apps/testApp/thetest_application.py](ATE/apps/testApp/thetest_application.py)

	19 : [reduce, it's temporarily large for manual mqtt messaging](ATE/apps/testApp/thetest_application.py#L19)

	52 : [does not work, os.waitpid can probably not be used, because 'any process' in the progress group includes this one !?](ATE/apps/testApp/thetest_application.py#L52)

	384 : [we probably want a way to indicate an error, such as a resource does not even exist (which we should check earlier, but there should be a way to avoid waiting for the timeout)](ATE/apps/testApp/thetest_application.py#L384)

	405 : [what timeout should we use? how to handle timeout at all? should it abort the whole dut test or just the individual test that uses the resource? probably the former because the environment is not in a sane state?](ATE/apps/testApp/thetest_application.py#L405)

	504 : [we probably don't want to keep running if any](ATE/apps/testApp/thetest_application.py#L504)

	532 : [subsequent connects are currently not really handled here and](ATE/apps/testApp/thetest_application.py#L532)

	538 : [else is here to avoid publishing the initial idle state](ATE/apps/testApp/thetest_application.py#L538)

	576 : [how to report positive init command results? we could also write the testresult](ATE/apps/testApp/thetest_application.py#L576)

	585 : [remove this block later. for now er TEMPORAILRY create job_data (for backward compatibility until master has it implemented)](ATE/apps/testApp/thetest_application.py#L585)

	601 : [code commented: this is currently done in state matching](ATE/apps/testApp/thetest_application.py#L601)

	613 : [use job related info here (e.g. from Master/job topic or passed in some other way with the loadTest command)](ATE/apps/testApp/thetest_application.py#L613)

- [ATE/data/measurements.py](ATE/data/measurements.py)

	43 : [complete the list of 'similar' python libraries, go trugh them to see what is usefull and what is shit.](ATE/data/measurements.py#L43)

- [ATE/data/metis.py](ATE/data/metis.py)

	82 : [move this one to be the first to be checked, as this will be the most common one!](ATE/data/metis.py#L82)

	141 : [add more ...](ATE/data/metis.py#L141)

- [ATE/data/register_map/register_map_abc.py](ATE/data/register_map/register_map_abc.py)

	26 : [Implement](ATE/data/register_map/register_map_abc.py#L26)

	37 : [write the default register_map to a file for debugging purposes](ATE/data/register_map/register_map_abc.py#L37)

	42 : [implement](ATE/data/register_map/register_map_abc.py#L42)

	386 : [think about this ... can't we support positive values ?!?](ATE/data/register_map/register_map_abc.py#L386)

- [ATE/data/register_map/utils/varia.py](ATE/data/register_map/utils/varia.py)

	57 : [add more checkings](ATE/data/register_map/utils/varia.py#L57)

- [ATE/data/STDF/records.py](ATE/data/STDF/records.py)

	338 : [ref value handling is missing here: for arrays (kxTYPE etc.) this returns the size of the array instead of its value for now](ATE/data/STDF/records.py#L338)

	364 : [the following condition should most likely be "Ref is not None", since this one is always true but initialized K to the field with '#' == 3 in case of Ref == None](ATE/data/STDF/records.py#L364)

	480 : [Fill in the int() statement](ATE/data/STDF/records.py#L480)

	483 : [Fill in the int() statement](ATE/data/STDF/records.py#L483)

	608 : [pad with spaces if the length doesn't match !!!](ATE/data/STDF/records.py#L608)

	609 : [OK, but why strip first, just to pad again? common value for "C*1" is a single space ' ', but "C*n" is usually not filled with spaces, is it?](ATE/data/STDF/records.py#L609)

	785 : [the reference handling and/or array ("kxTYPE") handling here is most probably](ATE/data/STDF/records.py#L785)

	1202 : [Implement](ATE/data/STDF/records.py#L1202)

	1613 : [implement the tests for decoding of the V*n type and remove this bypass return statement](ATE/data/STDF/records.py#L1613)

	1779 : [change 'V4' and 'V3' in self.version to 4 and 3 respectively](ATE/data/STDF/records.py#L1779)

	1780 : [Implement the FPE (Field Present Expression) in all records](ATE/data/STDF/records.py#L1780)

	1781 : [Impleent support for the FPE in packing/unpacking](ATE/data/STDF/records.py#L1781)

	1782 : [Run trough all records and set the FPE correct](ATE/data/STDF/records.py#L1782)

	2980 : [Implement "Field Presense Expression" (see PTR record on how)](ATE/data/STDF/records.py#L2980)

	3535 : [Needs some more work](ATE/data/STDF/records.py#L3535)

	4571 : [add a record_list of records to return](ATE/data/STDF/records.py#L4571)

- [ATE/data/STDF/utils.py](ATE/data/STDF/utils.py)

	153 : [add more ...](ATE/data/STDF/utils.py#L153)

	389 : [add other obligatory records here (make it dynamic from 'RecordDefinitions'](ATE/data/STDF/utils.py#L389)

	871 : [Implement implicit compression/decompression](ATE/data/STDF/utils.py#L871)

	980 : [Implement](ATE/data/STDF/utils.py#L980)

	1320 : [split up in test types](ATE/data/STDF/utils.py#L1320)

	1426 : [Implement](ATE/data/STDF/utils.py#L1426)

	1432 : [Implement](ATE/data/STDF/utils.py#L1432)

	1455 : [Implement](ATE/data/STDF/utils.py#L1455)

	1458 : [Implement](ATE/data/STDF/utils.py#L1458)

	1688 : [implement hashing](ATE/data/STDF/utils.py#L1688)

- [ATE/equipment/handlers/Geringer/G2G.py](ATE/equipment/handlers/Geringer/G2G.py)

	11 : [protocol is multiple multi-site ... got something from Ulf, need to](ATE/equipment/handlers/Geringer/G2G.py#L11)

	14 : [add the communication 'datasheet' to the doc tree](ATE/equipment/handlers/Geringer/G2G.py#L14)

- [ATE/equipment/handlers/Ismeca/NY32.py](ATE/equipment/handlers/Ismeca/NY32.py)

	12 : [add the communication 'datasheet' to the doc tree](ATE/equipment/handlers/Ismeca/NY32.py#L12)

- [ATE/equipment/handlers/MultiTest/MT9510.py](ATE/equipment/handlers/MultiTest/MT9510.py)

	11 : [add the communication datasheet to the document tree](ATE/equipment/handlers/MultiTest/MT9510.py#L11)

- [ATE/equipment/handlers/MultiTest/MT9928.py](ATE/equipment/handlers/MultiTest/MT9928.py)

	11 : [add the communication datasheet to the document tree](ATE/equipment/handlers/MultiTest/MT9928.py#L11)

- [ATE/equipment/handlers/Rasco/SO1000.py](ATE/equipment/handlers/Rasco/SO1000.py)

	12 : [add the communication 'datasheet' to the doc tree](ATE/equipment/handlers/Rasco/SO1000.py#L12)

- [ATE/equipment/handlers/Rasco/SO2000.py](ATE/equipment/handlers/Rasco/SO2000.py)

	12 : [add the communication 'datasheet' to the doc tree](ATE/equipment/handlers/Rasco/SO2000.py#L12)

- [ATE/equipment/probers/Accretech/PM90.py](ATE/equipment/probers/Accretech/PM90.py)

	12 : [add the communication 'datasheet' to the doc tree](ATE/equipment/probers/Accretech/PM90.py#L12)

- [ATE/equipment/probers/Accretech/UF200R.py](ATE/equipment/probers/Accretech/UF200R.py)

	12 : [add the communication 'datasheet' to the doc tree](ATE/equipment/probers/Accretech/UF200R.py#L12)

- [ATE/equipment/probers/TEL/P8XL.py](ATE/equipment/probers/TEL/P8XL.py)

	12 : [add the communication 'datasheet' to the doc tree](ATE/equipment/probers/TEL/P8XL.py#L12)

- [ATE/equipment/probers/TEL/PrecioOcto.py](ATE/equipment/probers/TEL/PrecioOcto.py)

	12 : [add the communication 'datasheet' to the doc tree](ATE/equipment/probers/TEL/PrecioOcto.py#L12)

- [ATE/org/abc.py](ATE/org/abc.py)

	8 : [change the capitalization of this file for consistency with the rest of the source tree](ATE/org/abc.py#L8)

	9 : [change the name so that this is no longer recognized as a unit-test ... (ABC.py ?!?)](ATE/org/abc.py#L9)

	25 : [import ABC ... make it a real Abstract Base Class !](ATE/org/abc.py#L25)

	75 : [implement functional test (based on the return value of do not being None](ATE/org/abc.py#L75)

	87 : [Implement pattern extraction from setup](ATE/org/abc.py#L87)

	88 : [Implement pattern extraction from do](ATE/org/abc.py#L88)

	89 : [Implement pattern extraction from teardown](ATE/org/abc.py#L89)

	90 : [Implement pattern extraction from functions in module definitions (definitions.py in the tests directory)](ATE/org/abc.py#L90)

	99 : [Implement tester-state extraction from setup](ATE/org/abc.py#L99)

	100 : [Implement tester-state extraction from do](ATE/org/abc.py#L100)

	101 : [Implement tester-state extraction from teardown](ATE/org/abc.py#L101)

	102 : [Implement tester-state extraction from functions in module definitions (definitions.py in the tests directory)](ATE/org/abc.py#L102)

	111 : [Implement test dependency extraction from do](ATE/org/abc.py#L111)

	570 : [implement the test_dependency](ATE/org/abc.py#L570)

	670 : [pass op & eop to the data manager and get a bincode back.](ATE/org/abc.py#L670)

	719 : [Implement 'get_labels_from_pattern'](ATE/org/abc.py#L719)

	724 : [Implement the unit tests here ...](ATE/org/abc.py#L724)

- [ATE/org/navigation.py](ATE/org/navigation.py)

	81 : [once we are integrated in Spyder, we need to get the following](ATE/org/navigation.py#L81)

	512 : [implement the other checks (see docstring)](ATE/org/navigation.py#L512)

	699 : [refactor this whole thing for better nameing !](ATE/org/navigation.py#L699)

	976 : [fix this](ATE/org/navigation.py#L976)

	1118 : [implement once the pluggy stuff is in place.](ATE/org/navigation.py#L1118)

	1122 : [implement once the pluggy stuff is in place.](ATE/org/navigation.py#L1122)

	1127 : [implement once the pluggy stuff is in place.](ATE/org/navigation.py#L1127)

	1272 : [arg kwarg](ATE/org/navigation.py#L1272)

- [ATE/org/toolbar.py](ATE/org/toolbar.py)

	142 : [do we realy need to blockSignals here ??](ATE/org/toolbar.py#L142)

	180 : [remove hack](ATE/org/toolbar.py#L180)

- [ATE/org/actions_on/device/NewDeviceWizard.py](ATE/org/actions_on/device/NewDeviceWizard.py)

	101 : [also add the Type = ['ASSP' or 'ASIC']](ATE/org/actions_on/device/NewDeviceWizard.py#L101)

	121 : [must be done elsewhere](ATE/org/actions_on/device/NewDeviceWizard.py#L121)

- [ATE/org/actions_on/die/NewDieWizard.py](ATE/org/actions_on/die/NewDieWizard.py)

	259 : [quality need to be defined](ATE/org/actions_on/die/NewDieWizard.py#L259)

- [ATE/org/actions_on/flow/NewFlowWizard.py](ATE/org/actions_on/flow/NewFlowWizard.py)

	80 : [add the whole flow thing](ATE/org/actions_on/flow/NewFlowWizard.py#L80)

	103 : [implement the whole flow thing](ATE/org/actions_on/flow/NewFlowWizard.py#L103)

	134 : [add the whole flow stuff here](ATE/org/actions_on/flow/NewFlowWizard.py#L134)

- [ATE/org/actions_on/hardwaresetup/HardwaresetupItem.py](ATE/org/actions_on/hardwaresetup/HardwaresetupItem.py)

	47 : [implement this](ATE/org/actions_on/hardwaresetup/HardwaresetupItem.py#L47)

- [ATE/org/actions_on/hardwaresetup/HardwareWizard.py](ATE/org/actions_on/hardwaresetup/HardwareWizard.py)

	50 : [try to skip the 'True'](ATE/org/actions_on/hardwaresetup/HardwareWizard.py#L50)

	81 : [move from list to tree for this widget!](ATE/org/actions_on/hardwaresetup/HardwareWizard.py#L81)

	92 : [move from list to tree for this widget!](ATE/org/actions_on/hardwaresetup/HardwareWizard.py#L92)

	95 : [initialize this section](ATE/org/actions_on/hardwaresetup/HardwareWizard.py#L95)

	102 : [initialize this section](ATE/org/actions_on/hardwaresetup/HardwareWizard.py#L102)

	105 : [initialize this section](ATE/org/actions_on/hardwaresetup/HardwareWizard.py#L105)

	236 : [implement a bit more verification](ATE/org/actions_on/hardwaresetup/HardwareWizard.py#L236)

- [ATE/org/actions_on/maskset/NewMasksetWizard.py](ATE/org/actions_on/maskset/NewMasksetWizard.py)

	316 : [this logic is defective, disabled for now, need to be re-done.](ATE/org/actions_on/maskset/NewMasksetWizard.py#L316)

	566 : [Implement the validation of the table](ATE/org/actions_on/maskset/NewMasksetWizard.py#L566)

	645 : [add the wafer map editor here](ATE/org/actions_on/maskset/NewMasksetWizard.py#L645)

	649 : [add the die viewer (based ont the table here)](ATE/org/actions_on/maskset/NewMasksetWizard.py#L649)

	677 : [future impl.](ATE/org/actions_on/maskset/NewMasksetWizard.py#L677)

	698 : [add the company specific plugins here](ATE/org/actions_on/maskset/NewMasksetWizard.py#L698)

- [ATE/org/actions_on/model/BaseItem.py](ATE/org/actions_on/model/BaseItem.py)

	32 : [at some point we are not going to need parameters any more, remove them](ATE/org/actions_on/model/BaseItem.py#L32)

- [ATE/org/actions_on/model/FlowItem.py](ATE/org/actions_on/model/FlowItem.py)

	68 : [Display all testprogramms associated with this flow here.](ATE/org/actions_on/model/FlowItem.py#L68)

- [ATE/org/actions_on/model/TreeModel.py](ATE/org/actions_on/model/TreeModel.py)

	127 : [do we need a sorting-order (alphabetic, etc...) ?](ATE/org/actions_on/model/TreeModel.py#L127)

	211 : [Move this class to its own file.](ATE/org/actions_on/model/TreeModel.py#L211)

- [ATE/org/actions_on/package/NewPackageWizard.py](ATE/org/actions_on/package/NewPackageWizard.py)

	77 : [Implement 'FindOnFileSystem'](ATE/org/actions_on/package/NewPackageWizard.py#L77)

	97 : [Implement, save the file in self.temp_dir under the name of the package !!!](ATE/org/actions_on/package/NewPackageWizard.py#L97)

- [ATE/org/actions_on/product/NewProductWizard.py](ATE/org/actions_on/product/NewProductWizard.py)

	71 : [find an other way to do this](ATE/org/actions_on/product/NewProductWizard.py#L71)

- [ATE/org/actions_on/program/ConfigureTest.py](ATE/org/actions_on/program/ConfigureTest.py)

	50 : [uncomment after binding sql database](ATE/org/actions_on/program/ConfigureTest.py#L50)

	57 : [use validator](ATE/org/actions_on/program/ConfigureTest.py#L57)

	64 : [uncomment after binding sql database](ATE/org/actions_on/program/ConfigureTest.py#L64)

- [ATE/org/actions_on/program/NewProgramWizard.py](ATE/org/actions_on/program/NewProgramWizard.py)

	100 : [commented during develpment](ATE/org/actions_on/program/NewProgramWizard.py#L100)

	167 : [use decorator](ATE/org/actions_on/program/NewProgramWizard.py#L167)

	240 : [data should be retrieved from database (sqlite database will be used), see "navigation.py"](ATE/org/actions_on/program/NewProgramWizard.py#L240)

	352 : [disable temperature view](ATE/org/actions_on/program/NewProgramWizard.py#L352)

	363 : [disable current view](ATE/org/actions_on/program/NewProgramWizard.py#L363)

- [ATE/org/actions_on/tests/NewStandardTestWizard.py](ATE/org/actions_on/tests/NewStandardTestWizard.py)

	33 : [fix this](ATE/org/actions_on/tests/NewStandardTestWizard.py#L33)

	35 : [](ATE/org/actions_on/tests/NewStandardTestWizard.py#L35)

	45 : [fix this](ATE/org/actions_on/tests/NewStandardTestWizard.py#L45)

	65 : [maybe also use the flags (Qt::ItemIsSelectable) ?!?](ATE/org/actions_on/tests/NewStandardTestWizard.py#L65)

	68 : [maybe also use the flags (Qt::ItemIsSelectable) ?!?](ATE/org/actions_on/tests/NewStandardTestWizard.py#L68)

- [ATE/org/actions_on/tests/NewTestWizard.py](ATE/org/actions_on/tests/NewTestWizard.py)

	33 : [fix this](ATE/org/actions_on/tests/NewTestWizard.py#L33)

	35 : [](ATE/org/actions_on/tests/NewTestWizard.py#L35)

	45 : [fix this](ATE/org/actions_on/tests/NewTestWizard.py#L45)

	65 : [maybe also use the flags (Qt::ItemIsSelectable) ?!?](ATE/org/actions_on/tests/NewTestWizard.py#L65)

	68 : [maybe also use the flags (Qt::ItemIsSelectable) ?!?](ATE/org/actions_on/tests/NewTestWizard.py#L68)

- [ATE/org/actions_on/tests/TestItem.py](ATE/org/actions_on/tests/TestItem.py)

	43 : [remove this after update toolbar class](ATE/org/actions_on/tests/TestItem.py#L43)

- [ATE/org/actions_on/utils/FileSystemOperator.py](ATE/org/actions_on/utils/FileSystemOperator.py)

	20 : [what if file exists already !??](ATE/org/actions_on/utils/FileSystemOperator.py#L20)

- [ATE/org/coding/test_generator.py](ATE/org/coding/test_generator.py)

	33 : [maybe move this to 'company specific stuff' later on ?](ATE/org/coding/test_generator.py#L33)

- [ATE/org/plugins/__init__.py](ATE/org/plugins/__init__.py)

	34 : [complete the 'masksetStructure' once the UI is stabilized.](ATE/org/plugins/__init__.py#L34)

- [ATE/org/sequencers/Sequencers.py](ATE/org/sequencers/Sequencers.py)

	18 : [move this to the __init__.py file as the ABC !!!](ATE/org/sequencers/Sequencers.py#L18)

	65 : [verify that the test_class is a child from ATE.Testing.test](ATE/org/sequencers/Sequencers.py#L65)

	186 : [implement console progress feedback](ATE/org/sequencers/Sequencers.py#L186)

- [ATE/testers/__init__.py](ATE/testers/__init__.py)

	3 : [this should later on move to the SCT plugin](ATE/testers/__init__.py#L3)

- [ATE/utils/compression.py](ATE/utils/compression.py)

	26 : [add the hashing possibility](ATE/utils/compression.py#L26)

- [ATE/utils/DT.py](ATE/utils/DT.py)

	458 : [Implement](ATE/utils/DT.py#L458)

- [scripts/list_GPL_lines.py](scripts/list_GPL_lines.py)

	29 : [probably there is a unicode thing inside, need to strip it out](scripts/list_GPL_lines.py#L29)

- [scripts/list_TODO_items.py](scripts/list_TODO_items.py)

	7 : [' items in .py files.](scripts/list_TODO_items.py#L7)

	24 : [probably there is a unicode thing inside, need to strip it out](scripts/list_TODO_items.py#L24)

	26 : [' in line_contents:](scripts/list_TODO_items.py#L26)

	27 : [')[1].strip()](scripts/list_TODO_items.py#L27)

- [scripts/readme.py](scripts/readme.py)

	34 : [probably there is a unicode thing inside, need to strip it out](scripts/readme.py#L34)

	37 : [' in line_contents:](scripts/readme.py#L37)

	38 : [')[1].strip()](scripts/readme.py#L38)

	39 : [' in line_contents:](scripts/readme.py#L39)

	40 : [')[1].strip()](scripts/readme.py#L40)

	41 : [' in line_contents:](scripts/readme.py#L41)

	42 : [')[1].strip()](scripts/readme.py#L42)

- [SCT/elements/physical/ElevATE.py](SCT/elements/physical/ElevATE.py)

	83 : [think about this ... can't we support posetive values ?!?](SCT/elements/physical/ElevATE.py#L83)

	92 : [some checking ...](SCT/elements/physical/ElevATE.py#L92)

- [SCT/elements/physical/__init__.py](SCT/elements/physical/__init__.py)

	25 : [Implement](SCT/elements/physical/__init__.py#L25)

	36 : [write the default register_map to a file for debugging purposes](SCT/elements/physical/__init__.py#L36)

	41 : [implement](SCT/elements/physical/__init__.py#L41)

	383 : [think about this ... can't we support positive values ?!?](SCT/elements/physical/__init__.py#L383)

- [SpyderMockUp/SpyderMockUp.py](SpyderMockUp/SpyderMockUp.py)

	54 : [this should later on move to the SCT plugin](SpyderMockUp/SpyderMockUp.py#L54)

	239 : [and what when there is no self.parent.project_info ?!?](SpyderMockUp/SpyderMockUp.py#L239)

	284 : [Reenable this, if we figure that we *really* want SpyderMock to be in front of our debugger](SpyderMockUp/SpyderMockUp.py#L284)

	342 : [not needed after refactoring .ui file](SpyderMockUp/SpyderMockUp.py#L342)

	354 : [the toolbar need to emit signals so others can connect to it!!!!!](SpyderMockUp/SpyderMockUp.py#L354)

	363 : [implement correctly (not as below)](SpyderMockUp/SpyderMockUp.py#L363)

	654 : [doc structure should follow the directory structure](SpyderMockUp/SpyderMockUp.py#L654)

	716 : [cycle through the directory and add the registermaps](SpyderMockUp/SpyderMockUp.py#L716)

	722 : [cycle through the directory and add the protocols](SpyderMockUp/SpyderMockUp.py#L722)

	728 : [insert the appropriate patterns from /sources/patterns, based on HWR and Base](SpyderMockUp/SpyderMockUp.py#L728)

	734 : [cycle through the states and add the states](SpyderMockUp/SpyderMockUp.py#L734)

	945 : [update the base filter to 'FT' if needed !](SpyderMockUp/SpyderMockUp.py#L945)

	1246 : [look in the directories](SpyderMockUp/SpyderMockUp.py#L1246)

- [SpyderMockUp/ScreenCasting/QtScreenCast.py](SpyderMockUp/ScreenCasting/QtScreenCast.py)

	70 : [check on mac if this works](SpyderMockUp/ScreenCasting/QtScreenCast.py#L70)

	85 : [check if I have all dependencies](SpyderMockUp/ScreenCasting/QtScreenCast.py#L85)

	88 : [implement the microphone-find-thingy](SpyderMockUp/ScreenCasting/QtScreenCast.py#L88)

	185 : [maybe screenG instead ?](SpyderMockUp/ScreenCasting/QtScreenCast.py#L185)

	384 : [how to move the](SpyderMockUp/ScreenCasting/QtScreenCast.py#L384)

---
auto generated : Wednesday, April 29 2020 @ 13:22:55 (Q2 20183)