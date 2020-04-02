import pytest
from PyQt5 import QtCore, Qt

from ATE.org.actions_on.maskset.ViewMasksetSettings import ViewMasksetSettings
from ATE.org.actions_on.maskset.ViewMasksetSettings import ErrorMessage
from ATE.org.actions_on.maskset.constants import DEFINITION
from pytestqt.qt_compat import qt_api  # debug prints inside unittests


def debug_message(message):
    qt_api.qWarning(message)


# using this function when running CI build will block for ever
# !!! DON'T !!!
# just for localy debuging purposes
def debug_visual(window, qtbot):
    window.show()
    qtbot.stopForInteraction()


NOT_VALID_CONFIG = {"pads": 2, "DieSize": ('2', '22'), "BondpadTable": {1: ("name", 1, 2, 3, 4, 'A', 'I')}}

DEFINITION["Bondpads"] = 2
DEFINITION["DieSize"] = ('4', '6')
DEFINITION["DieRef"] = ('2', '3') 
DEFINITION["Scribe"] = ('100', '101') 
DEFINITION["Offset"] = ('102', '103') 
DEFINITION["Flat"] = '90'
DEFINITION["BondpadTable"] = {1: ("name", 1, 2, 3, 4, 'A', 'I')}

MASKSET_NAME = "M1"


def setup_method(configuration=None):
    def setup(test_func):
        def wrap(qtbot):
            window = ViewMasksetSettings(configuration, MASKSET_NAME)
            window()
            qtbot.addWidget(window)
            return test_func(window, qtbot)
        return wrap
    return setup


@setup_method(NOT_VALID_CONFIG)
def test_no_valid_configuration(window, qtbot=None):
    assert window.feedback.text() == ErrorMessage.InvalidConfigurationElements()


@setup_method(configuration=DEFINITION)
def test_valid_configuration(window, qtbot):
    assert window.dieSizeX.text() == '4'
    assert window.dieSizeY.text() == '6'

    assert window.dieRefX.text() == '2'
    assert window.dieRefY.text() == '3'

    assert window.scribeX.text() == '100'
    assert window.scribeY.text() == '101'

    assert window.xOffset.text() == '102'
    assert window.yOffset.text() == '103'

    assert window.dieRefX.text() == '2'
    assert window.dieRefY.text() == '3'

    assert window.flat.text() == '90'
