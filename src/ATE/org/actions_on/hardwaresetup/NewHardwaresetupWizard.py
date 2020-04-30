'''
Created on Nov 18, 2019

@author: hoeren
'''
import os
import re

from PyQt5 import QtCore, QtWidgets, uic

from ATE.org.validation import is_ATE_project, is_valid_pcb_name
from ATE.org.actions_on.hardwaresetup.constants import UI_FILE


class NewHardwaresetupWizard(QtWidgets.QDialog):

    def __init__(self, project_info):
        super().__init__()
        self.project_info = project_info

        self._load_ui()
        self._setup()
        self._connect_event_handler()

    def _setup(self):
        self.blockSignals(True)

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)
        self.setWindowTitle(' '.join(re.findall('.[^A-Z]*', os.path.basename(__file__).replace('.py', ''))))

        self.hardware_name = self.project_info.get_next_hardware()
        self.HardwareSetup.setText(self.hardware_name)
        self.HardwareSetup.setEnabled(False)

        self.SingleSiteLoadboard.setText("")

        self.MultiSiteLoadboard.setText("")
        self.MultiSiteLoadboard.setEnabled(False)

        self.ProbeCard.setText("")

        self.SingleSiteDIB.setText("")

        self.MultiSiteDIB.setText("")
        self.MultiSiteDIB.setEnabled(False)

        # self.Parallelism.clear()
        self.Parallelism.addItems(['%s'%(i+1) for i in range(16)])
        self.Parallelism.setCurrentIndex(0) # conforms to '1'
        self.parallelism = int(self.Parallelism.currentText())

        self.Feedback.setText("")
        self.Feedback.setStyleSheet('color: orange')

        self.OKButton.setEnabled(False)
        self.CancelButton.setEnabled(True)
        self.blockSignals(False)

    def _connect_event_handler(self):
        self.CancelButton.clicked.connect(self.CancelButtonPressed)
        self.OKButton.clicked.connect(self.OKButtonPressed)
        self.Parallelism.currentTextChanged.connect(self.ParallelismChanged)
        self.MultiSiteDIB.textChanged.connect(self._verify)
        self.SingleSiteDIB.textChanged.connect(self._verify)
        self.ProbeCard.textChanged.connect(self._verify)
        self.SingleSiteLoadboard.textChanged.connect(self._verify)
        self.MultiSiteLoadboard.textChanged.connect(self._verify)

    def _load_ui(self):
        my_ui = f"{os.path.dirname(os.path.realpath(__file__))}\\{UI_FILE}"
        if not os.path.exists(my_ui):
            raise Exception("can not find %s" % my_ui)
        uic.loadUi(my_ui, self)

    def _verify(self):
        if self.parallelism == 1:
            SingleSiteDIB = self.SingleSiteDIB.text()
            if is_valid_pcb_name(SingleSiteDIB):
                self.Feedback.setText("")
            else:
                self.Feedback.setText("invalid Singel Site DIB Name")
            ProbeCardName = self.ProbeCard.text()
            if is_valid_pcb_name(ProbeCardName):
                self.Feedback.setText("")
            else:
                self.Feedback.setText("invalid ProbeCard Name")
            SingleSiteLoadboardName = self.SingleSiteLoadboard.text()
            if is_valid_pcb_name(SingleSiteLoadboardName):
                self.Feedback.setText("")
            else:
                self.Feedback.setText("invalid Singel Site LoadBoard Name")
        else:
            MultiSiteDIB = self.MultiSiteDIB.text()
            if is_valid_pcb_name(MultiSiteDIB):
                self.Feedback.setText("")
            else:
                self.Feedback.setText("invalid Singel Site DIB Name")
            MultiSiteLoadboardName = self.MultiSiteLoadboard.text()
            if is_valid_pcb_name(MultiSiteLoadboardName):
                self.Feedback.setText("")
            else:
                self.Feedback.setText("invalid Singel Site DIB Name")
            SingleSiteDIB = self.SingleSiteDIB.text()
            if is_valid_pcb_name(SingleSiteDIB):
                self.Feedback.setText("")
            else:
                self.Feedback.setText("invalid Singel Site DIB Name")
            ProbeCardName = self.ProbeCard.text()
            if is_valid_pcb_name(ProbeCardName):
                self.Feedback.setText("")
            else:
                self.Feedback.setText("invalid ProbeCard Name")
            SingleSiteLoadboardName = self.SingleSiteLoadboard.text()
            if is_valid_pcb_name(SingleSiteLoadboardName):
                self.Feedback.setText("")
            else:
                self.Feedback.setText("invalid Singel Site LoadBoard Name")

        if self.Feedback.text() == "":
            if SingleSiteLoadboardName != "":
                self.OKButton.setEnabled(True)
            else:
                self.OKButton.setEnabled(False)

    def ParallelismChanged(self):
        self.parallelism = int(self.Parallelism.currentText())
        if self.parallelism == 1:
            self.MultiSiteLoadboard.setEnabled(False)
            self.MultiSiteDIB.setEnabled(False)
        else:
            self.MultiSiteLoadboard.setEnabled(True)
            self.MultiSiteDIB.setEnabled(True)
        self.update()

    def _get_current_configuration(self):
        return {'SingleSiteLoadboard': self.SingleSiteLoadboard.text(),
                'SingleSiteDIB': self.SingleSiteDIB.text(),
                'MultiSiteLoadboard': self.MultiSiteLoadboard.text(),
                'MultiSiteDIB': self.MultiSiteDIB.text(),
                'ProbeCard': self.ProbeCard.text(),
                'Parallelism': self.parallelism}

    def OKButtonPressed(self):
        name = self.HardwareSetup.text()
        new_name = self.project_info.add_hardware(self._get_current_configuration())
        if name != new_name:
            raise Exception(f"Woops, something wrong with the name !!! '{name}'<->'{new_name}'")

        self.accept()

    def CancelButtonPressed(self):
        self.accept()


def new_hardwaresetup_dialog(project_info):
    newHardwaresetupWizard = NewHardwaresetupWizard(project_info)
    newHardwaresetupWizard.exec_()
    del(newHardwaresetupWizard)


if __name__ == '__main__':
    import sys, qdarkstyle
    from ATE.org.actions.dummy_main import DummyMainWindow

    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    dummyMainWindow = DummyMainWindow()
    dialog = NewHardwaresetupWizard(dummyMainWindow)
    dummyMainWindow.register_dialog(dialog)
    sys.exit(app.exec_())
