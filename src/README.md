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

	11 : [add the communication 'datasheet' to the doc tree](ATE/actuators/magnetic_field/STL/DCS1K.py#L12)

- [ATE/actuators/magnetic_field/STL/DCS6K.py](ATE/actuators/magnetic_field/STL/DCS6K.py)

	11 : [add the communication 'datasheet' to the doc tree](ATE/actuators/magnetic_field/STL/DCS6K.py#L12)

- [ATE/actuators/temperature/MPI/TA3000A.py](ATE/actuators/temperature/MPI/TA3000A.py)

	12 : [add the communication 'datasheet' to the doc tree](ATE/actuators/temperature/MPI/TA3000A.py#L13)

- [ATE/actuators/temperature/TempTronic/ATS710.py](ATE/actuators/temperature/TempTronic/ATS710.py)

	13 : [add the communication 'datasheet' to the doc tree](ATE/actuators/temperature/TempTronic/ATS710.py#L14)

- [ATE/actuators/temperature/TempTronic/XStream4300.py](ATE/actuators/temperature/TempTronic/XStream4300.py)

	11 : [add the communication 'datasheet' to the doc tree](ATE/actuators/temperature/TempTronic/XStream4300.py#L12)

- [ATE/apps/auto_script.py](ATE/apps/auto_script.py)

	141 : [only one master is supported for now](ATE/apps/auto_script.py#L142)

- [ATE/apps/controlApp/control_connection_handler.py](ATE/apps/controlApp/control_connection_handler.py)

	46 : [as a simple workaround we assume 'python' in current PATH](ATE/apps/controlApp/control_connection_handler.py#L47)

	56 : [this should be configurable in future: it will make the testapp kill itself if this parent process dies](ATE/apps/controlApp/control_connection_handler.py#L57)

	70 : [terminate testapp when control is closed during](ATE/apps/controlApp/control_connection_handler.py#L71)

	76 : [is kill better for linux? (on windows there is only terminate)](ATE/apps/controlApp/control_connection_handler.py#L77)

	186 : [handle status messages](ATE/apps/controlApp/control_connection_handler.py#L187)

- [ATE/apps/handlerApp/handler_connection_handler.py](ATE/apps/handlerApp/handler_connection_handler.py)

	76 : [should master have an explicit id](ATE/apps/handlerApp/handler_connection_handler.py#L77)

	94 : [should master be the only app who communication with the handler](ATE/apps/handlerApp/handler_connection_handler.py#L95)

- [ATE/apps/handlerApp/handler_statemachine_component.py](ATE/apps/handlerApp/handler_statemachine_component.py)

	31 : [error states](ATE/apps/handlerApp/handler_statemachine_component.py#L32)

- [ATE/apps/integration_tests/test_integrate.py](ATE/apps/integration_tests/test_integrate.py)

	45 : [add a better way to configure the test environment (dedicated json file?)](ATE/apps/integration_tests/test_integrate.py#L46)

	59 : [currently this is done to increase code coverage and inlcude STDF processing at all. but there are no assertions of the generated data yet (as they only affect websocket messages for now)](ATE/apps/integration_tests/test_integrate.py#L60)

	63 : [Implement a graceful shutdown for subprocesses (linux can simply use SIGTERM, a portable soluation for windows is a pita)](ATE/apps/integration_tests/test_integrate.py#L64)

	66 : [start a 'parent process watchdog' (see testapp) here as well to ensure we get rid of zombie processes when tests are cancelled? maybe we should do a killall all python processes from our virtualenv on CI as well.](ATE/apps/integration_tests/test_integrate.py#L67)

	79 : [verification should eventually be enabled, but currently the lot number in the xml is invalid](ATE/apps/integration_tests/test_integrate.py#L80)

	192 : [log some information about failures, maybe return two sets (done, fail)](ATE/apps/integration_tests/test_integrate.py#L193)

	426 : [this assertion is commented out, because we don't see 'loading' reliably as well.](ATE/apps/integration_tests/test_integrate.py#L427)

	433 : [If 'tests' are finished too fast, we also don't seetesting (same as the problem with 'loading' above)](ATE/apps/integration_tests/test_integrate.py#L434)

	435 : [Add an issue that short state changes are properly sent to the frontend (needs fix in master background task loop)](ATE/apps/integration_tests/test_integrate.py#L436)

	438 : [assert message with type=testresult is received. not sure if received before or after ready status message.](ATE/apps/integration_tests/test_integrate.py#L439)

	446 : [commented out TEMPORARILY because it fails and we want to start with a green test (reason unclear, master has exception because of event controldisconnected)](ATE/apps/integration_tests/test_integrate.py#L447)

	950 : [Note that eventually the master must publish the combined testresult and we should](ATE/apps/integration_tests/test_integrate.py#L951)

	964 : [commented out, because master does not handle this case correctly right now and makes the test fail (which we dont want right now)](ATE/apps/integration_tests/test_integrate.py#L965)

	1167 : [Check ATE-82 against actual requiremens.](ATE/apps/integration_tests/test_integrate.py#L1168)

- [ATE/apps/masterApp/master_application.py](ATE/apps/masterApp/master_application.py)

	221 : [properly limit source states to valid states where usersettings are allowed to be modified](ATE/apps/masterApp/master_application.py#L222)

	225 : [properly limit source states to valid states where usersettings are allowed to be modified](ATE/apps/masterApp/master_application.py#L226)

	326 : [notify UI of changes/initial settings. Should we send individual messages to all connected websockets or should we rely on mqtt proxy usages (UI just has to subscribe to Master/usersettings topic)?](ATE/apps/masterApp/master_application.py#L327)

	388 : [HACK for quick testing/development: allow to specify the](ATE/apps/masterApp/master_application.py#L389)

	408 : [report error: file could not be loaded (currently only logged)](ATE/apps/masterApp/master_application.py#L409)

	412 : [report error: file was loaded but contains invalid data (currently only logged)](ATE/apps/masterApp/master_application.py#L413)

	472 : [all sorts of error handling (but how do we handle sites from which we cannot process test results, whatever the reason may be)?](ATE/apps/masterApp/master_application.py#L473)

	480 : [this sucks: we need an integer for site number, the id is not guaranteed to be an integer! need other way of configurable lookup for remapping](ATE/apps/masterApp/master_application.py#L481)

	532 : [we probably need to check again if we are still in valid state. an error may occurred by now. also resource configuration may fail.](ATE/apps/masterApp/master_application.py#L533)

	554 : [temporarily exposed so websocket can publish](ATE/apps/masterApp/master_application.py#L555)

	625 : [would we need wait for on_published here to ensure the mqqt loop is not stopped?](ATE/apps/masterApp/master_application.py#L626)

	641 : [the default value of the static file path (here and config template) should](ATE/apps/masterApp/master_application.py#L642)

- [ATE/apps/masterApp/stdf_aggregator.py](ATE/apps/masterApp/stdf_aggregator.py)

	47 : [SDR](ATE/apps/masterApp/stdf_aggregator.py#L48)

- [ATE/apps/testApp/thetestzip_mock.py](ATE/apps/testApp/thetestzip_mock.py)

	113 : [result_ispass](ATE/apps/testApp/thetestzip_mock.py#L114)

	180 : [workaround, need to explicitly set this or serialization raises exception](ATE/apps/testApp/thetestzip_mock.py#L181)

	212 : [this is wrong, need to keep track of passes](ATE/apps/testApp/thetestzip_mock.py#L213)

	391 : [will we change the approach to always publish a full stdf as dut test result](ATE/apps/testApp/thetestzip_mock.py#L392)

	393 : [stdf prolog contains info from all dut tests since load on purpose for now, but this is not meant to stay like this](ATE/apps/testApp/thetestzip_mock.py#L394)

	419 : [do we need nested configs, i.e. restore the previously active config? if yes this needs to be implemented](ATE/apps/testApp/thetestzip_mock.py#L420)

	448 : [should we add records for the non-executed tests here?](ATE/apps/testApp/thetestzip_mock.py#L449)

- [ATE/apps/testApp/thetest_application.py](ATE/apps/testApp/thetest_application.py)

	19 : [reduce, it's temporarily large for manual mqtt messaging](ATE/apps/testApp/thetest_application.py#L20)

	52 : [does not work, os.waitpid can probably not be used, because 'any process' in the progress group includes this one !?](ATE/apps/testApp/thetest_application.py#L53)

	384 : [we probably want a way to indicate an error, such as a resource does not even exist (which we should check earlier, but there should be a way to avoid waiting for the timeout)](ATE/apps/testApp/thetest_application.py#L385)

	405 : [what timeout should we use? how to handle timeout at all? should it abort the whole dut test or just the individual test that uses the resource? probably the former because the environment is not in a sane state?](ATE/apps/testApp/thetest_application.py#L406)

	504 : [we probably don't want to keep running if any](ATE/apps/testApp/thetest_application.py#L505)

	532 : [subsequent connects are currently not really handled here and](ATE/apps/testApp/thetest_application.py#L533)

	538 : [else is here to avoid publishing the initial idle state](ATE/apps/testApp/thetest_application.py#L539)

	576 : [how to report positive init command results? we could also write the testresult](ATE/apps/testApp/thetest_application.py#L577)

	585 : [remove this block later. for now er TEMPORAILRY create job_data (for backward compatibility until master has it implemented)](ATE/apps/testApp/thetest_application.py#L586)

	601 : [code commented: this is currently done in state matching](ATE/apps/testApp/thetest_application.py#L602)

	613 : [use job related info here (e.g. from Master/job topic or passed in some other way with the loadTest command)](ATE/apps/testApp/thetest_application.py#L614)

- [ATE/data/measurements.py](ATE/data/measurements.py)

	43 : [complete the list of 'similar' python libraries, go trugh them to see what is usefull and what is shit.](ATE/data/measurements.py#L44)

- [ATE/data/metis.py](ATE/data/metis.py)

	82 : [move this one to be the first to be checked, as this will be the most common one!](ATE/data/metis.py#L83)

	141 : [add more ...](ATE/data/metis.py#L142)

- [ATE/data/register_map/register_map_abc.py](ATE/data/register_map/register_map_abc.py)

	26 : [Implement](ATE/data/register_map/register_map_abc.py#L27)

	37 : [write the default register_map to a file for debugging purposes](ATE/data/register_map/register_map_abc.py#L38)

	42 : [implement](ATE/data/register_map/register_map_abc.py#L43)

	386 : [think about this ... can't we support positive values ?!?](ATE/data/register_map/register_map_abc.py#L387)

- [ATE/data/register_map/utils/varia.py](ATE/data/register_map/utils/varia.py)

	57 : [add more checkings](ATE/data/register_map/utils/varia.py#L58)

- [ATE/data/STDF/records.py](ATE/data/STDF/records.py)

	338 : [ref value handling is missing here: for arrays (kxTYPE etc.) this returns the size of the array instead of its value for now](ATE/data/STDF/records.py#L339)

	364 : [the following condition should most likely be "Ref is not None", since this one is always true but initialized K to the field with '#' == 3 in case of Ref == None](ATE/data/STDF/records.py#L365)

	480 : [Fill in the int() statement](ATE/data/STDF/records.py#L481)

	483 : [Fill in the int() statement](ATE/data/STDF/records.py#L484)

	608 : [pad with spaces if the length doesn't match !!!](ATE/data/STDF/records.py#L609)

	609 : [OK, but why strip first, just to pad again? common value for "C*1" is a single space ' ', but "C*n" is usually not filled with spaces, is it?](ATE/data/STDF/records.py#L610)

	785 : [the reference handling and/or array ("kxTYPE") handling here is most probably](ATE/data/STDF/records.py#L786)

	1202 : [Implement](ATE/data/STDF/records.py#L1203)

	1613 : [implement the tests for decoding of the V*n type and remove this bypass return statement](ATE/data/STDF/records.py#L1614)

	1779 : [change 'V4' and 'V3' in self.version to 4 and 3 respectively](ATE/data/STDF/records.py#L1780)

	1780 : [Implement the FPE (Field Present Expression) in all records](ATE/data/STDF/records.py#L1781)

	1781 : [Impleent support for the FPE in packing/unpacking](ATE/data/STDF/records.py#L1782)

	1782 : [Run trough all records and set the FPE correct](ATE/data/STDF/records.py#L1783)

	2980 : [Implement "Field Presense Expression" (see PTR record on how)](ATE/data/STDF/records.py#L2981)

	3535 : [Needs some more work](ATE/data/STDF/records.py#L3536)

	4571 : [add a record_list of records to return](ATE/data/STDF/records.py#L4572)

- [ATE/data/STDF/utils.py](ATE/data/STDF/utils.py)

	153 : [add more ...](ATE/data/STDF/utils.py#L154)

	389 : [add other obligatory records here (make it dynamic from 'RecordDefinitions'](ATE/data/STDF/utils.py#L390)

	871 : [Implement implicit compression/decompression](ATE/data/STDF/utils.py#L872)

	980 : [Implement](ATE/data/STDF/utils.py#L981)

	1320 : [split up in test types](ATE/data/STDF/utils.py#L1321)

	1426 : [Implement](ATE/data/STDF/utils.py#L1427)

	1432 : [Implement](ATE/data/STDF/utils.py#L1433)

	1455 : [Implement](ATE/data/STDF/utils.py#L1456)

	1458 : [Implement](ATE/data/STDF/utils.py#L1459)

	1688 : [implement hashing](ATE/data/STDF/utils.py#L1689)

- [ATE/equipment/handlers/Geringer/G2G.py](ATE/equipment/handlers/Geringer/G2G.py)

	11 : [protocol is multiple multi-site ... got something from Ulf, need to](ATE/equipment/handlers/Geringer/G2G.py#L12)

	14 : [add the communication 'datasheet' to the doc tree](ATE/equipment/handlers/Geringer/G2G.py#L15)

- [ATE/equipment/handlers/Ismeca/NY32.py](ATE/equipment/handlers/Ismeca/NY32.py)

	12 : [add the communication 'datasheet' to the doc tree](ATE/equipment/handlers/Ismeca/NY32.py#L13)

- [ATE/equipment/handlers/MultiTest/MT9510.py](ATE/equipment/handlers/MultiTest/MT9510.py)

	11 : [add the communication datasheet to the document tree](ATE/equipment/handlers/MultiTest/MT9510.py#L12)

- [ATE/equipment/handlers/MultiTest/MT9928.py](ATE/equipment/handlers/MultiTest/MT9928.py)

	11 : [add the communication datasheet to the document tree](ATE/equipment/handlers/MultiTest/MT9928.py#L12)

- [ATE/equipment/handlers/Rasco/SO1000.py](ATE/equipment/handlers/Rasco/SO1000.py)

	12 : [add the communication 'datasheet' to the doc tree](ATE/equipment/handlers/Rasco/SO1000.py#L13)

- [ATE/equipment/handlers/Rasco/SO2000.py](ATE/equipment/handlers/Rasco/SO2000.py)

	12 : [add the communication 'datasheet' to the doc tree](ATE/equipment/handlers/Rasco/SO2000.py#L13)

- [ATE/equipment/probers/Accretech/PM90.py](ATE/equipment/probers/Accretech/PM90.py)

	12 : [add the communication 'datasheet' to the doc tree](ATE/equipment/probers/Accretech/PM90.py#L13)

- [ATE/equipment/probers/Accretech/UF200R.py](ATE/equipment/probers/Accretech/UF200R.py)

	12 : [add the communication 'datasheet' to the doc tree](ATE/equipment/probers/Accretech/UF200R.py#L13)

- [ATE/equipment/probers/TEL/P8XL.py](ATE/equipment/probers/TEL/P8XL.py)

	12 : [add the communication 'datasheet' to the doc tree](ATE/equipment/probers/TEL/P8XL.py#L13)

- [ATE/equipment/probers/TEL/PrecioOcto.py](ATE/equipment/probers/TEL/PrecioOcto.py)

	12 : [add the communication 'datasheet' to the doc tree](ATE/equipment/probers/TEL/PrecioOcto.py#L13)

- [ATE/org/abc.py](ATE/org/abc.py)

	8 : [change the capitalization of this file for consistency with the rest of the source tree](ATE/org/abc.py#L9)

	9 : [change the name so that this is no longer recognized as a unit-test ... (ABC.py ?!?)](ATE/org/abc.py#L10)

	25 : [import ABC ... make it a real Abstract Base Class !](ATE/org/abc.py#L26)

	75 : [implement functional test (based on the return value of do not being None](ATE/org/abc.py#L76)

	87 : [Implement pattern extraction from setup](ATE/org/abc.py#L88)

	88 : [Implement pattern extraction from do](ATE/org/abc.py#L89)

	89 : [Implement pattern extraction from teardown](ATE/org/abc.py#L90)

	90 : [Implement pattern extraction from functions in module definitions (definitions.py in the tests directory)](ATE/org/abc.py#L91)

	99 : [Implement tester-state extraction from setup](ATE/org/abc.py#L100)

	100 : [Implement tester-state extraction from do](ATE/org/abc.py#L101)

	101 : [Implement tester-state extraction from teardown](ATE/org/abc.py#L102)

	102 : [Implement tester-state extraction from functions in module definitions (definitions.py in the tests directory)](ATE/org/abc.py#L103)

	111 : [Implement test dependency extraction from do](ATE/org/abc.py#L112)

	570 : [implement the test_dependency](ATE/org/abc.py#L571)

	670 : [pass op & eop to the data manager and get a bincode back.](ATE/org/abc.py#L671)

	719 : [Implement 'get_labels_from_pattern'](ATE/org/abc.py#L720)

	724 : [Implement the unit tests here ...](ATE/org/abc.py#L725)

- [ATE/org/navigation.py](ATE/org/navigation.py)

	81 : [once we are integrated in Spyder, we need to get the following](ATE/org/navigation.py#L82)

	512 : [implement the other checks (see docstring)](ATE/org/navigation.py#L513)

	699 : [refactor this whole thing for better nameing !](ATE/org/navigation.py#L700)

	976 : [fix this](ATE/org/navigation.py#L977)

	1118 : [implement once the pluggy stuff is in place.](ATE/org/navigation.py#L1119)

	1122 : [implement once the pluggy stuff is in place.](ATE/org/navigation.py#L1123)

	1127 : [implement once the pluggy stuff is in place.](ATE/org/navigation.py#L1128)

	1272 : [arg kwarg](ATE/org/navigation.py#L1273)

- [ATE/org/toolbar.py](ATE/org/toolbar.py)

	142 : [do we realy need to blockSignals here ??](ATE/org/toolbar.py#L143)

	180 : [remove hack](ATE/org/toolbar.py#L181)

- [ATE/org/actions_on/device/NewDeviceWizard.py](ATE/org/actions_on/device/NewDeviceWizard.py)

	101 : [also add the Type = ['ASSP' or 'ASIC']](ATE/org/actions_on/device/NewDeviceWizard.py#L102)

	121 : [must be done elsewhere](ATE/org/actions_on/device/NewDeviceWizard.py#L122)

- [ATE/org/actions_on/die/NewDieWizard.py](ATE/org/actions_on/die/NewDieWizard.py)

	259 : [quality need to be defined](ATE/org/actions_on/die/NewDieWizard.py#L260)

- [ATE/org/actions_on/flow/NewFlowWizard.py](ATE/org/actions_on/flow/NewFlowWizard.py)

	80 : [add the whole flow thing](ATE/org/actions_on/flow/NewFlowWizard.py#L81)

	103 : [implement the whole flow thing](ATE/org/actions_on/flow/NewFlowWizard.py#L104)

	134 : [add the whole flow stuff here](ATE/org/actions_on/flow/NewFlowWizard.py#L135)

- [ATE/org/actions_on/hardwaresetup/HardwaresetupItem.py](ATE/org/actions_on/hardwaresetup/HardwaresetupItem.py)

	47 : [implement this](ATE/org/actions_on/hardwaresetup/HardwaresetupItem.py#L48)

- [ATE/org/actions_on/hardwaresetup/HardwareWizard.py](ATE/org/actions_on/hardwaresetup/HardwareWizard.py)

	50 : [try to skip the 'True'](ATE/org/actions_on/hardwaresetup/HardwareWizard.py#L51)

	81 : [move from list to tree for this widget!](ATE/org/actions_on/hardwaresetup/HardwareWizard.py#L82)

	92 : [move from list to tree for this widget!](ATE/org/actions_on/hardwaresetup/HardwareWizard.py#L93)

	95 : [initialize this section](ATE/org/actions_on/hardwaresetup/HardwareWizard.py#L96)

	102 : [initialize this section](ATE/org/actions_on/hardwaresetup/HardwareWizard.py#L103)

	105 : [initialize this section](ATE/org/actions_on/hardwaresetup/HardwareWizard.py#L106)

	236 : [implement a bit more verification](ATE/org/actions_on/hardwaresetup/HardwareWizard.py#L237)

- [ATE/org/actions_on/maskset/NewMasksetWizard.py](ATE/org/actions_on/maskset/NewMasksetWizard.py)

	316 : [this logic is defective, disabled for now, need to be re-done.](ATE/org/actions_on/maskset/NewMasksetWizard.py#L317)

	566 : [Implement the validation of the table](ATE/org/actions_on/maskset/NewMasksetWizard.py#L567)

	645 : [add the wafer map editor here](ATE/org/actions_on/maskset/NewMasksetWizard.py#L646)

	649 : [add the die viewer (based ont the table here)](ATE/org/actions_on/maskset/NewMasksetWizard.py#L650)

	677 : [future impl.](ATE/org/actions_on/maskset/NewMasksetWizard.py#L678)

	698 : [add the company specific plugins here](ATE/org/actions_on/maskset/NewMasksetWizard.py#L699)

- [ATE/org/actions_on/model/BaseItem.py](ATE/org/actions_on/model/BaseItem.py)

	32 : [at some point we are not going to need parameters any more, remove them](ATE/org/actions_on/model/BaseItem.py#L33)

- [ATE/org/actions_on/model/FlowItem.py](ATE/org/actions_on/model/FlowItem.py)

	68 : [Display all testprogramms associated with this flow here.](ATE/org/actions_on/model/FlowItem.py#L69)

- [ATE/org/actions_on/model/TreeModel.py](ATE/org/actions_on/model/TreeModel.py)

	127 : [do we need a sorting-order (alphabetic, etc...) ?](ATE/org/actions_on/model/TreeModel.py#L128)

	211 : [Move this class to its own file.](ATE/org/actions_on/model/TreeModel.py#L212)

- [ATE/org/actions_on/package/NewPackageWizard.py](ATE/org/actions_on/package/NewPackageWizard.py)

	77 : [Implement 'FindOnFileSystem'](ATE/org/actions_on/package/NewPackageWizard.py#L78)

	97 : [Implement, save the file in self.temp_dir under the name of the package !!!](ATE/org/actions_on/package/NewPackageWizard.py#L98)

- [ATE/org/actions_on/product/NewProductWizard.py](ATE/org/actions_on/product/NewProductWizard.py)

	71 : [find an other way to do this](ATE/org/actions_on/product/NewProductWizard.py#L72)

- [ATE/org/actions_on/program/ConfigureTest.py](ATE/org/actions_on/program/ConfigureTest.py)

	50 : [uncomment after binding sql database](ATE/org/actions_on/program/ConfigureTest.py#L51)

	57 : [use validator](ATE/org/actions_on/program/ConfigureTest.py#L58)

	64 : [uncomment after binding sql database](ATE/org/actions_on/program/ConfigureTest.py#L65)

- [ATE/org/actions_on/program/NewProgramWizard.py](ATE/org/actions_on/program/NewProgramWizard.py)

	100 : [commented during develpment](ATE/org/actions_on/program/NewProgramWizard.py#L101)

	167 : [use decorator](ATE/org/actions_on/program/NewProgramWizard.py#L168)

	240 : [data should be retrieved from database (sqlite database will be used), see "navigation.py"](ATE/org/actions_on/program/NewProgramWizard.py#L241)

	352 : [disable temperature view](ATE/org/actions_on/program/NewProgramWizard.py#L353)

	363 : [disable current view](ATE/org/actions_on/program/NewProgramWizard.py#L364)

- [ATE/org/actions_on/tests/NewStandardTestWizard.py](ATE/org/actions_on/tests/NewStandardTestWizard.py)

	33 : [fix this](ATE/org/actions_on/tests/NewStandardTestWizard.py#L34)

	35 : [](ATE/org/actions_on/tests/NewStandardTestWizard.py#L36)

	45 : [fix this](ATE/org/actions_on/tests/NewStandardTestWizard.py#L46)

	65 : [maybe also use the flags (Qt::ItemIsSelectable) ?!?](ATE/org/actions_on/tests/NewStandardTestWizard.py#L66)

	68 : [maybe also use the flags (Qt::ItemIsSelectable) ?!?](ATE/org/actions_on/tests/NewStandardTestWizard.py#L69)

- [ATE/org/actions_on/tests/NewTestWizard.py](ATE/org/actions_on/tests/NewTestWizard.py)

	33 : [fix this](ATE/org/actions_on/tests/NewTestWizard.py#L34)

	35 : [](ATE/org/actions_on/tests/NewTestWizard.py#L36)

	45 : [fix this](ATE/org/actions_on/tests/NewTestWizard.py#L46)

	65 : [maybe also use the flags (Qt::ItemIsSelectable) ?!?](ATE/org/actions_on/tests/NewTestWizard.py#L66)

	68 : [maybe also use the flags (Qt::ItemIsSelectable) ?!?](ATE/org/actions_on/tests/NewTestWizard.py#L69)

- [ATE/org/actions_on/tests/TestItem.py](ATE/org/actions_on/tests/TestItem.py)

	43 : [remove this after update toolbar class](ATE/org/actions_on/tests/TestItem.py#L44)

- [ATE/org/actions_on/utils/FileSystemOperator.py](ATE/org/actions_on/utils/FileSystemOperator.py)

	20 : [what if file exists already !??](ATE/org/actions_on/utils/FileSystemOperator.py#L21)

- [ATE/org/coding/test_generator.py](ATE/org/coding/test_generator.py)

	33 : [maybe move this to 'company specific stuff' later on ?](ATE/org/coding/test_generator.py#L34)

- [ATE/org/plugins/__init__.py](ATE/org/plugins/__init__.py)

	34 : [complete the 'masksetStructure' once the UI is stabilized.](ATE/org/plugins/__init__.py#L35)

- [ATE/org/sequencers/Sequencers.py](ATE/org/sequencers/Sequencers.py)

	18 : [move this to the __init__.py file as the ABC !!!](ATE/org/sequencers/Sequencers.py#L19)

	65 : [verify that the test_class is a child from ATE.Testing.test](ATE/org/sequencers/Sequencers.py#L66)

	186 : [implement console progress feedback](ATE/org/sequencers/Sequencers.py#L187)

- [ATE/testers/__init__.py](ATE/testers/__init__.py)

	3 : [this should later on move to the SCT plugin](ATE/testers/__init__.py#L4)

- [ATE/utils/compression.py](ATE/utils/compression.py)

	26 : [add the hashing possibility](ATE/utils/compression.py#L27)

- [ATE/utils/DT.py](ATE/utils/DT.py)

	458 : [Implement](ATE/utils/DT.py#L459)

- [scripts/list_GPL_lines.py](scripts/list_GPL_lines.py)

	29 : [probably there is a unicode thing inside, need to strip it out](scripts/list_GPL_lines.py#L30)

- [scripts/list_TODO_items.py](scripts/list_TODO_items.py)

	7 : [' items in .py files.](scripts/list_TODO_items.py#L8)

	24 : [probably there is a unicode thing inside, need to strip it out](scripts/list_TODO_items.py#L25)

	26 : [' in line_contents:](scripts/list_TODO_items.py#L27)

	27 : [')[1].strip()](scripts/list_TODO_items.py#L28)

- [scripts/readme.py](scripts/readme.py)

	34 : [probably there is a unicode thing inside, need to strip it out](scripts/readme.py#L35)

	37 : [' in line_contents:](scripts/readme.py#L38)

	38 : [')[1].strip()](scripts/readme.py#L39)

	39 : [' in line_contents:](scripts/readme.py#L40)

	40 : [')[1].strip()](scripts/readme.py#L41)

	41 : [' in line_contents:](scripts/readme.py#L42)

	42 : [')[1].strip()](scripts/readme.py#L43)

- [SCT/elements/physical/ElevATE.py](SCT/elements/physical/ElevATE.py)

	83 : [think about this ... can't we support posetive values ?!?](SCT/elements/physical/ElevATE.py#L84)

	92 : [some checking ...](SCT/elements/physical/ElevATE.py#L93)

- [SCT/elements/physical/__init__.py](SCT/elements/physical/__init__.py)

	25 : [Implement](SCT/elements/physical/__init__.py#L26)

	36 : [write the default register_map to a file for debugging purposes](SCT/elements/physical/__init__.py#L37)

	41 : [implement](SCT/elements/physical/__init__.py#L42)

	383 : [think about this ... can't we support positive values ?!?](SCT/elements/physical/__init__.py#L384)

- [SpyderMockUp/SpyderMockUp.py](SpyderMockUp/SpyderMockUp.py)

	54 : [this should later on move to the SCT plugin](SpyderMockUp/SpyderMockUp.py#L55)

	239 : [and what when there is no self.parent.project_info ?!?](SpyderMockUp/SpyderMockUp.py#L240)

	284 : [Reenable this, if we figure that we *really* want SpyderMock to be in front of our debugger](SpyderMockUp/SpyderMockUp.py#L285)

	342 : [not needed after refactoring .ui file](SpyderMockUp/SpyderMockUp.py#L343)

	354 : [the toolbar need to emit signals so others can connect to it!!!!!](SpyderMockUp/SpyderMockUp.py#L355)

	363 : [implement correctly (not as below)](SpyderMockUp/SpyderMockUp.py#L364)

	654 : [doc structure should follow the directory structure](SpyderMockUp/SpyderMockUp.py#L655)

	716 : [cycle through the directory and add the registermaps](SpyderMockUp/SpyderMockUp.py#L717)

	722 : [cycle through the directory and add the protocols](SpyderMockUp/SpyderMockUp.py#L723)

	728 : [insert the appropriate patterns from /sources/patterns, based on HWR and Base](SpyderMockUp/SpyderMockUp.py#L729)

	734 : [cycle through the states and add the states](SpyderMockUp/SpyderMockUp.py#L735)

	945 : [update the base filter to 'FT' if needed !](SpyderMockUp/SpyderMockUp.py#L946)

	1246 : [look in the directories](SpyderMockUp/SpyderMockUp.py#L1247)

- [SpyderMockUp/ScreenCasting/QtScreenCast.py](SpyderMockUp/ScreenCasting/QtScreenCast.py)

	70 : [check on mac if this works](SpyderMockUp/ScreenCasting/QtScreenCast.py#L71)

	85 : [check if I have all dependencies](SpyderMockUp/ScreenCasting/QtScreenCast.py#L86)

	88 : [implement the microphone-find-thingy](SpyderMockUp/ScreenCasting/QtScreenCast.py#L89)

	185 : [maybe screenG instead ?](SpyderMockUp/ScreenCasting/QtScreenCast.py#L186)

	384 : [how to move the](SpyderMockUp/ScreenCasting/QtScreenCast.py#L385)

---
auto generated : Wednesday, April 29 2020 @ 13:23:42 (Q2 20183)