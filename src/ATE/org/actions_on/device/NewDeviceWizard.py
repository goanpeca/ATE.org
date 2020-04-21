# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 15:09:41 2019

@author: hoeren
"""
import os
import pickle
import re

from PyQt5 import QtCore, QtGui, QtWidgets, uic

import qtawesome as qta

from ATE.org.validation import valid_device_name_regex

class NewDeviceWizard(QtWidgets.QDialog):
    def __init__(self, project_info, active_hardware):
        self.project_info = project_info
        super().__init__()

        my_ui = __file__.replace('.py', '.ui')
        if not os.path.exists(my_ui):
            raise Exception("can not find %s" % my_ui)
        uic.loadUi(my_ui, self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle(' '.join(re.findall('.[^A-Z]*', os.path.basename(__file__).replace('.py', ''))))

    # hardware
        self.existing_hardwares = self.project_info.get_hardwares()
        self.hardware.blockSignals(True)
        self.hardware.clear()
        self.hardware.addItems(self.existing_hardwares)
        self.hardware.setCurrentText(active_hardware)

        # if fixed:
        #     self.hardware.setEnabled(False)

        self.hardware.currentTextChanged.connect(self.hardwareChanged)
        self.hardware.blockSignals(False)        

    # name
        rxDeviceName = QtCore.QRegExp(valid_device_name_regex)
        DeviceName_validator = QtGui.QRegExpValidator(rxDeviceName, self)
        self.deviceName.blockSignals(True)
        self.deviceName.setValidator(DeviceName_validator)
        self.deviceName.setText('')
        self.deviceName.textChanged.connect(self.verify)
        self.deviceName.blockSignals(False)
        self.existing_devices = self.project_info.get_devices_for_hardware(self.hardware.currentText())
    
    # packages
        self.existing_packages = self.project_info.packages_get()
        self.package.blockSignals(True)
        self.package.clear()
        self.package.addItems([''] + self.existing_packages + ['Naked Die'])
        self.package.setCurrentIndex(0) # this is the empty string !
        self.package.currentTextChanged.connect(self.packageChanged)
        self.package.blockSignals(False)

    # Dies/Pins
        if self.hardware.currentText()=='':
            self.tabWidget.setEnabled(False)
            self.available_dies = []
        else:
            self.tabWidget.setEnabled(True)
            self.pins.setEnabled(False)
            self.available_dies = self.project_info.get_dies_for_hardware(self.hardware.currentText())
        self.dies_in_device = []
        
    # available dies
        self.availableDies.blockSignals(True)
        self.availableDies.clear()
        self.availableDies.clearSelection()
        self.availableDies.addItems(self.available_dies)
        self.availableDies.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.availableDies.blockSignals(False)

    # dies in device    
        self.diesInDevice.blockSignals(True)
        self.diesInDevice.clear()
        self.diesInDevice.clearSelection()
        self.diesInDevice.addItems(self.dies_in_device)
        self.diesInDevice.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.diesInDevice.blockSignals(False)

    # add die(s) to device
        self.addDie.blockSignals(True)
        self.addDie.setEnabled(True)
        self.addDie.setIcon(qta.icon('mdi.arrow-right-bold-outline', color='orange'))
        self.addDie.clicked.connect(self.add_dies)
        self.addDie.blockSignals(False)

    # remove die(s) from device
        self.removeDie.blockSignals(True)
        self.removeDie.setEnabled(True)
        self.removeDie.setIcon(qta.icon('mdi.arrow-left-bold-outline', color='orange'))
        self.removeDie.clicked.connect(self.remove_dies)
        self.removeDie.blockSignals(False)

    # Type
        #TODO: also add the Type = ['ASSP' or 'ASIC']

    # feedback
        self.feedback.setStyleSheet('color: orange')

    # buttons
        self.CancelButton.clicked.connect(self.CancelButtonPressed)
        self.OKButton.clicked.connect(self.OKButtonPressed)
        self.OKButton.setDisabled(True)

    # go
        self.verify()
        self.show()

    def hardwareChanged(self, SelectedHardware):
        '''
        if the selected hardware changes, make sure the active_hardware 
        at the parent level is also changed, the dies in device list is cleared,
        and the available dies is reloaded.
        '''
        # TODO: must be done elsewhere
        # self.parent.active_hardware = self.hardware.currentText()

        self.diesInDevice.clear()
        self.existing_dies = self.project_info.get_dies_for_hardware(self.project_info.active_hardware)
        self.availableDies.blockSignals(True)
        self.availableDies.clear()
        self.availableDies.addItems(self.existing_dies)
        self.availableDies.clearSelection()
        self.availableDies.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.availableDies.blockSignals(False)
    
    def nameChanged(self, DeviceName):
        pass
    
    def packageChanged(self, Package):
        if self.package.currentText()=='': # no package
            self.pins.setVisible(False)
        elif self.package.currentText()=='Naked Die': # naked die
            self.pins.setVisible(True)
            self.diesInDevice.clear()
            self.pinsTable.setRowCount(0)
        else: # normal package
            self.pins.setVisible(True)
            packages_info = self.project_info.packages_get_info()
            pins_in_package = packages_info[self.package.currentText()]
            self.pinsTable.setRowCount(pins_in_package)
    
    def check_for_dual_die(self):
        '''
        this mentod will check if a configuration qualifies for 'DualDie',
        if so, the radio will be enabled, if not disabled (and cleared)
        '''
        temp = []
        for die in self.diesInDevice.findItems('*', QtCore.Qt.MatchWrap | QtCore.Qt.MatchWildcard):
            temp.append(die.text())
        if len(temp)==2:
            self.dualDie.setCheckState(QtCore.Qt.Unchecked)
            if temp[0] == temp[1]:
                self.dualDie.setEnabled(True)
            else:
                self.dualDie.setEnabled(False)
        else:
            self.dualDie.setCheckState(QtCore.Qt.Unchecked)
            self.dualDie.setEnabled(False)
    
    def verify(self):
        self.feedback.setText('')

    # Check hardware
        if self.feedback.text()=='':
            if self.hardware.currentText()=='':
                self.feedback.setText("Select a hardware setup")

    # Check Device Name
        if self.feedback.text()=='':
            if self.deviceName.text()=='':
                self.feedback.setText("Supply a Device Name")
            elif self.deviceName.text() in self.existing_devices:
                self.feedback.setText(f"Device '{self.deviceName.text()}' already defined!")

    # Check Package
        if self.feedback.text()=='':
            if self.package.currentText()=='':
                self.feedback.setText("Select a Package")
    
    # Check Dies
    
    # Check Pins
    
    # Check Type

                
        if self.feedback.text()=='':
            package_name = self.package.currentText()
            if package_name == '':
                feedback = "No package selected"
            elif package_name != 'Naked Die':
                number_of_dies_in_device = self.diesInDevice.count()
                if not self.dualDie.checkState(): # no dual die
                    if number_of_dies_in_device == 0:
                        self.feedback.setText('Need at least ONE die')
            else: # Naked die
                number_of_dies_in_device = self.diesInDevice.count()
                if number_of_dies_in_device == 0:
                    self.feedback.setText("select the naked die")
                elif number_of_dies_in_device > 1:
                    self.feedback.setText("Only one die allowed in 'Naked Die'")
                else: # one selected
                    self.feedback.setText('')



    # Check the pins table
        if self.feedback.text()=='':
            pass


        if self.feedback.text() == "":
            self.OKButton.setEnabled(True)
        else:
            self.OKButton.setEnabled(False)

    def add_dies(self):
        '''
        this method is called when the 'add die' (tool)button is pressed
        '''
        if self.dualDie.isChecked(): 
            pass
        
        
        
        self.diesInDevice.blockSignals(True)
        for die_to_add in self.availableDies.selectedItems():
            self.diesInDevice.insertItem(self.diesInDevice.count(), die_to_add.text())
        self.diesInDevice.clearSelection()
        self.availableDies.clearSelection()
        self.diesInDevice.blockSignals(False)
        
        
        
        
        self.check_for_dual_die()
        self.verify()
        
    def remove_dies(self):
        '''
        this method is called when the 'remove die' (tool)button is pressed
        '''
        self.diesInDevice.blockSignals(True)
        self.diesInDevice.takeItem(self.diesInDevice.selectedIndexes()[0].row()) # DiesInDevice set to SingleSelection ;-)
        self.diesInDevice.clearSelection()
        self.availableDies.clearSelection()
        self.diesInDevice.blockSignals(False)
        self.check_for_dual_die()
        self.verify()
        
    def CancelButtonPressed(self):
        self.accept()

    def OKButtonPressed(self):
        hardware = self.hardware.currentText()
        name = self.deviceName.text()
        package = self.package.currentText()
        dies_in_package = []
        for die in self.diesInDevice.findItems('*', QtCore.Qt.MatchWrap | QtCore.Qt.MatchWildcard):
            dies_in_package.append(die.text())
        definition = {'dies_in_package' : dies_in_package,
                      'is_dual_die' : self.dualDie.checkState(),
                      'pin_names' : {}}
            
        self.project_info.add_device(name, hardware, package, definition)    
        self.accept()

def new_device_dialog(project_info, active_hardware):
    newDeviceWizard = NewDeviceWizard(project_info, active_hardware)
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
