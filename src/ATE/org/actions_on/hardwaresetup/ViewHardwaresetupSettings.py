from PyQt5 import QtCore, QtWidgets, uic
from enum import Enum

import os
import re


from ATE.org.actions_on.hardwaresetup.constants import DEFINITION
from ATE.org.actions_on.hardwaresetup.constants import UI_FILE


class ErrorMessage(Enum):
    NoValidConfiguration = "no valid configuration"
    InvalidConfigurationElements = "configuration does not match the template inside constants.py"
    def __call__(self):
        return self.value


class ViewHardwaresetupSettings(QtWidgets.QDialog):
    def __init__(self, hw_configuration, hw_name):
        self.hw_configuration = hw_configuration
        self.hw_name = hw_name

    def __call__(self):
        super().__init__()
        self._load_ui()
        self._setup(self.hw_name)
        ViewHardwaresetupSettings._show(self, self.hw_configuration)

    def _load_ui(self):
        import os
        my_ui = f"{os.path.dirname(os.path.realpath(__file__))}\{UI_FILE}"
        uic.loadUi(my_ui, self)

    def _setup(self, hw_name):
        self.setWindowTitle(' '.join(re.findall('.[^A-Z]*', os.path.basename(__file__).replace('.py', ''))))
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)

        self.HardwareSetup.setText(hw_name)
        self.HardwareSetup.setEnabled(False)

        self.SingleSiteLoadboard.setEnabled(False)
        self.SingleSiteDIB.setEnabled(False)
        self.MultiSiteLoadboard.setEnabled(False)
        self.MultiSiteDIB.setEnabled(False)
        self.ProbeCard.setEnabled(False)
        self.Parallelism.setEnabled(False)

        self.OKButton.setEnabled(True)
        self.OKButton.clicked.connect(self.accept)

        self.CancelButton.setEnabled(True)
        self.CancelButton.clicked.connect(self.accept)
        self.Feedback.setText("")

    @staticmethod
    def is_valid_configuration(hw_configuration):
        if not hw_configuration.keys() == DEFINITION.keys():
            return False

        return True

    @staticmethod
    def _show(owner, hw_configuration):
        if not ViewHardwaresetupSettings.is_valid_configuration(hw_configuration):
            owner.Feedback.setText(ErrorMessage.InvalidConfigurationElements())
            owner.Feedback.setStyleSheet('color: red')
            return

        owner.Feedback.setText('')
        owner.Feedback.setStyleSheet('')

        owner.SingleSiteLoadboard.setText(hw_configuration["SingleSiteLoadboard"])
        owner.SingleSiteDIB.setText(hw_configuration["SingleSiteDIB"])
        owner.MultiSiteLoadboard.setText(hw_configuration["MultiSiteLoadboard"])
        owner.MultiSiteDIB.setText(hw_configuration["MultiSiteDIB"])
        owner.ProbeCard.setText(hw_configuration["ProbeCard"])
        owner.Parallelism.setCurrentIndex(hw_configuration['Parallelism'] - 1)


def display_hardware_settings_dialog(hw_configuration, hw_name):
    hardware_wizard = ViewHardwaresetupSettings(hw_configuration, hw_name)
    hardware_wizard()
    hardware_wizard.exec_()
    del(hardware_wizard)
