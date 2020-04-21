# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 18:18:33 2020

@author: hoeren
"""
from PyQt5 import QtWidgets

import qtawesome as qta

from ATE.testers import SCT_testers
from ATE.org.navigation import project_navigator


class toolBar(QtWidgets.QToolBar):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.__call__(parent)

    def __call__(self, parent):
        self.parent = parent

        self.clear()

        self.setMovable(False)

        tester_label = QtWidgets.QLabel("Tester:")
        tester_label.setStyleSheet("background-color: rgba(0,0,0,0%)")
        self.addWidget(tester_label)

        self.tester_combo = QtWidgets.QComboBox()
        self.tester_combo.clear()
        self.testers = SCT_testers()
        self.tester_combo.addItems(['']+self.testers.report())
        self.tester_combo.setCurrentText('')
        self.active_tester = ''
        self.tester_combo.currentTextChanged.connect(self.testerChanged)
        self.tester_combo.setEnabled(True)
        self.tester_combo.setVisible(True)
        self.addWidget(self.tester_combo)

        refreshTesters = QtWidgets.QAction(qta.icon('mdi.refresh', color='orange'), "Refresh Testers", self)
        refreshTesters.setStatusTip("Refresh the tester list")
        refreshTesters.triggered.connect(self.rescanTesters)
        refreshTesters.setCheckable(False)
        self.addAction(refreshTesters)

        run_action = QtWidgets.QAction(qta.icon('mdi.play-circle-outline', color='orange'), "Run", self)
        run_action.setStatusTip("Run active module")
        run_action.triggered.connect(self.onRun)
        run_action.setCheckable(False)
        self.addAction(run_action)

        hardware_label = QtWidgets.QLabel("Hardware:")
        hardware_label.setStyleSheet("background-color: rgba(0,0,0,0%)")
        self.addWidget(hardware_label)
    # HARDWARE
        self.hardware_combo = QtWidgets.QComboBox()
        self.hardware_combo.blockSignals(True)
        self.hardware_combo.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.hardware_combo.clear()
        if hasattr(self.parent, 'project_info') and isinstance(self.parent.project_info, project_navigator):
            self.hardware_combo.addItems(self.parent.project_info.get_hardwares())
            self.active_hardware = self.parent.project_info.get_latest_hardware()
            self.hardware_combo.setCurrentText(self.active_hardware)        
        else:
            self.hardware_combo.addItems([''])
            self.active_hardware = ''
            self.hardware_combo.setCurrentText('')
        self.hardware_combo.currentTextChanged.connect(self.hardwareChanged)
        self.hardware_combo.setEnabled(True)
        self.hardware_combo.blockSignals(False)
        self.addWidget(self.hardware_combo)

        base_label = QtWidgets.QLabel("Base:")
        base_label.setStyleSheet("background-color: rgba(0,0,0,0%)")
        self.addWidget(base_label)
    # BASE
        self.base_combo = QtWidgets.QComboBox()
        self.base_combo.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.base_combo.blockSignals(True)
        self.base_combo.clear()
        self.base_combo.addItems(['', 'PR', 'FT'])
        self.active_base = ''
        self.base_combo.setCurrentText(self.active_base)        
        self.base_combo.currentTextChanged.connect(self.baseChanged)
        self.base_combo.setEnabled(True)
        self.base_combo.blockSignals(False)
        self.addWidget(self.base_combo)

        self.target_label = QtWidgets.QLabel("Target:")
        self.target_label.setStyleSheet("background-color: rgba(0,0,0,0%)")
        self.addWidget(self.target_label)
    # TARGET
        self.target_combo = QtWidgets.QComboBox()
        self.target_combo.blockSignals(True)
        self.target_combo.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.target_combo.clear()
        self.target_combo.addItems([''])
        if hasattr(self.parent, 'project_info') and isinstance(self.parent.project_info, project_navigator):
            self.target_combo.addItems(self.parent.project_info.get_devices_for_hardware(self.active_hardware)+
                                       self.parent.project_info.get_dies_for_hardware(self.active_hardware))
        self.active_target = ''
        self.target_combo.setCurrentText(self.active_target)
        self.target_combo.currentTextChanged.connect(self.targetChanged)
        self.target_combo.setEnabled(True)
        self.target_combo.blockSignals(False)
        self.addWidget(self.target_combo)

        info_action = QtWidgets.QAction(qta.icon('mdi.information-outline', color='orange'), "Information", self)
        info_action.setStatusTip("print current information")
        info_action.triggered.connect(self.infoPressed)
        info_action.setCheckable(False)
        self.addAction(info_action)

        settings_action = QtWidgets.QAction(qta.icon('mdi.wrench', color='orange'), "Settings", self)
        settings_action.setStatusTip("Settings")
        settings_action.triggered.connect(self.settingsPressed)
        settings_action.setCheckable(False)
        self.addAction(settings_action)
        
        self.settingsPressed()
        self.show()
        
    def rescanTesters(self):
        self.tester_combo.blockSignals(True)
        self.testers.rescan()
        tester_list = [''] + self.testers.report()
        self.tester_combo.clear()
        self.tester_combo.addItems(tester_list)
        if self.active_tester in tester_list:
            self.tester_combo.setText(self.active_tester)
        else:
            self.tester_combo.setText('')
        self.tester_combo.blockSignals(False)

    def testerChanged(self, selected_tester):
        self.active_tester = selected_tester

    def hardwareChanged(self, selected_hardware):
        self.active_hardware = selected_hardware
        # TODO: do we realy need to blockSignals here ??
        self.target_combo.blockSignals(True)
        if self.active_base == 'FT':
            self.target_combo.clear()
            self.target_combo.addItems([''])
            if hasattr(self.parent, 'project_info') and isinstance(self.parent.project_info, project_navigator):
                self.target_combo.addItems(self.parent.project_info.get_devices_for_hardware(self.active_hardware))
            self.target_combo.setCurrentText('')
            self.active_target = ''
        elif self.active_base == 'PR':
            self.target_combo.clear()
            self.target_combo.addItems([''])
            if hasattr(self.parent, 'project_info') and isinstance(self.parent.project_info, project_navigator):
                self.target_combo.addItems(self.parent.project_info.get_dies_for_hardware(self.active_hardware))            
            self.target_combo.setCurrentText('')
            self.active_target = ''
        else:
            self.target_combo.clear()
            self.target_combo.addItems([''])
            if hasattr(self.parent, 'project_info') and isinstance(self.parent.project_info, project_navigator):
                self.target_combo.addItems(self.parent.project_info.get_devices_for_hardware(self.active_hardware)+
                                           self.parent.project_info.get_dies_for_hardware(self.active_hardware))
            self.target_combo.setCurrentText('')
            self.active_target = ''

        self.target_combo.blockSignals(False)
        self.parent.project_info.set_active_hardware(self.active_hardware)

    def baseChanged(self, selected_base):
        self.active_base = selected_base
        self.hardwareChanged(self.active_hardware)
        self.parent.model.update(self.active_hardware, self.active_base, self.active_target)
        self.parent.project_info.set_active_base(self.active_base)

    def targetChanged(self, selected_target):
        # the fact that we have a target to change to, means that there is a navigator ... no?
        self.active_target = selected_target

        # TODO: remove hack
        self.parent.active_target = selected_target

        if self.active_target in self.parent.project_info.get_devices_for_hardware(self.active_hardware):
            self.base_combo.blockSignals(True)
            self.base_combo.setCurrentText('FT')
            self.base_combo.blockSignals(False)
        elif self.active_target in self.parent.project_info.get_dies_for_hardware(self.active_hardware):
            self.base_combo.blockSignals(True)
            self.base_combo.setCurrentText('PR')
            self.base_combo.blockSignals(False)
        else:
            print(f"woops ... what is '{selected_target}' ? FT or PR ?!?")
        #self.parent.model.update(self.active_hardware, self.active_base, self.active_target)
        self.parent.project_info.set_active_product(self.active_target)
            
    def onRun(self):
        print("run button pressed")

    def infoPressed(self):
        print("info button pressed")

    def settingsPressed(self):
        pass
        # print("settings button pressed")
        # print(f"active tester = '{self.active_tester}'")
        # print(f"active hardware = '{self.active_hardware}'")
        # print(f"active base = '{self.active_base}'")
        # print(f"active target = '{self.active_target}'")
