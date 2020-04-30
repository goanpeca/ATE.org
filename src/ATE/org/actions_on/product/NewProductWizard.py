# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 16:09:05 2019

@author: hoeren
"""
import os
import re

from PyQt5 import QtCore, QtGui, QtWidgets, uic


class NewProductWizard(QtWidgets.QDialog):
    def __init__(self, project_info, read_only=False):
        self.project_info = project_info
        super().__init__()
        self.read_only = read_only
        self._load_ui()
        self._setup()

    def _load_ui(self):
        my_ui = __file__.replace('.py', '.ui')
        uic.loadUi(my_ui, self)

    def _setup(self):
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle(' '.join(re.findall('.[^A-Z]*', os.path.basename(__file__).replace('.py', ''))))

        self.existing_hardwares = self.project_info.get_available_hardwares()
        if len(self.existing_hardwares) == 0:
            self.existing_hardwares = ['']

        self.existing_devices = [''] + self.project_info.get_devices_for_hardware(self.project_info.active_hardware)
        self.existing_products = self.project_info.get_products_for_hardware(self.project_info.active_hardware)

        from ATE.org.validation import valid_product_name_regex
        rxProductName = QtCore.QRegExp(valid_product_name_regex)
        ProductName_validator = QtGui.QRegExpValidator(rxProductName, self)
        self.ProductName.setText("")
        self.ProductName.setValidator(ProductName_validator)
        self.ProductName.textChanged.connect(self._verify)

        self.WithHardware.blockSignals(True)
        self.WithHardware.clear()
        for index, hardware in enumerate(self.existing_hardwares):
            self.WithHardware.addItem(hardware)
            if hardware == self.project_info.active_hardware:
                self.WithHardware.setCurrentIndex(index)

        self.WithHardware.currentIndexChanged.connect(self.hardware_changed)
        self.WithHardware.blockSignals(False)

        self.FromDevice.blockSignals(True)
        self.FromDevice.clear()
        self.FromDevice.addItems(self.existing_devices)
        self.FromDevice.setCurrentIndex(0)  # this is the empty string in the beginning of the list!
        self.FromDevice.currentIndexChanged.connect(self._verify)
        self.FromDevice.blockSignals(False)

        self.Feedback.setText("No die name")
        self.Feedback.setStyleSheet('color: orange')

        self.CancelButton.clicked.connect(self.CancelButtonPressed)
        self.OKButton.clicked.connect(self.OKButtonPressed)
        self.OKButton.setEnabled(False)

        self._verify()

    def hardware_changed(self):
        '''
        if the selected hardware changes, make sure the active_hardware
        at the parent level is also changed and that the new device list
        (for the new hardware) is loaded.
        '''
        # TODO: find an other way to do this
        # self.parent.active_hardware = self.WithHardware.currentText()

        self.existing_devices = [''] + self.project_info.get_devices_for_hardware(self.project_info.active_hardware)
        self.existing_products = self.project_info.get_products_for_hardware(self.project_info.active_hardware)

    def _verify(self):
        if self.existing_hardwares[0] == '':
            self.Feedback.setText("No hardware is available")
            return

        if len(self.existing_devices) == 1:
            self.Feedback.setText("No device is available")
            return

        if not self.read_only and self.ProductName.text() in self.existing_products:
            self.Feedback.setText("Product already exists !")
            self.OKButton.setEnabled(False)
        else:
            if self.FromDevice.currentText() == "":
                self.Feedback.setText("No device selected")
                self.OKButton.setEnabled(False)
            else:  # device selected (hardware is always selected)
                self.Feedback.setText("")
                self.OKButton.setEnabled(True)

    def CancelButtonPressed(self):
        self.accept()

    def _get_actual_defintion(self):
        return {'name': self.ProductName.text(),
                'device': self.FromDevice.currentText(),
                'hardware': self.WithHardware.currentText()}

    def OKButtonPressed(self):
        configuration = self._get_actual_defintion()

        self.project_info.add_product(configuration['name'], configuration['device'],
                                      configuration['hardware'])
        self.accept()


def new_product_dialog(project_info):
    newProductWizard = NewProductWizard(project_info)
    newProductWizard.exec_()
    del(newProductWizard)


if __name__ == '__main__':
    import sys, qdarkstyle
    from ATE.org.actions.dummy_main import DummyMainWindow

    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    dummyMainWindow = DummyMainWindow()
    dialog = NewProductWizard(dummyMainWindow)
    dummyMainWindow.register_dialog(dialog)
    sys.exit(app.exec_())
