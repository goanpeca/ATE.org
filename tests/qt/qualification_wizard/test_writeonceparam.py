from PyQt5 import QtCore, QtGui, QtWidgets, uic
from pytestqt.qt_compat import qt_api  # debug prints inside unittests
import ATE.org.actions_on.flow.qualificationwizardbase.wizardbase
import ATE.org.actions_on.flow.qualificationwizardbase
import ATE.org.actions_on.flow.qualificationwizardbase.writeoncetextparam
from  ATE.org.actions_on.flow.qualificationwizardbase import * 


class WriteOnceParamWizard(wizardbase.wizardbase):
    def __init__(self):
        # self.parent = parent
        # Note: The init call needs to come after we setup this variable, in order for
        # it to exist when init calls _get_wizard_params
        self.theParam = writeoncetextparam.WriteOnceTextParam("Parameter1")
        super().__init__({}, None)

    def _get_wizard_parameters(self) -> list:
        return [self.theParam]
        
    def _get_wizard_testprogram_slots(self) -> dict:
        return []


def setup_method():
    def setup(test_func):
        def wrap(qtbot):
            window = WriteOnceParamWizard()
            qtbot.addWidget(window)
            return test_func(window, qtbot)
        return wrap
    return setup


@setup_method()
def test_writeonce_param_can_find_line_edit(window, qtbot=None):
    paramField = window.findChild(QtWidgets.QLineEdit, "txtParameter1")
    assert paramField is not None


@setup_method()
def test_writeonce_param_line_edit_is_editable_if_empty(window, qtbot=None):
    window.theParam.load_values(dict())
    paramField = window.findChild(QtWidgets.QLineEdit, "txtParameter1")
    assert(paramField.text() == "")
    assert(paramField.isEnabled() == True)


@setup_method()
def test_writeonce_param_line_edit_is_populated_from_inserted_data_and_disabled(window, qtbot):
    window.theParam.load_values({"Parameter1": "Foobar"})
    paramField = window.findChild(QtWidgets.QLineEdit, "txtParameter1")
    assert(paramField.text() == "Foobar")
    assert(paramField.isEnabled() == False)