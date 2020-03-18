import pytest
from PyQt5 import QtCore, Qt

from ATE.org.actions.new.program.NewProgramWizard import NewProgramWizard
from ATE.org.actions.new.program.NewProgramWizard import ErrorMessage
from ATE.org.actions.new.program.NewProgramWizard import Action

from pytestqt.qt_compat import qt_api  # debug prints inside unittests


def debug_message(message):
    qt_api.qWarning(message)


# using this function when running CI build will block for ever
# !!! DON'T !!!
# just for localy debuging purposes
def debug_visual(window, qtbot):
    window.show()
    qtbot.stopForInteraction()


AVAILABE_TESTS = ["test1", "test2"]
def setup_method(show_window=False, test_path="./tests/test"):
    def setup(test_func):
        def wrap(qtbot):
            window = NewProgramWizard(test_path=test_path)
            qtbot.addWidget(window)

            return test_func(window, qtbot)
        return wrap
    return setup


@setup_method()
def test_sequencer_type_default_value(window, qtbot=None):
    assert window.SequencerType.currentText() == "Static"
    assert window.Temperature.text() == "25"


@setup_method()
def test_sequencer_type_default_value_with_wrong_temp_type(window, qtbot=None):
    assert window.SequencerType.currentText() == "Static"
    qtbot.keyClicks(window.Temperature, "2a")
    assert window.Feedback.text() == ErrorMessage.InvalidTemperature()
    assert not window.OKButton.isEnabled()


@setup_method()
def test_select_sequencer_type(window, qtbot=None):
    qtbot.keyClicks(window.SequencerType, "Dynamic")
    assert window.SequencerType.currentText() == "Dynamic"


@setup_method()
def test_select_dynamic_sequencer_type_with_correct_paramters(window, qtbot=None):
    qtbot.keyClicks(window.SequencerType, "Dynamic")
    assert window.SequencerType.currentText() == "Dynamic"
    qtbot.keyClicks(window.Temperature, "24,-10")
    assert window.OKButton.isEnabled()


@setup_method()
def test_select_dynamic_sequencer_type_with_wrong_paramters(window, qtbot=None):
    qtbot.keyClicks(window.SequencerType, "Dynamic")
    assert window.SequencerType.currentText() == "Dynamic"
    qtbot.keyClicks(window.Temperature, "24,a1")
    assert window.Feedback.text() == ErrorMessage.InvalidTemperature()
    assert not window.OKButton.isEnabled()


@setup_method(test_path="./t")
def test_Avalable_test_list_wrong_path(window, qtbot=None):
    assert window.AvailableTests.count() == 0


@setup_method()
def test_Avalable_test_list(window, qtbot=None):
    assert window.AvailableTests.count() == 2


@setup_method()
def test_click_without_selecting(window, qtbot=None):
    actions = {Action.Right(): window.RightButton,
               Action.Left(): window.LeftButton,
               Action.Up(): window.UpButton,
               Action.Down(): window.DownButton}

    for _, action in actions.items():
        with qtbot.waitSignal(action.clicked) as _:
            qtbot.mouseClick(action, QtCore.Qt.LeftButton)
            assert window.Feedback.text() == ErrorMessage.NotSelected()


@setup_method()
def test_select_Available_test_in_list(window, qtbot=None):
    assert window.AvailableTests.count() == 2
    item = window.AvailableTests.findItems(AVAILABE_TESTS[0], Qt.Qt.MatchExactly)
    window.AvailableTests.setCurrentItem(item[0])
    with qtbot.waitSignal(window.RightButton.clicked):
        qtbot.mouseClick(window.RightButton, QtCore.Qt.LeftButton)
        assert window.SelectedTests.count() == 1
