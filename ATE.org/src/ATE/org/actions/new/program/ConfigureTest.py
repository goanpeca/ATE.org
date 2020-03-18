from PyQt5 import QtGui, QtCore, QtWidgets, uic
import os
import sys
import json
from enum import Enum

import qtawesome as qta


class Paramters(Enum):
    Temperature = 'Temperature'
    Current = 'Current'

    def __call__(self):
        return self.value


PARAMETER = ['T', 'i']


class ConfigureTest(QtWidgets.QDialog):
    def __init__(self, test_name):
        super().__init__()

        self.test_name = test_name
        self.current = None
        self.temperature = None

        self._load_ui()
        self._setup()
        self._action()
        self._view()

    def show(self):
        self.exec_()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        sys.exit(self.exec_())

    def _load_ui(self):
        ui = __file__.replace('.py', '.ui')
        if not os.path.exists(ui):
            raise Exception(f'can not find {ui}')

        uic.loadUi(ui, self)

    def _setup(self):
        # TODO: uncomment after binding sql database
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)   # not needed in development phase
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)

        # test_configuration = self.test_parser.get_configuration(self.test_name)
        self.setWindowTitle(f'configigure {self.test_name}')

        # TODO: use validator 
        # from ATE.org.validation import valid_integer_regex
        # rxi = QtCore.QRegExp(valid_integer_regex)
        # integer_validator = QtGui.QRegExpValidator(rxi, self)
        # self.Temperature.setValidator(integer_validator)

    def _view(self):
        # TODO: uncomment after binding sql database
        # self._temperature_view_update()
        # self._current_view_update()

        self.TempRefresh.setIcon(QtGui.QIcon(qta.icon('mdi.refresh', color='orange')))
        self.TempRefresh.setText("")
        self.CurrRefresh.setIcon(QtGui.QIcon(qta.icon('mdi.refresh', color='orange')))
        self.CurrRefresh.setText("")

        self.Feedback.setText("")

    def _action(self):
        self.OKButton.clicked.connect(self._save)
        self.CancelButton.clicked.connect(self._cancel)

        self.TempMinVal.setEnabled(False)
        self.TempMaxVal.setEnabled(False)
        self.TempDefVal.setEnabled(False)
        self.TempVal.setEnabled(False)

        self.CurrMinVal.setEnabled(False)
        self.CurrMaxVal.setEnabled(False)
        self.CurrDefVal.setEnabled(False)
        self.CurrVal.setEnabled(False)

    def _save(self):
        self.accept()

    def _cancel(self):
        self.reject()

    def _verify_changes(self, param_type):
        if param_type == Paramters.Temperature():
            if self.TempDefVal.text() != self.TempVal.text():
                self.TempVal.setStyleSheet('color: red')
            else:
                self.TempVal.setStyleSheet('')

        elif param_type == Paramters.Current():
            if self.CurrDefVal.text() != self.CurrVal.text():
                self.CurrVal.setStyleSheet('color: red')
            else:
                self.CurrVal.setStyleSheet('')

    def _verify_input_paramters(self, param_type):
        try:
            if param_type == Paramters.Temperature():
                val = int(self.TempVal.text())
                Max, Min, Default = int(self.TempMaxVal.text()), int(self.TempMinVal.text()), int(self.TempDefVal.text())
            elif param_type == Paramters.Current():
                val = float(self.CurrVal.text())
                Max, Min, Default = float(self.CurrMaxVal.text()), float(self.CurrMinVal.text()), float(self.CurrDefVal.text())
            else:
                pass

        except ValueError:
            self.Feedback.setText('invalid input')
            self.Feedback.setStyleSheet('color: red')
            return

        if not val >= Min or not val <= Max:
            self.Feedback.setText('value is out of range')
            self.Feedback.setStyleSheet('color: red')
            return

        is_changed = val == Default
        self.TempVal.setStyleSheet("color: red")
        print(is_changed)

        self.Feedback.setText('')
