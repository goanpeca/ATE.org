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

    def __init__(self, project_info, active_hardware, fixed=True):
        self.project_info = project_info
        super().__init__()

        my_ui = __file__.replace('.py', '.ui')
        if not os.path.exists(my_ui):
            raise Exception("can not find %s" % my_ui)
        uic.loadUi(my_ui, self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle(' '.join(re.findall('.[^A-Z]*', os.path.basename(__file__).replace('.py', ''))))


    # hardware
        self.withHardware.blockSignals(True)
        self.withHardware.clear()
        self.withHardware.addItems(self.project_info.get_hardwares())        
        self.withHardware.setCurrentText(active_hardware)
        if fixed:
            self.withHardware.setEnabled(False)
        self.withHardware.currentTextChanged.connect(self.hardwareChanged)
        self.withHardware.blockSignals(False)

    # name
        rxDieName = QtCore.QRegExp(valid_die_name_regex)
        DieName_validator = QtGui.QRegExpValidator(rxDieName, self)
        self.dieName.setText("")
        self.dieName.setValidator(DieName_validator)
        self.dieName.textChanged.connect(self.verify)
        self.existing_dies = self.project_info.get_dies()
   
    # maskset    
        self.existing_masksets = [''] + self.project_info.get_masksets()
        self.fromMaskset.blockSignals(True)
        self.fromMaskset.clear()
        self.fromMaskset.addItems(self.existing_masksets)
        self.fromMaskset.setCurrentIndex(0) # this is the empty string !
        self.fromMaskset.currentTextChanged.connect(self.masksetChanged)
        self.fromMaskset.blockSignals(False)

    # grade
        self.grade.blockSignals(True)
        self.grade.setCurrentText('A')
        self.grade.setDisabled(True)
        self.grade.currentTextChanged.connect(self.gradeChanged)
        self.grade.blockSignals(False)
        
        self.gradeLabel.setDisabled(True)

    # reference grade
        self.referenceGradeLabel.setHidden(True)
        self.referenceGradeLabel.setVisible(False)

        self.referenceGrade.blockSignals(True)
        self.referenceGrade.clear() 
        self.referenceGrade.setHidden(True)
        self.referenceGrade.setVisible(False)
        self.referenceGrade.currentTextChanged.connect(self.referenceGradeChanged)
        self.referenceGrade.blockSignals(False)
    
    # Type & customer
        self.Type.blockSignals(True)
        self.Type.clear()
        self.Type.addItems(['ASSP', 'ASIC'])
        self.Type.setCurrentText('ASSP')
        self.Type.setDisabled(True)
        self.Type.currentTextChanged.connect(self.typeChanged)
        self.Type.blockSignals(False)
        
        self.typeLabel.setDisabled(True)
        
        self.customerLabel.setHidden(True)
        self.customerLabel.setVisible(False)
        
        self.customer.blockSignals(True)
        self.customer.setText('')
        self.customer.textChanged.connect(self.customerChanged)
        self.customer.setHidden(True)
        self.customer.setVisible(False)
        self.customer.blockSignals(False)

    # feedback
        self.feedback.setStyleSheet('color: orange')

    # buttons
        self.CancelButton.clicked.connect(self.CancelButtonPressed)
        self.OKButton.clicked.connect(self.OKButtonPressed)
        self.OKButton.setEnabled(False)

    # go
        self.verify()
        self.show()


    def hardwareChanged(self, hardware):
        pass

    def nameChanged(self, name):
        self.verify()


    def masksetChanged(self, SelectedMaskset):
        print(f"masksetChanged --> {SelectedMaskset}")
        if SelectedMaskset=='':
            self.gradeLabel.setDisabled(True)
            self.grade.blockSignals(True)
            self.grade.setCurrentText('A')
            self.grade.setDisabled(True)
            self.grade.blockSignals(False)
            self.typeLabel.setDisabled(True)
            self.Type.blockSignals(True)
            self.Type.setCurrentText('ASSP')
            self.Type.setDisabled(True)
            self.Type.blockSignals(False)
            self.customerLabel.setHidden(True)
            self.customer.blockSignals(True)
            self.customer.setText('')
            self.customer.setHidden(True)
            self.customer.blockSignals(True)
        else:
            ASIC_masksets = self.project_info.get_ASIC_masksets()
            if SelectedMaskset in ASIC_masksets:
                print("ASIC")
                self.gradeLabel.setDisabled(False)
                self.grade.blockSignals(True)
                self.grade.setCurrentText('A')
                self.grade.setDisabled(False)
                self.grade.blockSignals(False)
                self.typeLabel.setDisabled(True)
                self.Type.blockSignals(True)
                self.Type.setCurrentText('ASIC')
                self.Type.setDisabled(True)
                self.Type.blockSignals(False)
                self.customerLabel.setHidden(False)
                self.customerLabel.setDisabled(True)
                Customer = self.project_info.get_maskset_customer(SelectedMaskset)
                self.customer.blockSignals(True)
                self.customer.setText(Customer)
                self.customer.setHidden(False)
                self.customer.setDisabled(True)
                self.customer.blockSignals(True)
            else:
                print("ASSP")
                self.gradeLabel.setDisabled(False)
                self.grade.blockSignals(True)
                self.grade.setCurrentText('A')
                self.grade.setDisabled(False)
                self.grade.blockSignals(False)
                self.typeLabel.setDisabled(False)
                self.Type.blockSignals(True)
                self.Type.setCurrentText('ASSP')
                self.Type.setDisabled(False)
                self.Type.blockSignals(False)
                self.customerLabel.setHidden(True)
                self.customer.blockSignals(True)
                self.customer.setText('')
                self.customer.setHidden(True)
                self.customer.blockSignals(True)
        self.verify()

    def gradeChanged(self, SelectedGrade):
        if SelectedGrade == 'A':
            self.referenceGradeLabel.setHidden(True)
            self.referenceGrade.setHidden(True)
        else:
            self.referenceGradeLabel.setHidden(False)
            self.referenceGrade.setHidden(False)

    def referenceGradeChanged(self, SelectedReferenceGrade):
        pass

    def typeChanged(self, SelectedType):
        '''
        if the Type is 'ASIC' enable CustomerLabel and Customer
        '''
        if SelectedType == 'ASIC':
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

    def customerChanged(self, Customer):
        pass

    def verify(self):
        self.feedback.setText("")

    # Die Name        
        if self.dieName.text() == '':
            self.feedback.setText("Supply a Die Name")
        elif self.dieName.text() in self.existing_dies:
            self.feedback.setText("Die name already exists !")
    
    # Maskset
        if self.feedback.text() == '':
            if self.fromMaskset.currentText() == "":
                self.feedback.setText("No maskset selected")

    # Grade & reference grade
        if self.feedback.text() == '':
            if self.grade.currentText() != 'A' and self.referenceGrade.currentTet() == '':
                self.feedback.setText("A '{self.grade.currentText()}' grade Die needs an 'A' grade reference")
    
    # Type & customer
        if self.feedback.text() == '':
            if self.Type.currentText() == "ASIC" and self.customer.text() == "":
                self.feedback.setText("need a customer name for the ASIC")

    # Buttons
        if self.feedback.text() == '':
            self.OKButton.setEnabled(True)
        else:
            self.OKButton.setEnabled(False)

    def OKButtonPressed(self):
        hardware = self.withHardware.currentText()
        name = self.dieName.text()
        maskset = self.fromMaskset.currentText()
        grade = self.grade.currentText()
        if grade == 'A':
            grade_reference = ''
        else:
            grade_reference = self.referenceGrade.currentText()
        if self.Type.currentText() == 'ASIC':
            customer = self.customer.text()
        else: #ASSP
            customer = ''
        
        # TODO: quality need to be defined
        quality = ''

        self.project_info.add_die(name, hardware, maskset, quality, grade, grade_reference, customer)
        
        self.accept()

    def CancelButtonPressed(self):
        self.accept()

def new_die_dialog(project_info, active_hardware):
    newDieWizard = NewDieWizard(project_info, active_hardware)
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
