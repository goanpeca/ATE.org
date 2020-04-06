# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 09:52:27 2020

@author: hoeren
"""

import os
import re

from PyQt5 import QtCore, QtGui, QtWidgets, uic

import qtawesome as qta

from ATE.org.validation import valid_pcb_name_regex

class HardwareWizard(QtWidgets.QDialog):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self._load_ui()
        self._setup()
        self._connect_event_handler()

    def _load_ui(self):
        ui = '.'.join(os.path.realpath(__file__).split('.')[:-1]) + '.ui'
        if not os.path.exists(ui):
            raise Exception("can not find %s" % ui)
        uic.loadUi(ui, self)
        self.setWindowTitle(' '.join(re.findall('.[^A-Z]*', os.path.basename(__file__).replace('.py', ''))))

    def _setup(self):

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)

    # hardware
        self.hardware.setText(self.parent.project_info.get_next_hardware())
        self.hardware.setEnabled(False)

    # PCBs
        rxPCBName = QtCore.QRegExp(valid_pcb_name_regex)
        PCBName_validator = QtGui.QRegExpValidator(rxPCBName, self)
        self.probecardsLinked = False
        if self.probecardsLinked:
            self.probecardLink.setIcon(qta.icon('mdi.link', color='orange'))
        else:
            self.probecardLink.setIcon(qta.icon('mdi.link-off', color='orange'))
        self.probecardLink.setDisabled(True) #TODO: try to skip the 'True'

        self.singlesiteLoadboard.setText('')
        self.singlesiteLoadboard.setValidator(PCBName_validator)
        self.singlesiteLoadboard.setEnabled(True)
        self.multisiteLoadboard.setText('')
        self.multisiteLoadboard.setValidator(PCBName_validator)
        self.multisiteLoadboard.setDisabled(True)
        self.singlesiteProbecard.setText('')
        self.singlesiteProbecard.setValidator(PCBName_validator)
        self.singlesiteProbecard.setEnabled(True)
        self.multisiteProbecard.setText('')
        self.multisiteProbecard.setValidator(PCBName_validator)
        self.multisiteProbecard.setDisabled(True)
        self.singlesiteDIB.setText('')
        self.singlesiteDIB.setValidator(PCBName_validator)
        self.singlesiteDIB.setEnabled(True)
        self.multisiteDIB.setText('')
        self.multisiteDIB.setValidator(PCBName_validator)
        self.multisiteDIB.setDisabled(True)
        
        self.maxParallelism.setCurrentText('1')
        
    # Instruments
        self.tester.clear()
        self.tester.addItems(['']+self.parent.project_info.get_available_testers())
        self.tester.setCurrentText('')
        
        # self.availableInstruments.clear()
        # self.availableInstruments.addItems([''])
        #self.parent.project_info.get_available_instruments())
        #TODO: move from list to tree for this widget!
    
        self.collapse.setIcon(qta.icon('mdi.unfold-less-horizontal', color='orange'))
    
        self.expand.setIcon(qta.icon('mdi.unfold-more-horizontal', color='orange'))
    
        self.addInstrument.setIcon(qta.icon('mdi.arrow-right-bold', color='orange'))
    
        self.removeInstrument.setIcon(qta.icon('mdi.arrow-left-bold', color='orange'))
    
        # self.usedInstruments.clear()
        #TODO: move from list to tree for this widget!
    
    # Actuator
        #TODO: initialize this section
    
        self.addActuator.setIcon(qta.icon('mdi.arrow-right-bold', color='orange'))
        
        self.removeActuator.setIcon(qta.icon('mdi.arrow-left-bold', color='orange'))
    
    # Parallelism in Probing
        #TODO: initialize this section
        
    # Parallelism in Final Test
        #TODO: initialize this section
        
    # general    
        self.feedback.setText('')
        self.feedback.setStyleSheet('color: orange')

        self.OKButton.setEnabled(False)
        self.CancelButton.setEnabled(True)

    def _connect_event_handler(self):

    # PCBs
        self.singlesiteLoadboard.textChanged.connect(self.singlesiteLoadboarChanged)
        self.singlesiteProbecard.textChanged.connect(self.singlesiteProbecardChanged)
        self.singlesiteDIB.textChanged.connect(self.singlesiteDIBChanged)
        self.maxParallelism.currentTextChanged.connect(self.maxParallelismChanged)
        self.multisiteLoadboard.textChanged.connect(self.multisiteLoadboardChanged)
        self.multisiteProbecard.textChanged.connect(self.multisiteProbecardChanged)
        self.multisiteDIB.textChanged.connect(self.multisiteDIBChanged)
        self.probecardLink.triggered.connect(self.probecardLinkToggled)
    # Instruments
        self.tester.currentTextChanged.connect(self.testerChanged)
        self.collapse.clicked.connect(self.collapseAvailableInstruments)
        self.expand.clicked.connect(self.expandAvailableInstruments)
        self.addInstrument.clicked.connect(self.addingInstrument)
        self.removeInstrument.clicked.connect(self.removingInstrument)
        self.checkInstruments.clicked.connect(self.checkInstrumentUsage)
        self.availableInstruments.itemSelectionChanged.connect(self.availableInstrumentsSelectionChanged)
        self.usedInstruments.itemSelectionChanged.connect(self.usedInstrumentsSelectionChanged)
        
    # Actuator
        # self.availableActuator.
        self.addActuator.clicked.connect(self.addingActuator)
        self.removeActuator.clicked.connect(self.removingActuator)
        self.checkActuators.clicked.connect(self.checkActuatorUsage)
        self.availableActuators.itemSelectionChanged.connect(self.availableActuatorSelectionChanged)
        self.usedActuators.itemSelectionChanged.connect(self.usedActuatorSelectionChanged)
    
    # Parallelism
    
    # general
        self.CancelButton.clicked.connect(self.CancelButtonPressed)
        self.OKButton.clicked.connect(self.OKButtonPressed)

# PCBs
    def singlesiteLoadboarChanged(self, new_single_site_loadboard):
        print(f"singlesiteLoadboardChanged to '{new_single_site_loadboard}'")

    def singlesiteProbecardChanged(self, new_single_site_probecard):
        print(f"singlesiteProbecardChanged to '{new_single_site_probecard}'")
    
    def singlesiteDIBChanged(self, new_single_site_DIB):
        print(f"singlesiteDIBChanged to '{new_single_site_DIB}'")

    def maxParallelismChanged(self, selected_parallelism):
        print(f"maxParallelismChanged to '{selected_parallelism}'")

    def multisiteLoadboardChanged(self, new_multi_site_loadboard):
        print(f"multisiteLoadboardChanged to '{new_multi_site_loadboard}'")

    def multisiteProbecardChanged(self, new_multi_site_probecard):
        print(f"multisiteProbecardChanged to '{new_multi_site_probecard}'")

    def multisiteDIBChanged(self, new_multi_site_DIB):
        print(f"multisiteDIBChanged to '{new_multi_site_DIB}'")

    def probecardLinkToggled(self):
        print(f"probecardLinkToggled to '{self.probecardsLinked}'")


# instruments
    def testerChanged(self, new_tester):
        print(f"testerChanged to '{new_tester}'")
        
    def availableInstrumentsSelectionChanged(self):
        print("available Instruments selection changed")

    def addingInstrument(self):
        print("adding instrument")
        
    def removingInstrument(self):
        print("removing instrument")

    def checkInstrumentUsage(self):
        print("check Instrument Usage")

    def usedInstrumentsSelectionChanged(self):
        print("used instruments selection changed")
    
# Actuator
    def availableActuatorSelectionChanged(self):
        print("available Actuator selection changed")

    def collapseAvailableInstruments(self):
        print("collapse available Instruments")

    def expandAvailableInstruments(self):
        print("exapnding available Instruments")

    def addingActuator(self):
        print("adding Actuator")
        
    def removingActuator(self):
        print("removing Actuator")
        
    def checkActuatorUsage(self):
        print("check Actuator Usage")

    def usedActuatorSelectionChanged(self):
        print("used Actuator selection changed")

# Parallelism    




# General
    def CancelButtonPressed(self):
        self.accept()

    def OKButtonPressed(self):
        name = self.hardware.text()
        new_name = self.project_info.add_hardware(self._get_actual_definition())
        if name != new_name:
            raise Exception(f"Woops, something wrong with the name !!! '{name}'<->'{new_name}'")

        self.accept()

    def verify(self):
        self.feedback.setText('')
        
        #TODO: implement a bit more verification
        
        
        
        if self.Feedback.text()=='':
            self.OKButton.setEnabled(True)


if __name__ == '__main__':
    from ATE.org.navigation import project_navigator, run_dummy_main
    
    project_info = project_navigator(r'C:\Users\hoeren\__spyder_workspace__\CTCA')
    run_dummy_main(project_info, HardwareWizard)

