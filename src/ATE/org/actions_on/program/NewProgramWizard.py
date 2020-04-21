from PyQt5 import  QtGui, QtCore, QtWidgets, QtSql
from PyQt5 import uic
import  sys, os, re
from enum import Enum

from functools import wraps

from ATE.org.actions_on.program.ConfigureTest import ConfigureTest


class Action(Enum):
    Up = 'Up'
    Down = 'Down'
    Left = 'Left'
    Right = 'Right'

    def __call__(self):
        return self.value


class Sequencer(Enum):
    Static = 'Static'
    Dynamic = 'Dynamic'

    def __call__(self):
        return self.value


class ErrorMessage(Enum):
    NotSelected = "no test is selected"
    InvalidInput = "invalid input"
    InvalidTemperature = "invalid temperature value(s)"

    def __call__(self):
        return self.value


DEFAULT_TEMPERATURE = '25'


TEST_PATH = os.path.dirname(os.path.realpath(__file__)) + '/test'


class NewProgramWizard(QtWidgets.QDialog):
    def __init__(self, parent=None, test_path=None):
        super().__init__()
        self.parent = parent
        self.path = TEST_PATH if test_path is None else test_path

        # list of all available test
        self.tests_list = []

        # list of choosen tests
        self.tests_choosen = []

        self.current_selected_test = None

        self._load_ui()
        self._setup()
        self._view()
        self._connect_event_handler()

    def __call__(self):
        # self.show()
        pass

    def __enter__(self):
        self.show()
        return self
        # self.exec_()

    def __exit__(self, exc_type, exc_val, exc_tb):
        del self

    def _load_ui(self):
        ui = __file__.replace('.py', '.ui')
        if not os.path.exists(ui):
            raise Exception(f'can not find {ui}')

        uic.loadUi(ui, self)

    def _connect_event_handler(self):
        self.OKButton.clicked.connect(self._save_configuration)
        self.CancelButton.clicked.connect(self._cancel)

        self.AvailableTests.itemClicked.connect(self._store_selected_test)
        self.SelectedTests.itemClicked.connect(self._store_selected_test)

        self.SelectedTests.itemDoubleClicked.connect(self._config_selected_test)

        self.UpButton.clicked.connect(lambda: self._move_test(Action.Up()))
        self.DownButton.clicked.connect(lambda: self._move_test(Action.Down()))
        self.LeftButton.clicked.connect(lambda: self._move_test(Action.Left()))
        self.RightButton.clicked.connect(lambda: self._move_test(Action.Right()))

        self.SequencerType.currentIndexChanged.connect(self._sequencer_type_changed)
        self.Temperature.textEdited.connect(self._verify_input_temperature)

    def _setup(self):
        # windows setup
        # TODO: commented during develpment
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)   # not needed in development phase
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)

        # self.setWindowTitle(' '.join(re.findall('.[^A-Z]*', os.path.basename(__file__).replace('.py', ''))))
        self.setWindowTitle("Test Program Configuraiton")

        self.SelectedTests.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.AvailableTests.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        self.RightButton.setToolTip("select")

        from ATE.org.actions_on.program.Actions import ACTIONS
        icon_up = QtGui.QIcon(ACTIONS['arrow-up'])
        self.UpButton.setIcon(icon_up)
        self.UpButton.setText("")

        icon_down = QtGui.QIcon(ACTIONS['arrow-down'])
        self.DownButton.setIcon(icon_down)
        self.DownButton.setText("")
        
        icon_left = QtGui.QIcon(ACTIONS['arrow-left'])
        self.LeftButton.setIcon(icon_left)
        self.LeftButton.setText("")

        icon_right = QtGui.QIcon(ACTIONS['arrow-right'])
        self.RightButton.setIcon(icon_right)
        self.RightButton.setText("")

    def _view(self):
        # button setup
        # feedback text
        self.Feedback.setText('')
        # self.Feedback.setStyleSheet('')

        # set seqeuncer types
        self.SequencerType.addItems([Sequencer.Static(), Sequencer.Dynamic()])
        self.Temperature.setText(DEFAULT_TEMPERATURE)

        # list availabe tests
        self.AvailableTests.addItems(self._get_available_tests())

    def _sequencer_type_changed(self, item):
        if self.SequencerType.itemText(item) == Sequencer.Static():
            self.Temperature.setText(DEFAULT_TEMPERATURE)
            return

        self.Temperature.setText(f'{DEFAULT_TEMPERATURE},')

    def _store_selected_test(self, item):
        self.current_selected_test = item

    def _config_selected_test(self, item):
        # pop up new dialog
        c = ConfigureTest(item.text())
        c.show()

    def _move_test(self, action):
        try:
            { Action.Up(): lambda: self._move_up(),
              Action.Down(): lambda: self._move_down(),
              Action.Left(): lambda: self._remove_from_testprogram(),
              Action.Right(): lambda: self._add_to_testprogram(),
            }[action]()
        except Exception:
            raise (f'action "{action}" not recognized')

    # TODO: use decorator
    def _move_if_selected(self, func):
        @wraps(func)
        def move_func():
            if self.current_selected_test is None:
                self._update_feedback(ErrorMessage.NotSelected())
                return

            func()
        return move_func

    @QtCore.pyqtSlot()
    def _move_up(self):
        selected_items = len(self.SelectedTests.selectedItems())
        if selected_items == 0 or selected_items > 1:
            self._update_feedback(ErrorMessage.NotSelected())
            return

        if self.SelectedTests.currentRow() > 0:
            current_row = self.SelectedTests.currentRow()
            current_row_item = self.SelectedTests.currentItem()
            self.SelectedTests.takeItem(current_row)
            self.SelectedTests.insertItem(current_row - 1, current_row_item)

        self._update_view()

    @QtCore.pyqtSlot()
    def _move_down(self):
        selected_items = len(self.SelectedTests.selectedItems())
        if selected_items == 0 or selected_items > 1:
            self._update_feedback('no test is selected')
            return

        if self.SelectedTests.currentRow() < self.SelectedTests.count() - 1:
            current_row = self.SelectedTests.currentRow()
            current_row_item = self.SelectedTests.currentItem()
            self.SelectedTests.takeItem(current_row)
            self.SelectedTests.insertItem(current_row + 1, current_row_item)

        self._update_view()

    @QtCore.pyqtSlot()
    def _remove_from_testprogram(self):
        selected_items = len(self.SelectedTests.selectedItems())
        if selected_items == 0:
            self._update_feedback(ErrorMessage.NotSelected())
            return

        for _ in range(selected_items):
            self.SelectedTests.takeItem(self.SelectedTests.currentRow())

        self._update_view()

    @QtCore.pyqtSlot()
    def _add_to_testprogram(self):
        selected_items = len(self.AvailableTests.selectedItems())
        if selected_items == 0:
            self._update_feedback(ErrorMessage.NotSelected())
            return

        for item in self.AvailableTests.selectedItems():
            self.SelectedTests.addItem(f'{item.text()}')

        self._update_view()

    def _save_configuration(self):
        # self.parent.project_info.add_program()  # store configuration in database
        # generate main program
        self.accept()

    def _cancel(self):
        self.reject()

    # TODO: data should be retrieved from database (sqlite database will be used), see "navigation.py"
    def _verify_input_temperature(self, item):
        if self.SequencerType.currentText() == "Static":
            if self._get_static_temp() is None:
                return

        if self.SequencerType.currentText() == "Dynamic":
            if self._get_dynamic_temp() is None:
                return

        self._update_feedback('')
        self.OKButton.setEnabled(True)

    def _get_static_temp(self):
        try:
            temp = int(self.temperature)

        except ValueError:
            self._update_feedback(ErrorMessage.InvalidTemperature())
            self.OKButton.setEnabled(False)
            return None

        return [temp]

    def _get_dynamic_temp(self):
        temp_vars = []
        try:
            temps = self.temperature.split(',')
            if len(temps) == 0:
                return None

            for i in temps:
                if i != '':
                    temp_vars.append(int(i))

        except ValueError:
            self._update_feedback(ErrorMessage.InvalidTemperature())
            self.OKButton.setEnabled(False)
            return None

        return temp_vars

    def _get_test_info_parameter(self, test_name=None):
        import inspect
        import importlib.util

        # check if there is a module with this name
        path = self.path + '/' + test_name + '.py'
        module_name = inspect.getmodulename(path)
        if module_name is None:
            return None

        spec = importlib.util.spec_from_file_location(module_name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        obj = getattr(module, test_name)
        input_parameters = None
        output_parameters = None

        # merge input- and output-dict
        parameters = { **input_parameters, **output_parameters }
        return parameters

    def _inset_selected_test(self, test=None):
        self.SelectedTests.addItem(f'{self.current_selected_test.text()}: {test}')

    def _get_available_tests(self, path=None):
        from os import walk, path

        files = []
        for _, _, filenames in walk(self.path):
            files.extend([path.splitext(x)[0] for x in filenames if not x == '__init__.py' and not x == 'testABC.py'])
            break

        return files

    def _get_selected_tests(self):
        return []

    def _update_view(self):
        self._update_feedback('')

    @property
    def sequencer_type(self):
        return self.SequencerType.currentText()

    @property
    def temperature(self):
        return self.Temperature.text()

    def _update_feedback(self, message):
        if not len(message) == 0:
            self.Feedback.setText(message)
            self.Feedback.setStyleSheet('color: red')
            return

        self.Feedback.setStyleSheet('')
        self.Feedback.setText('')

    def _extract_parameters(self):
        for key, paramter in self.test_paramters.items():
            self.test_name = key
            for param, value in paramter.items():
                if param == 'T':
                    self.temperature = value
                if param == 'i':
                    self.current = value
                else:
                    continue

    def _temperature_view_update(self):
        if self.temperature is None:
            # TODO: disable temperature view
            return

        self.CurrLabel.setText("i(mA)")
        self.CurrMaxVal.setText(str(self.current["Max"]))
        self.CurrMinVal.setText(str(self.current["Min"]))
        self.CurrDefVal.setText(str(self.current["Default"]))
        self.CurrVal.setText(str(self.current["Default"]))

    def _current_view_update(self):
        if self.current is None:
            # TODO: disable current view
            return

        self.TempLabel.setText("T(°C)")
        self.TempMaxVal.setText(str(self.temperature["Max"]))
        self.TempMinVal.setText(str(self.temperature["Min"]))
        self.TempDefVal.setText(str(self.temperature["Default"]))
        self.TempVal.setText(str(self.temperature["Default"]))


def new_program_dialog(parent):
    newProgramWizard = NewProgramWizard(parent)
    newProgramWizard.exec_()
    del newProgramWizard


if __name__ == '__main__':
    import qdarkstyle
    app = QtWidgets.QApplication([])
    app.setStyleSheet(qdarkstyle.load_stylesheet_from_environment())

    with NewProgramWizard() as win:
        sys.exit(app.exec_())
