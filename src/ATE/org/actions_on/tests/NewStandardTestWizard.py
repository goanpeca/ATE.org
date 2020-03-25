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
        self.ForHardwareSetup.currentTextChanged.connect(self.verify)
        self.ForHardwareSetup.blockSignals(False)
        
    # WithBase ComboBox
        self.WithBase.blockSignals(True)
        self.WithBase.clear()
        self.WithBase.addItems(['PR', 'FT'])
        self.WithBase.setCurrentIndex(self.WithBase.findText(self.parent.base_combo.currentText()))
        self.WithBase.setDisabled(fixed)
        self.WithBase.currentTextChanged.connect(self.verify)
        self.WithBase.blockSignals(False)

    # StandardTestName ComboBox
        self.model = QtGui.QStandardItemModel()
    
        from ATE.org.actions_on.tests import standard_test_names
        existing_standard_test_names = \
            self.parent.project_info.tests_get_standard_tests(
                self.ForHardwareSetup.currentText(),
                self.WithBase.currentText())

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
        self.StandardTestName.currentTextChanged.connect(self.verify)            
        self.StandardTestName.blockSignals(False)

    # feedback
        self.feedback.setText("")
        self.feedback.setStyleSheet('color: orange')

    # buttons
        self.CancelButton.clicked.connect(self.CancelButtonPressed)
        self.OKButton.clicked.connect(self.OKButtonPressed)
        self.OKButton.setEnabled(False)

    # go
        self.verify()
        self.show()
        
        
    def verify(self):
        self.feedback.setText('')
        
        # hardware        
        if self.feedback.text() == '':
            if self.ForHardwareSetup.currentText()=='':
                self.feedback.setText("Select a hardware setup")

        # base        
        if self.feedback.text() == '':
            if self.WithBase.currentText() not in ['FT', 'PR']:
                self.feedback.setText("Select the base")

        # standard test        
        if self.feedback.text() == '':
            if self.StandardTestName.currentText() == '':
                self.feedback.setText("Select a standard test")

        # buttons
        if self.feedback.text() == "":
            self.OKButton.setEnabled(True)
        else:
            self.OKButton.setEnabled(False)


    def CancelButtonPressed(self):
        self.accept()

    def OKButtonPressed(self):
        name = self.StandardTestName.currentText()
        hardware = self.ForHardwareSetup.currentText()
        Type = 'standard'
        base = self.WithBase.currentText()
        definition = {'doc_string' : [], #list of lines
                      'input_parameters' : {},
                      'output_parameters' : {}}

        self.parent.project_info.test_add(name, hardware, Type, base, definition)        
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
