# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 14:32:40 2019

@author: hoeren
"""
import os
import re

from PyQt5 import QtCore, QtGui, QtWidgets, uic

from ATE.org.validation import valid_die_name_regex

class NewDieWizard(QtWidgets.QDialog):

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

        self.withHardware.blockSignals(True)
        self.withHardware.clear()
        self.withHardware.addItems(self.parent.project_info.get_hardwares())        
        self.withHardware.setCurrentText(self.parent.active_hw)
        if fixed:
            self.withHardware.setEnabled(False)
        self.withHardware.currentTextChanged.connect(self.hardwareChanged)
        self.withHardware.blockSignals(False)

        rxDieName = QtCore.QRegExp(valid_die_name_regex)
        DieName_validator = QtGui.QRegExpValidator(rxDieName, self)
        self.dieName.setText("")
        self.dieName.setValidator(DieName_validator)
        self.dieName.textChanged.connect(self.verify)
        self.existing_dies = self.parent.project_info.get_dies()
        
        self.Type.blockSignals(True)
        self.Type.setCurrentText('ASSP')
        self.Type.currentTextChanged.connect(self.typeChanged)
        self.Type.blockSignals(False)
        
        self.customerLabel.setVisible(False)
        
        self.customer.blockSignals(True)
        self.customer.setCurrentText('')
        self.customer.currentTextChanged.connect(self.customerChanged)
        self.customer.setVisible(False)
        self.customer.blockSignals(False)
        
        
        
        
        self.existing_masksets = [''] + self.parent.project_info.get_masksets()
        self.fromMaskset.blockSignals(True)
        self.fromMaskset.clear()
        self.fromMaskset.addItems(self.existing_masksets)
        self.fromMaskset.setCurrentIndex(0) # this is the empty string !
        self.fromMaskset.currentTextChanged.connect(self.masksetChanged)
        self.fromMaskset.blockSignals(False)

        self.grade.blockSignals(True)
        self.grade.setCurrentText('A')
        self.grade.setVisible(False)
        self.grade.currentTextChanged.connect(self.gradeChanged)
        self.grade.blockSignals(False)

        self.referenceGrade.blockSignals(True)
        
        
        
        
        self.referenceGrade.setVisible(False)
        self.referenceGrade.currentTextChanged.connect(self.referenceGradeChanged)
        self.referenceGrade.blockSignals(False)

        self.Type.blockSignals(True)
        self.Type.clear()
        self.Type.addItems(['ASSP', 'ASIC'])
        self.Type.setCurrentIndex(0) # --> ASSP
        self.Type.currentIndexChanged.connect(self.type_changed)
        self.Type.blockSignals(False)
        
        self.customerLabel.setDisabled(True)
        self.customerLabel.setHidden(True)
        self.customerLabel.setVisible(False)
        
        self.customer.blockSignals(True)
        self.customer.setText("")
        self.customer.setDisabled(True)
        self.customer.setHidden(True)
        self.customer.setVisible(False)
        self.customer.blockSignals(False)
        
        self.feedback.setText("No die name")
        self.feedback.setStyleSheet('color: orange')

        self.CancelButton.clicked.connect(self.CancelButtonPressed)
        self.OKButton.clicked.connect(self.OKButtonPressed)
        self.OKButton.setEnabled(False)

        self.verify()
        self.show()

    def nameChanged(self, name):
        pass


    def masksetChanged(self, SelectedMaskset):
        pass

    def gradeChanged(self, SelectedGrade):
        if SelectedGrade != 'A':
            self.referenceGradeLabel.setVisible(False)
            self.referenceGrade.setVisible(False)
        else:
            self.referenceGradeLabel.setVisible(False)
            self.referenceGrade.setVisible(False)

    def referenceGradeChanged(self, SelectedReferenceGrade):
        pass

    def typeChanged(self):
        '''
        if the Type is 'ASIC' enable CustomerLabel and Customer
        '''
        if self.Type.currentText() == 'ASIC':
            self.customerLabel.setDisabled(False)
            self.customerLabel.setHidden(False)
            self.customerLabel.setVisible(True)
            
            self.customer.blockSignals(True)
            self.customer.setText("")
            self.customer.setDisabled(False)
            self.customer.setHidden(False)
            self.customer.setVisible(True)
            self.customer.blockSignals(False)
        else:
            self.customerLabel.setDisabled(True)
            self.customerLabel.setHidden(True)
            self.customerLabel.setVisible(False)
            
            self.customer.blockSignals(True)
            self.customer.setText("")
            self.customer.setDisabled(True)
            self.customer.setHidden(True)
            self.customer.setVisible(False)
            self.customer.blockSignals(False)

    def verify(self):
        if self.dieName.text() in self.existing_dies:
            self.feedback.setText("Die name already exists !")
            self.OKButton.setEnabled(False)
        else:
            if self.fromMaskset.currentText() == "":
                self.feedback.setText("No maskset selected")
                self.OKButton.setEnabled(False)
            else:
                if self.Type.currentText() == "ASIC":
                    if self.Customer.text() == "":
                        self.feedback.setText("need a customer for ASIC")
                        self.OKButton.setEnabled(False)
                    else: # ASSP
                        self.feedback.setText("")
                        self.OKButton.setEnabled(True)
                else: # ASSP
                    self.feedback.setText("")
                    self.OKButton.setEnabled(True)

    def CancelButtonPressed(self):
        self.accept()

    def OKButtonPressed(self):
        name = self.NewDieName.text()
        maskset = self.FromMaskset.currentText()
        hardware = self.WithHardware.currentText()
        if self.Type.currentText() == 'ASIC':
            customer = 'ASIC'
        else: #ASSP
            customer = self.Customer.text()
        
        self.parent.project_info.add_die(name, hardware, maskset, customer)
        self.parent.update_tree()
        self.accept()

def new_die_dialog(parent):
    newDieWizard = NewDieWizard(parent)
    newDieWizard.exec_()
    del(newDieWizard)

if __name__ == '__main__':
    import sys, qdarkstyle
    from ATE.org.actions.dummy_main import DummyMainWindow

    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    dummyMainWindow = DummyMainWindow()
    dialog = NewDieWizard(dummyMainWindow)
    dummyMainWindow.register_dialog(dialog)
    sys.exit(app.exec_())
