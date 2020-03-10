# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 15:09:41 2019

@author: hoeren
"""
import os
import pickle
import re

import qtawesome as qta
from ATE.org.listings import dict_project_paths, list_devices, list_dies, list_packages
from ATE.org.validation import is_ATE_project, valid_device_name_regex
from PyQt5 import QtCore, QtGui, QtWidgets, uic


class NewDeviceWizard(QtWidgets.QDialog):

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

        self.existing_hardware = self.parent.project_info.get_hardwares()
        self.Hardware.blockSignals(True)
        self.Hardware.clear()
        for index, hardware in enumerate(self.existing_hardware):
            self.Hardware.addItem(hardware)
            if hardware == self.parent.active_hw:
                self.Hardware.setCurrentIndex(index)
        self.Hardware.currentIndexChanged.connect(self.hardware_changed)
        self.Hardware.blockSignals(False)        

        self.existing_packages = self.parent.project_info.get_packages()
        self.Package.blockSignals(True)
        self.Package.clear()
        self.Package.addItems([''] + self.existing_packages + ['Naked Die'])
        self.Package.setCurrentIndex(0) # this is the empty string !
        self.Package.currentIndexChanged.connect(self.verify)
        self.Package.blockSignals(False)

        self.existing_devices = self.parent.project_info.get_devices()
        self.DeviceName.setText("")
        rxDeviceName = QtCore.QRegExp(valid_device_name_regex)
        DeviceName_validator = QtGui.QRegExpValidator(rxDeviceName, self)
        self.DeviceName.setValidator(DeviceName_validator)
        self.DeviceName.textChanged.connect(self.verify)

        self.existing_dies = self.parent.project_info.get_dies_for_hardware(self.parent.active_hw)
        print(f"get_dies_for_hardware = {self.existing_dies}")
        self.AvailableDies.blockSignals(True)
        self.AvailableDies.clear()
        self.AvailableDies.addItems(self.existing_dies)
        self.AvailableDies.clearSelection()
        self.AvailableDies.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.AvailableDies.blockSignals(False)

        self.AddDie.setEnabled(True)
        self.AddDie.setIcon(qta.icon('mdi.arrow-right-bold-outline', color='orange'))
        self.AddDie.clicked.connect(self.add_dies)

        self.RemoveDie.setEnabled(True)
        self.RemoveDie.setIcon(qta.icon('mdi.arrow-left-bold-outline', color='orange'))
        self.RemoveDie.clicked.connect(self.remove_dies)

        self.dies_in_device = []
        self.DiesInDevice.blockSignals(True)
        self.DiesInDevice.clear()
        self.DiesInDevice.addItems(self.dies_in_device)
        self.DiesInDevice.clearSelection()
        self.DiesInDevice.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.DiesInDevice.blockSignals(False)

        self.Feedback.setStyleSheet('color: orange')

        self.CancelButton.clicked.connect(self.CancelButtonPressed)
        self.OKButton.clicked.connect(self.OKButtonPressed)

        self.verify()
        self.show()

    def add_dies(self):
        self.DiesInDevice.blockSignals(True)
        for die_to_add in self.AvailableDies.selectedItems():
            self.DiesInDevice.insertItem(self.DiesInDevice.count(), die_to_add.text())
        self.DiesInDevice.clearSelection()
        self.AvailableDies.clearSelection()
        self.DiesInDevice.blockSignals(False)
        self.check_for_dual_die()
        self.verify()

    def remove_dies(self):
        self.DiesInDevice.blockSignals(True)
        self.DiesInDevice.takeItem(self.DiesInDevice.selectedIndexes()[0].row()) # DiesInDevice set to SingleSelection ;-)
        self.DiesInDevice.clearSelection()
        self.AvailableDies.clearSelection()
        self.DiesInDevice.blockSignals(False)
        self.check_for_dual_die()
        self.verify()
        
    def hardware_changed(self):
        '''
        if the selected hardware changes, make sure the active_hardware 
        at the parent level is also changed, the dies in device list is cleared,
        and the available dies is reloaded.
        '''
        self.parent.active_hw = self.Hardware.currentText()
        self.DiesInDevice.clear()
        self.existing_dies = self.parent.project_info.get_dies_for_hardware(self.parent.active_hw)
        self.AvailableDies.blockSignals(True)
        self.AvailableDies.clear()
        self.AvailableDies.addItems(self.existing_dies)
        self.AvailableDies.clearSelection()
        self.AvailableDies.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.AvailableDies.blockSignals(False)
    
    def verify(self):
        feedback = ""

        device_name = self.DeviceName.text()
        if device_name == "":
            feedback = "Invalid device name"
        elif device_name in self.existing_devices:
            feedback = "device already defined"
        else: # valid device name
            package_name = self.Package.currentText()
            if package_name == '':
                feedback = "No package selected"
            elif package_name != 'Naked Die':
                number_of_dies_in_device = self.DiesInDevice.count()
                if self.DualDie.checkState(): # dual die
                    feedback = ''
                else: # normal
                    if number_of_dies_in_device == 0:
                        feedback = 'need at least ONE die'
                    else:
                        feedback = ''
            else: # Naked die
                number_of_dies_in_device = self.DiesInDevice.count()
                if number_of_dies_in_device == 0:
                    feedback = "select the naked die"
                elif number_of_dies_in_device > 1:
                    feedback = "only one die allowed in 'Naked Die'"
                else: # one selected
                    feedback = ''

        self.Feedback.setText(feedback)

        if feedback == "":
            self.OKButton.setEnabled(True)
        else:
            self.OKButton.setEnabled(False)

    def check_for_dual_die(self):
        '''
        this mentod will check if a configuration qualifies for 'DualDie',
        if so, the radio will be enabled, if not disabled (and cleared)
        '''
        temp = []
        for die in self.DiesInDevice.findItems('*', QtCore.Qt.MatchWrap | QtCore.Qt.MatchWildcard):
            temp.append(die.text())
        if len(temp)==2:
            if temp[0] == temp[1]:
                self.DualDie.setEnabled(True)
            else:
                self.DualDie.setCheckState(QtCore.Qt.Unchecked)
                self.DualDie.setEnabled(False)
        else:
            self.DualDie.setCheckState(QtCore.Qt.Unchecked)
            self.DualDie.setEnabled(False)

    def CancelButtonPressed(self):
        self.accept()

    def OKButtonPressed(self):
        name = self.DeviceName.text()
        hardware = self.Hardware.currentText()
        package = self.Package.currentText()
        dies_in_package = []
        for die in self.DiesInDevice.findItems('*', QtCore.Qt.MatchWrap | QtCore.Qt.MatchWildcard):
            dies_in_package.append(die.text())
        definition = {'dies_in_package' : dies_in_package,
                      'is_dual_die' : self.DualDie.checkState(),
                      'pin_names' : {}}
            
        self.parent.project_info.add_device(name, hardware, package, definition)    
        self.parent.tree_update()
        self.accept()

def new_device_dialog(parent):
    newDeviceWizard = NewDeviceWizard(parent)
    newDeviceWizard.exec_()
    del(newDeviceWizard)

if __name__ == '__main__':
    import sys, qdarkstyle
    from ATE.org.actions.dummy_main import DummyMainWindow

    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    dummyMainWindow = DummyMainWindow()
    dialog = NewDeviceWizard(dummyMainWindow)
    dummyMainWindow.register_dialog(dialog)
    sys.exit(app.exec_())
