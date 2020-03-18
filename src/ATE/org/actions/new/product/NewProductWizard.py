# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 16:09:05 2019

@author: hoeren
"""
import os
import pickle
import re

from ATE.org.listings import dict_project_paths, list_devices, list_products
from ATE.org.validation import is_ATE_project
from PyQt5 import QtCore, QtGui, QtWidgets, uic


class NewProductWizard(QtWidgets.QDialog):

    def __init__(self, parent):
        self.parent = parent
        super().__init__()

        my_ui = __file__.replace('.py', '.ui')
        if not os.path.exists(my_ui):
            raise Exception("can not find %s" % my_ui)
        uic.loadUi(my_ui, self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle(' '.join(re.findall('.[^A-Z]*', os.path.basename(__file__).replace('.py', ''))))

        self.parent = parent

        self.existing_hardwares = self.parent.project_info.get_hardwares()
        if len(self.existing_hardwares)==0:
            self.existing_hardwares = ['']
        print(f"self.parent.active_hw = {self.parent.active_hw}")
        self.existing_devices = [''] + self.parent.project_info.get_devices_for_hardware(self.parent.active_hw)
        print(f"existing_devices = {self.existing_devices}")
        self.existing_products = self.parent.project_info.get_products_for_hardware(self.parent.active_hw)

        from ATE.org.validation import valid_product_name_regex
        rxProductName = QtCore.QRegExp(valid_product_name_regex)
        ProductName_validator = QtGui.QRegExpValidator(rxProductName, self)
        self.ProductName.setText("")
        self.ProductName.setValidator(ProductName_validator)
        self.ProductName.textChanged.connect(self.verify)

        self.WithHardware.blockSignals(True)
        self.WithHardware.clear()
        for index, hardware in enumerate(self.existing_hardwares):
            self.WithHardware.addItem(hardware)
            if hardware == self.parent.active_hw:
                self.WithHardware.setCurrentIndex(index)
        self.WithHardware.currentIndexChanged.connect(self.hardware_changed)
        self.WithHardware.blockSignals(False)

        self.FromDevice.blockSignals(True)
        self.FromDevice.clear()
        self.FromDevice.addItems(self.existing_devices)
        self.FromDevice.setCurrentIndex(0) # this is the empty string in the beginning of the list!
        self.FromDevice.currentIndexChanged.connect(self.verify)
        self.FromDevice.blockSignals(False)

        self.Feedback.setText("No die name")
        self.Feedback.setStyleSheet('color: orange')

        self.CancelButton.clicked.connect(self.CancelButtonPressed)
        self.OKButton.clicked.connect(self.OKButtonPressed)
        self.OKButton.setEnabled(False)

        self.verify()
        self.show()

    def hardware_changed(self):
        '''
        if the selected hardware changes, make sure the active_hardware 
        at the parent level is also changed and that the new device list
        (for the new hardware) is loaded.
        '''
        self.parent.active_hw = self.WithHardware.currentText()
        self.existing_devices = [''] + self.parent.project_info.get_devices_for_hardware(self.parent.active_hw)
        self.existing_products = self.parent.project_info.get_products_for_hardware(self.parent.active_hw)

    def verify(self):
        if self.ProductName.text() in self.existing_products:
            self.Feedback.setText("Product already exists !")
            self.OKButton.setEnabled(False)
        else:
            if self.FromDevice.currentText() == "":
                self.Feedback.setText("No device selected")
                self.OKButton.setEnabled(False)
            else: # device selected (hardware is always selected)
                self.Feedback.setText("")
                self.OKButton.setEnabled(True)

    def CancelButtonPressed(self):
        self.accept()

    def OKButtonPressed(self):
        name = self.ProductName.text()
        device = self.FromDevice.currentText()
        hardware = self.WithHardware.currentText()

        self.parent.project_info.add_product(name, device, hardware)
        self.parent.update_tree()
        self.accept()

def new_product_dialog(parent):
    newProductWizard = NewProductWizard(parent)
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
