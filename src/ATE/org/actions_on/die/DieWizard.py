# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 14:32:40 2019

@author: hoeren
"""
import os
import re

from PyQt5 import QtCore, QtGui, QtWidgets, uic

from ATE.org.validation import valid_die_name_regex

class DieWizard(QtWidgets.QDialog):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        my_ui = __file__.replace('.py', '.ui')
        if not os.path.exists(my_ui):
            raise Exception("can not find %s" % my_ui)
        uic.loadUi(my_ui, self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self._setupUI()
        
        
    def _setupUI(self):
        self.setWindowTitle(' '.join(re.findall('.[^A-Z]*', os.path.basename(__file__).replace('.py', ''))))

    # hardware
        self.withHardware.blockSignals(True)
        self.withHardware.clear()
        self.withHardware.addItems(self.parent.project_info.get_hardwares())        
        self.withHardware.setCurrentText(self.parent.active_hardware)
        self.withHardware.setEnabled(True)
        self.withHardware.currentTextChanged.connect(self.hardwareChanged)
        self.withHardware.blockSignals(False)

    # name
        rxDieName = QtCore.QRegExp(valid_die_name_regex)
        DieName_validator = QtGui.QRegExpValidator(rxDieName, self)
        self.dieName.setText("")
        self.dieName.setValidator(DieName_validator)
        self.dieName.textChanged.connect(self.verify)
        self.existing_dies = self.parent.project_info.get_dies()
   
    # maskset    
        self.existing_masksets = sorted([''] + self.parent.project_info.get_masksets())
        self.fromMaskset.blockSignals(True)
        self.fromMaskset.clear()
        self.fromMaskset.addItems(self.existing_masksets)
        self.fromMaskset.setCurrentText('')
        self.fromMaskset.currentTextChanged.connect(self.masksetChanged)
        self.fromMaskset.blockSignals(False)

    # quality
        self.quality.setCurrentText('')

    # product quality
        self.quality.blockSignals(True)
        self.quality.setCurrentText('')
        self.quality.blockSignals(False)

    # grade
        self.isAGrade.blockSignals(True)
        self.isAGrade.setChecked(True)
        self.isAGrade.setEnabled(False)
        self.isAGrade.toggled.connect(self.isAGradeChanged)
        self.isAGrade.blockSignals(False)

        self.referenceGradeLabel.setDisabled(True)
        self.referenceGradeLabel.setHidden(True)
        self.referenceGradeLabel.setVisible(False)

        all_dies = self.parent.project_info.get_dies_info()
        print(all_dies)
        reference_dies = ['']
        referenced_dies = {i : '' for i in ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']}
        free_grades = []

        for die in all_dies:
            if all_dies[die][0] == self.withHardware.currentText() and all_dies[die][1] == self.fromMaskset.currentText():
                if all_dies[die][2] == 'A':
                    reference_dies.append(die)
                else:
                    referenced_dies[all_dies[die]['grade']] = all_dies[die]['grade_reference']

        for die in referenced_dies:
            if referenced_dies[die] == '':
                free_grades.append(die)

        if len(free_grades) == 0: # nothing free anymore
            first_free_grade = ''
        else:
            first_free_grade = sorted(free_grades)[0]

        self.referenceGrade.blockSignals(True)
        self.referenceGrade.clear() 
        self.referenceGrade.addItems(reference_dies)        
        self.referenceGrade.setCurrentText('')
        self.referenceGrade.setDisabled(True)
        self.referenceGrade.setHidden(True)
        self.referenceGrade.setVisible(False)
        self.referenceGrade.currentTextChanged.connect(self.referenceGradeChanged)
        self.referenceGrade.blockSignals(False)

        self.gradeLabel.setDisabled(True)
        self.gradeLabel.setHidden(True)
        self.gradeLabel.setVisible(False)

        self.grade.blockSignals(True)
        self.grade.clear()
        self.grade.addItems(sorted(list(referenced_dies)))
        for index in range(self.grade.count()):
            item_text = self.grade.itemText(index)
            if referenced_dies[item_text] != '':
                self.grade.model().item(index).setEnabled(False)
                self.grade.model().item(index).setToolTip(referenced_dies[item_text])
        self.grade.setCurrentText(first_free_grade)
        self.grade.setDisabled(True)
        self.grade.setHidden(True)
        self.grade.setVisible(False)
        self.grade.currentTextChanged.connect(self.gradeChanged)
        self.grade.blockSignals(False)
    
    # Type & customer
        self.Type.blockSignals(True)
        self.Type.setCurrentText('ASSP')
        self.Type.currentTextChanged.connect(self.typeChanged)
        self.Type.blockSignals(False)

        self.customerLabel.setDisabled(True)
        self.customerLabel.setHidden(True)
        self.customerLabel.setVisible(False)
        
        self.customer.blockSignals(True)
        self.customer.setText('')
        self.customer.textChanged.connect(self.customerChanged)
        self.customer.setDisabled(True)
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
    # name
        self.dieName.blockSignals(True)
        self.dieName.setText("")
        self.dieName.blockSignals(False)


        
        
        
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
            self.isAGrade.setEnabled(False)
        else:
            ASIC_masksets = self.parent.project_info.get_ASIC_masksets()
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
                Customer = self.parent.project_info.get_maskset_customer(SelectedMaskset)
                self.customer.blockSignals(True)
                self.customer.setText(Customer)
                self.customer.setHidden(False)
                self.customer.setDisabled(True)
                self.customer.blockSignals(True)
                self.isAGrade.setEnabled(True)
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
                self.isAGrade.setEnabled(True)
        self.verify()

    def isAGradeChanged(self, isAGrade):
        if isAGrade:
            self.referenceGradeLabel.setDisabled(True)
            self.referenceGradeLabel.setHidden(True)
            self.referenceGradeLabel.setVisible(False)
    
            self.referenceGrade.setDisabled(True)
            self.referenceGrade.setHidden(True)
            self.referenceGrade.setVisible(False)
    
            self.gradeLabel.setDisabled(True)
            self.gradeLabel.setHidden(True)
            self.gradeLabel.setVisible(False)
    
            self.grade.setDisabled(True)
            self.grade.setHidden(True)
            self.grade.setVisible(False)
        else:
            self.referenceGradeLabel.setDisabled(False)
            self.referenceGradeLabel.setHidden(False)
            self.referenceGradeLabel.setVisible(True)
    
            all_dies = self.parent.project_info.get_dies_info()
            reference_dies = ['']
            referenced_dies = {i : '' for i in ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']}
            free_grades = []
    
            for die in all_dies:
                if all_dies[die][0] == self.withHardware.currentText() and all_dies[die][1] == self.fromMaskset.currentText():
                    if all_dies[die][2] == 'A':
                        reference_dies.append(die)
                    else:
                        referenced_dies[all_dies[die]['grade']] = all_dies[die]['grade_reference']
    
            for die in referenced_dies:
                if referenced_dies[die] == '':
                    free_grades.append(die)
    
            if len(free_grades) == 0: # nothing free anymore
                raise Exception("no secondary grades available !!!")
                first_free_grade = ''
            else:
                first_free_grade = sorted(free_grades)[0]
    
            self.referenceGrade.blockSignals(True)
            self.referenceGrade.clear() 
            self.referenceGrade.addItems(reference_dies)        
            self.referenceGrade.setCurrentText('')
            self.referenceGrade.setDisabled(False)
            self.referenceGrade.setHidden(False)
            self.referenceGrade.setVisible(True)
            self.referenceGrade.blockSignals(False)
    
            self.gradeLabel.setDisabled(False)
            self.gradeLabel.setHidden(False)
            self.gradeLabel.setVisible(True)
    
            self.grade.blockSignals(True)
            self.grade.clear()
            self.grade.addItems(sorted(list(referenced_dies)))
            for index in range(self.grade.count()):
                item_text = self.grade.itemText(index)
                if referenced_dies[item_text] != '':
                    self.grade.model().item(index).setEnabled(False)
                    self.grade.model().item(index).setToolTip(referenced_dies[item_text])
            self.grade.setCurrentText(first_free_grade)
            self.grade.setDisabled(False)
            self.grade.setHidden(False)
            self.grade.setVisible(True)
            self.grade.blockSignals(False)

    def referenceGradeChanged(self, SelectedReferenceGrade):
        pass

    def gradeChanged(self, SelectedGrade):
        if SelectedGrade == 'A':
            self.referenceGradeLabel.setHidden(True)
            self.referenceGrade.setHidden(True)
        else:
            self.referenceGradeLabel.setHidden(False)
            self.referenceGrade.setHidden(False)

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
            if not self.isAGrade.isChecked():
                if self.referenceGrade.currentText() == '':
                    self.feedback.setText("A non-A-Grade die needs a reference grade (read: die), select one.")

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
        quality = self.quality.currentText()
        if self.isAGrade.isChecked():
            grade = 'A'
            grade_reference = ''
        else:
            grade = self.grade.currentText()
            grade_reference = self.referenceGrade.currentText()
        if self.Type.currentText() == 'ASIC':
            customer = self.customer.text()
        else: #ASSP
            customer = ''
        
        self.parent.project_info.add_die(name, hardware, maskset, quality, grade, grade_reference, customer)
        
        self.parent.update_tree()
        self.accept()

    def CancelButtonPressed(self):
        self.accept()


class NewDieWizard(DieWizard):
    
    def __init__(self):
        super().__init__()
        self.withHardware.setDisabled(True)
        

class EditDieWizard(DieWizard):
    pass


def new_die_dialog(parent):
    newDieWizard = DieWizard(parent)
    newDieWizard.exec_()
    del(newDieWizard)



if __name__ == "__main__":
    from ATE.org.navigation import project_navigator, run_dummy_main
    
    project_info = project_navigator(r'C:\Users\hoeren\__spyder_workspace__\BROL')
    run_dummy_main(project_info, DieWizard)
