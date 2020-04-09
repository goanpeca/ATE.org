# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 09:52:58 2020

@author: hoeren
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from ABC import abc

class ATE_navigator(object):
    
    testerChanged = QtCore.pyqtSignal(str)
    hardwareChanged = QtCore.pyqtSignal(str)
    baseChanged = QtCore.pyqtSignal(str)
    targetChanged = QtCore.pyqtSignal(str)
    
    def __init__(self, project_root):
        self.active_tester = ''
        self.active_hardware = ''
        self.active_base = ''
        self.active_target = ''
        pass
            
    def changeTester(self, tester):
        self.active_tester = tester
        pass
        self.testerChanged.emit(tester)
    
    def changeHardware(self, hardware):
        self.active_hardware = hardware
        pass
        self.hardwareChanged.emit(hardware)
        
    def changeBase(self, base):
        self.active_base = base
        pass
        self.baseChanged.emit(base)
        
    def changeTarget(self, target):
        self.active_target = target
        pass
        self.targetChanged.emit(target)
    
class ATE_toolbar(QtWidgets.QToolBar):
        
    def __init__(self, navigator):
        self.project_info = navigator
        self.project_info.testerChanged.connect(self.changeTester)
        self.project_info.hardwareChanged.connect(self.changeHardware)
        self.project_info.baseChanged.connect(self.changeTester)
        self.project_info.targetChanged.connect(self.changeTarget)
        
    def changeTester(self, tester): 
        if self.project_info.active_tester != tester: # change origniates from the toolbar update the navigator
            self.project_info.changeTester(tester)
        else: # change originates from the navigator (via signal) update the toolbar
            pass
        
    def changeHardware(self, hardware):
        if self.project_info.active_hardware != hardware: # change originates from the toolbar  update the navigator
            self.project_info.changeHardware(hardware)
        else: # change originates from the navigator (via signal) update the toolbar
            pass
    
    def changeBase(self, base):
        if self.project_info.active_base != base: # change originates from the toolbar  update the navigator
            self.project_info.changeBase(base)
        else: # change originates from the navigator (via signal) update the toolbar
            pass
    
    def changeTarget(self, target):
        if self.project_info.active_target != target: # change originates from the toolbar  update the navigator
            self.project_info.changeTarget(target)
        else: # change originates from the navigator (via signal) update the toolbar
            pass

class ATE_tree(object):

    def __init__(self, navigator):
        self.project_info = navigator
        self.project_info.hardwareChanged.connect(self.changeHardware)
        self.project_info.baseChanged.connect(self.changeTester)
        self.project_info.targetChanged.connect(self.changeTarget)

        self.model = QtGui.QStandardItemModel()
    
    def changeHardware(self, hardware):
        if self.project_info.active_hardware != hardware: # change originates from the tree  update the navigator
            self.project_info.changeHardware(hardware)
        else: # change originates from the navigator (via signal) update the tree
            pass
    
    def changeBase(self, base):
        if self.project_info.active_base != base: # change originates from the tree  update the navigator
            self.project_info.changeBase(base)
        else: # change originates from the navigator (via signal) update the tree
            pass
    
    def changeTarget(self, target):
        if self.project_info.active_target != target: # change originates from the tree  update the navigator
            self.project_info.changeTarget(target)
        else: # change originates from the navigator (via signal) update the tree
            pass

class Spyder_Plugin_Manager(object):
    
    def __init__(self):
        pass
    
    @abc.abstractmethod
    def model(self):
        pass

    @abc.abstractmethod
    def toolbar(self):
        pass

class ATE_Plugin_Manager(Spyder_Plugin_Manager):
    
    def __init__(self, project_root):
        self.project_info = ATE_navigator(project_root)
        self.project_tree = ATE_tree(self.project_info)
        self.project_toolbar = ATE_toolbar(self.project_info)

    def model(self):
        return self.project_tree.model
    
    def toolbar(self):
        return self.project_toolbar

class spyder(object):
    
    def openProject(self):
        project_root = 'dialog return'
        project = ATE_Plugin_Manager(project_root)
        project_model = project.model()
        project_toolbar = project.toolbar()
        
if __name__ == '__main__':
    pass

