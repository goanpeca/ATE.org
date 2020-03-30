import pytest
from PyQt5 import QtCore, Qt

from ATE.org.actions_on.hardwaresetup.ViewHardwaresetupSettings import ViewHardwaresetupSettings
from ATE.org.actions_on.hardwaresetup.ViewHardwaresetupSettings import ErrorMessage
from ATE.org.navigation import project_navigator
from pytestqt.qt_compat import qt_api  # debug prints inside unittests


def debug_message(message):
    qt_api.qWarning(message)


# using this function when running CI build will block for ever
# !!! DON'T !!!
# just for localy debuging purposes
def debug_visual(window, qtbot):
    window.show()
    qtbot.stopForInteraction()


NOT_VALID_CONFIG = {"Single": 'df', "Probe": 'abc'}

CONFIGURATION = {'SingleSiteLoadboard': 'abc',
                 'SingleSiteDIB': 'cba',
                 'MultiSiteLoadboard': 'bac',
                 'MultiSiteDIB': 'urt',
                 'ProbeCard': 'ttr',
                 'Parallelism': 1}

HW_NAME = "HW1"
DB_FILE = "./tests/qt/test.sqlite5"


def setup_method(configuration=None):
    def setup(test_func):
        def wrap(qtbot):
            proj_nav = project_navigator("./tests/qt/")
            proj_nav.db_file = ""
            proj_nav.create_sql_connection()
            window = ViewHardwaresetupSettings(configuration, HW_NAME)
            window()
            qtbot.addWidget(window)

            return test_func(window, qtbot)
        return wrap
    return setup


@setup_method(NOT_VALID_CONFIG)
def test_no_valid_configuration(window, qtbot=None):
    assert window.Feedback.text() == ErrorMessage.InvalidConfigurationElements()

@setup_method(configuration=CONFIGURATION)
def test_valid_configuration(window, qtbot=None):
    assert window.SingleSiteLoadboard.text() == 'abc'
    assert window.SingleSiteDIB.text() == 'cba'
    assert window.MultiSiteLoadboard.text() == 'bac'
    assert window.MultiSiteDIB.text() == 'urt'
    assert window.ProbeCard.text() == 'ttr'
