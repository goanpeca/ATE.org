# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 18:56:05 2019

@author: hoeren
"""
import os
import re

from ATE.org.validation import is_valid_test_name

from PyQt5 import QtCore, QtGui, QtWidgets, uic

import qdarkstyle
import qtawesome as qta

class NewTestWizard(QtWidgets.QDialog):

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

        self.existing_hardwaresetups = self.parent.project_info.get_hardwares()
        self.ForHardwareSetup.blockSignals(True)
        self.ForHardwareSetup.clear()
        self.ForHardwareSetup.addItems(self.existing_hardwaresetups)
        self.ForHardwareSetup.setCurrentIndex(self.ForHardwareSetup.findText(self.parent.hw_combo.currentText()))
        self.ForHardwareSetup.blockSignals(False)
        
        self.WithBase.blockSignals(True)
        self.WithBase.clear()
        self.WithBase.addItems(['PR', 'FT'])
        self.WithBase.setCurrentIndex(self.WithBase.findText(self.parent.base_combo.currentText()))
        self.WithBase.blockSignals(False)

        from ATE.org.validation import valid_test_name_regex
        rxTestName = QtCore.QRegExp(valid_test_name_regex)
        TestName_validator = QtGui.QRegExpValidator(rxTestName, self)

        self.TestName.setText("")
        self.TestName.setValidator(TestName_validator)
        self.TestName.textChanged.connect(self.verify)

        self.Feedback.setStyleSheet('color: orange')

    # unitContextMenu --> reference = https://en.wikipedia.org/wiki/International_System_of_Units
        units = [# SI base units
                 's (time - second)',
                 'm (length - meter',
                 'kg (mass - kilogram)',
                 'A (electric current - ampères)',
                 'K (temperature - Kelvin)',
                 'mol (amount of substance - mole)',
                 'cd (luminous intensity - candela)',
                 # SI derived units
                 'rad (plane angle - radian = m/m)',
                 'sr (solid angle - steradian = m²/m²)',
                 'Hz (frequency - hertz = s⁻¹)',
                 'N (force, weight - newton = kg⋅m⋅s⁻²)',
                 'Pa ( pressure, stress - pascal = kg⋅m⁻¹⋅s⁻²)',
                 'J (energy, work, heat - joule = kg⋅m²⋅s⁻² = N⋅m = Pa⋅m³)',
                 'W (power, radiant flux - watt = kg⋅m²⋅s⁻³ = J/s)',
                 'C (electric charge - coulomb = s⋅A)',
                 'V (electric potential, emf - volt = kg⋅m²⋅s⁻³⋅A⁻¹ = W/A = J/C)',
                 'F (electric capacitance - farad = kg⁻¹⋅m⁻²⋅s⁴⋅A² = C/V)',
                 'Ω (electric resistance, impedance, reactance - ohm = kg⋅m²⋅s⁻³⋅A⁻² = V/A)',
                 'S (electric conductance - siemens = kg⁻¹⋅m⁻²⋅s³⋅A² = Ω⁻¹)',
                 'Wb (magnetic flux - weber = kg⋅m²⋅s⁻²⋅A⁻¹ = V⋅s)',
                 'T (magnetic flux density - tesla = kg⋅s⁻²⋅A⁻¹ = Wb/m²)',
                 'H (electric inductance - henry = kg⋅m²⋅s⁻²⋅A⁻² = Wb/A)',
                 'lm (luminous flux - lumen = cd⋅sr)',
                 'lx (illuminance - lux = m⁻²⋅cd = lm/m²)',
                 'Bq (radioactivity - Becquerel = s⁻¹)',
                 'Gy (absorbed dose - gray = m²⋅s⁻² = J/kg)',
                 'Sv (equivalent dose - sievert = m²⋅s⁻² = J/kg)',
                 'kat (catalytic activity - katal = mol⋅s⁻¹)',
                 # Alternatives
                 '°C (temperature - degree Celcius = K - 273.15)',
                 'Gs (magnetic flux density - gauss = 10⁻⁴ Tesla)',
                 '𝓡 (unitless real number)', 
                 '№ (unitless integer number)',
                 'Custom']
        #TODO: make a context menu
        
    # multiplierContextMenu --> reference = STDF V4.pdf @ page 50 & https://en.wikipedia.org/wiki/Order_of_magnitude
        multipliers = ['y (yocto=10⁻²⁴)',
                       'z (zepto=10⁻²¹)',
                       'a (atto=10⁻¹⁸)',
                       'f (femto=10⁻¹⁵)',
                       'p (pico=10⁻¹²)',
                       'η (nano=10⁻⁹)',
                       'μ (micro=10⁻⁶)',
                       'ppm (parts per million=ᴺ/₁․₀₀₀․₀₀₀)',
                       'm (mili=10⁻³)',
                       '‰ (promille=ᴺ/₁․₀₀₀)'
                       '% (percent=ᴺ/₁₀₀)',
                       'c (centi=10⁻²)'
                       'd (deci=10⁻¹)'
                       '˽ (no scaling=10⁰)',
                       '㍲ (deca=10¹)',
                       'h (hecto=10²)',
                       'k (kilo=10³)',
                       'M (mega=10⁶)',
                       'G (giga=10⁹)',
                       'T (tera=10¹²)',
                       'P (peta=10¹⁵)',
                       'E (exa=10¹⁸)',
                       'Z (zetta=10²¹)',
                       'ϒ (yotta=10²⁴)']
        #TODO: make a context menu

    # infiniteContext
        special_values = ['+∞', 'None', '-∞'] 
        #TODO: make a context menu

    # DescriptionTab
        self.description.clear()
        #TODO: the description should be at least xyz chanracters long !
        
    # InputParametersTab
        self.inputParameterMoveUp.setIcon(qta.icon('mdi.arrow-up-bold-box-outline', color='orange'))
        self.inputParameterMoveDown.setIcon(qta.icon('mdi.arrow-down-bold-box-outline', color='orange'))
        self.inputParameterAdd.setIcon(qta.icon('mdi.plus-box-outline', color='orange'))
        self.inputParameterDelete.setIcon(qta.icon('mdi.minus-box-outline', color='orange'))
        self.inputParameterTable.clear()
        self.inputParameterTable.setColumnCount(6)
        self.inputParameterTable.setHorizontalHeaderLabels(['Name', 'Min', 'Default', 'Max', '10ᵡ', 'Unit'])
        self.inputParameterTable.setRowCount(1)

        item_name = QtWidgets.QTableWidgetItem("Temperature")
        self.inputParameterTable.setItem(0,0,item_name)
        item_min = QtWidgets.QTableWidgetItem("-40")
        self.inputParameterTable.setItem(0,1,item_min)
        item_default = QtWidgets.QTableWidgetItem("+25")
        self.inputParameterTable.setItem(0,2,item_default)
        item_max = QtWidgets.QTableWidgetItem("+170")
        self.inputParameterTable.setItem(0,3,item_max)
        item_multiplier = QtWidgets.QTableWidgetItem('')
        self.inputParameterTable.setItem(0,4,item_multiplier)
        item_unit = QtWidgets.QTableWidgetItem("°C")
        self.inputParameterTable.setItem(0,5,item_unit)

        self.inputParameterTable.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.inputParameterTable.customContextMenuRequested.connect(self.input_parameters_context_menu_manager)
        
        #Idea: limit the number of input parameters to 3, as shmoo-ing on 3 parameters is still
        #      manageable for a human (3D), but more is not ...




    # OutputParametersTab
        self.outputParameterMoveUp.setIcon(qta.icon('mdi.arrow-up-bold-box-outline', color='orange'))
        self.outputParameterMoveDown.setIcon(qta.icon('mdi.arrow-down-bold-box-outline', color='orange'))
        self.outputParameterAdd.setIcon(qta.icon('mdi.plus-box-outline', color='orange'))
        self.outputParameterDelete.setIcon(qta.icon('mdi.minus-box-outline', color='orange'))
        #Idea: limit the number of output parameters to 9, so we have a decade per test-number,
        #      and the '0' is the FTR 🙂

    # buttons
        self.CancelButton.clicked.connect(self.CancelButtonPressed)
        self.OKButton.clicked.connect(self.OKButtonPressed)
        self.OKButton.setEnabled(False)

        self.verify()
        self.show()

    def input_parameters_context_menu_manager(self, point):
        '''
        here we select which context menu (for input_parameters) we need,
        based on the column where we activated the context menu on, and 
        dispatch to the appropriate context menu.
        '''
        index = self.inputParameterTable.indexAt(point)
        col = index.column()
        row = index.row()

        print(f"({point.x()}, {point.y()})-->[{row}, {col}] = ", end='')

        if col == 5: # Unit
            print(f"units")
            menu = QtWidgets.QMenu(self)
            menu.addAction("boe")
            
            
            # menu.addAction(qta.icon("mdi.incognito", color='orange') ,"audit")
            # audit.triggered.connect(self.placeholder)
            
            menu.exec_(QtGui.QCursor.pos())

            
        elif col == 4: # multiplier
            print(f"multiplier")
        elif col >= 1 and col <= 3: # Min, Default, Max
            print(f"special_values")
        else: # Name
            print(f"name")


    # def 


    def verify(self):
        self.Feedback.setText("")
        if not is_valid_test_name(self.TestName.text()):
            self.Feedback.setText("The test name can not contain the word 'TEST' in any form!")
        else:
            if self.TestName.text() in self.parent.project_info.get_tests_from_files(self.parent.active_hw, self.parent.base_combo.currentText()):
                self.Feedback.setText("Test already exists!")
            else:
                self.Feedback.setText("")



        if self.Feedback.text() == "":
            self.OKButton.setEnabled(True)
        else:
            self.OKButton.setEnabled(False)

    def CancelButtonPressed(self):
        self.accept()

    def OKButtonPressed(self):
        name = self.TestName.text()
        hardware = self.ForHardwareSetup.currentText()
        base = self.WithBase.currentText()
        test_data = {'input_parameters' : {},
                     'output_parameters' : {}}

        self.parent.project_info.add_test(name, hardware, base, test_data)        
        self.accept()

def new_test_dialog(parent):
    newTestWizard = NewTestWizard(parent)
    newTestWizard.exec_()
    del(newTestWizard)

if __name__ == '__main__':
    import sys, qdarkstyle
    from ATE.org.actions.dummy_main import DummyMainWindow

    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    dummyMainWindow = DummyMainWindow()
    dialog = NewTestWizard(dummyMainWindow)
    dummyMainWindow.register_dialog(dialog)
    sys.exit(app.exec_())
