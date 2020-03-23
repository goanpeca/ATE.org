# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 12:26:00 2020

@author: hoeren
"""
import os
import re

from PyQt5 import QtCore, QtGui, QtWidgets, uic

import qtawesome as qta


class NewStandardTestWizard(QtWidgets.QDialog):

    def __init__(self, parent, fixed=True):
        self.parent = parent
        super().__init__()

        my_ui = __file__.replace('.py', '.ui')
        if not os.path.exists(my_ui):
            raise Exception("can not find %s" % my_ui)
        uic.loadUi(my_ui, self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle(' '.join(re.findall('.[^A-Z]*', os.path.basename(__file__).replace('.py', ''))))

        self.parent = parent

    # ForHardwareSetup ComboBox
        self.existing_hardwaresetups = self.parent.project_info.get_hardwares()
        self.ForHardwareSetup.blockSignals(True)
        self.ForHardwareSetup.clear()
        self.ForHardwareSetup.addItems(self.existing_hardwaresetups)
        self.ForHardwareSetup.setCurrentIndex(self.ForHardwareSetup.findText(self.parent.hw_combo.currentText()))
        self.ForHardwareSetup.setDisabled(fixed)
        self.ForHardwareSetup.blockSignals(False)
        
    # WithBase ComboBox
        self.WithBase.blockSignals(True)
        self.WithBase.clear()
        self.WithBase.addItems(['PR', 'FT'])
        self.WithBase.setCurrentIndex(self.WithBase.findText(self.parent.base_combo.currentText()))
        self.WithBase.setDisabled(fixed)
        self.WithBase.blockSignals(False)

    # StandardTestName ComboBox
        self.model = QtGui.QStandardItemModel()
    
        from ATE.org.actions.new.standard_test import standard_test_names
        self.parent.project_info.
        
        
        existing_standard_test_names = ['IDDq'] #TODO: get the list
        for index, standard_test_name in enumerate(standard_test_names):
            item = QtGui.QStandardItem(standard_test_name)
            if standard_test_name in existing_standard_test_names:
                item.setEnabled(False)
                #TODO: maybe also use the flags (Qt::ItemIsSelectable) ?!?
            else:
                item.setEnabled(True)
                #TODO: maybe also use the flags (Qt::ItemIsSelectable) ?!?
            self.model.appendRow(item)
                
        self.StandardTestName.blockSignals(True)
        self.StandardTestName.clear()
        self.StandardTestName.setModel(self.model)            
        self.StandardTestName.blockSignals(False)



    # buttons
        self.CancelButton.clicked.connect(self.CancelButtonPressed)
        self.OKButton.clicked.connect(self.OKButtonPressed)
        self.OKButton.setEnabled(False)

        self.verify()
        self.show()
        
    def verify(self):
        pass
    
    def CancelButtonPressed(self):
        self.accept()

    def OKButtonPressed(self):
        name = self.TestName.CurrentText()
        hardware = self.ForHardwareSetup.currentText()
        base = self.WithBase.currentText()
        test_data = {'input_parameters' : {},
                     'output_parameters' : {}}

        self.parent.project_info.add_test(name, hardware, base, test_data)        
        self.accept()
    
    
    
def new_standard_test_dialog(parent):
    newStandardTestWizard = NewStandardTestWizard(parent)
    newStandardTestWizard.exec_()
    del(newStandardTestWizard)

if __name__ == '__main__':
    # import sys, qdarkstyle
    # from ATE.org.actions.dummy_main import DummyMainWindow

    # app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    # dummyMainWindow = DummyMainWindow()
    # dialog = NewTestWizard(dummyMainWindow)
    # dummyMainWindow.register_dialog(dialog)
    # sys.exit(app.exec_())
    pass
