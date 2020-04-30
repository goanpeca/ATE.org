# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 18:56:05 2019

@author: hoeren

References:
    http://www.cplusplus.com/reference/cstdio/fprintf/
    https://docs.python.org/3/library/functions.html#float
    https://docs.python.org/3.6/library/string.html#format-specification-mini-language
    
"""
import os
import re

import numpy as np

from ATE.org.validation import (is_valid_test_name, 
                                is_valid_python_class_name, 
                                
                                valid_test_parameter_name_regex, 
                                valid_test_name_regex,
                                
                                valid_min_float_regex,
                                valid_default_float_regex,
                                valid_max_float_regex)

from PyQt5 import QtCore, QtGui, QtWidgets, uic

import qdarkstyle
import qtawesome as qta

minimal_description_length = 80 

class Delegator(QtWidgets.QStyledItemDelegate):

    def __init__(self, regex, parent=None):
        QtWidgets.QStyledItemDelegate.__init__(self, parent)
        self.validator = QtGui.QRegExpValidator(QtCore.QRegExp(regex))

    def createEditor(self, parent, option, index):
        line_edit = QtWidgets.QLineEdit(parent)
        line_edit.setValidator(self.validator)
        return line_edit

    #bookmark: afdadf
    


class TestWizard(QtWidgets.QDialog):

    def __init__(self, project_info, fixedHardware=None, fixedBase=None, 
                 testName=None, docString=None, inputParameters=None, 
                 outputParameters=None):
        super().__init__()

        my_ui = __file__.replace('.py', '.ui')
        if not os.path.exists(my_ui):
            raise Exception("can not find %s" % my_ui)
        uic.loadUi(my_ui, self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle(' '.join(re.findall('.[^A-Z]*', os.path.basename(__file__).replace('.py', ''))))

        self.project_info = project_info

    # Feedback
        self.Feedback.setStyleSheet('color: orange')

    # TestName
        TestName_validator = QtGui.QRegExpValidator(QtCore.QRegExp(valid_test_name_regex), self)
        self.TestName.setText("")
        self.TestName.setValidator(TestName_validator)
        self.TestName.textChanged.connect(self.verify)

    # ForHardwareSetup
        existing_hardwares = self.project_info.get_hardwares()
        self.ForHardwareSetup.blockSignals(True)
        self.ForHardwareSetup.clear()
        self.ForHardwareSetup.addItems(existing_hardwares)
        self.ForHardwareSetup.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        if fixedHardware!=None: # yes 
            if fixedHardware in existing_hardwares:
                self.ForHardwareSetup.setCurrentText(fixedHardware)
            else:
                self.ForHardwareSetup.setCurrentText(sorted(existing_hardwares)[-1]) # highest available hardware
            self.ForHardwareSetup.setDisabled(True)
        else: 
            self.ForHardwareSetup.setCurrentText(sorted(existing_hardwares)[-1])            
            self.ForHardwareSetup.setEnabled(True)
        self.ForHardwareSetup.blockSignals(False)

    # WithBase
        existing_bases = ['PR', 'FT']
        self.WithBase.blockSignals(True)
        self.WithBase.clear()
        self.WithBase.addItems(existing_bases)
        self.WithBase.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        if fixedBase!=None:
            if fixedBase in existing_bases:
                self.WithBase.setCurrentText(fixedBase)
            else:
                self.WithBase.setCurrentText('PR')
            self.WithBase.setDisabled(True)
        else:
            self.WithBase.setCurrentText('PR')            
            self.WithBase.setEnabled(True)
        self.WithBase.blockSignals(False)

    # DescriptionTab
        self.description.blockSignals(True)
        self.description.clear()
        self.description.setLineWrapMode(QtWidgets.QTextEdit.NoWrap) # https://doc.qt.io/qt-5/qtextedit.html#LineWrapMode-enum
        #TODO: add a line at 80 characters (https://stackoverflow.com/questions/30371613/draw-vertical-lines-on-qtextedit-in-pyqt)
        if docString!=None:
            # self.description
            pass
        else:
            #TODO: add user, time and such to the description by default ?!?
            pass
        #TODO: fix this 
        self.description_length = 0
        self.description.textChanged.connect(self.descriptionLength)
        self.description.blockSignals(False)
        
    # Delegators
        self.minDelegator = Delegator(valid_min_float_regex, self)
        self.maxDelegator = Delegator(valid_max_float_regex, self)
        self.defaultDelegator = Delegator(valid_default_float_regex, self)
        self.nameDelegator = Delegator(valid_test_parameter_name_regex, self)
        
    # InputParametersTab
        self.inputParameterMoveUp.setIcon(qta.icon('mdi.arrow-up-bold-box-outline', color='orange'))
        self.inputParameterMoveUp.setToolTip('Move selected parameter Up')
        self.inputParameterMoveUp.clicked.connect(self.moveInputParameterUp)

        self.inputParameterAdd.setIcon(qta.icon('mdi.plus-box-outline', color='orange'))
        self.inputParameterAdd.setToolTip('Add a parameter')
        self.inputParameterAdd.clicked.connect(self.addInputParameter)

        self.inputParameterUnselect.setIcon(qta.icon('mdi.select-off', color='orange'))
        self.inputParameterUnselect.setToolTip('Clear selection')
        self.inputParameterUnselect.clicked.connect(self.unselectInputParameter)
        
        self.inputParameterMoveDown.setIcon(qta.icon('mdi.arrow-down-bold-box-outline', color='orange'))
        self.inputParameterMoveDown.setToolTip('Move selected parameter Down')
        self.inputParameterMoveDown.clicked.connect(self.moveInputParameterDown)
        
        self.inputParameterDelete.setIcon(qta.icon('mdi.minus-box-outline', color='orange'))
        self.inputParameterDelete.setToolTip('Delete selected parameter')
        self.inputParameterDelete.clicked.connect(self.deleteInputParameter)

        inputParameterHeaderLabels = ['Name', 'Min', 'Default', 'Max', '10ᵡ', 'Unit', 'fmt']
        self.inputParameterModel = QtGui.QStandardItemModel()
        self.inputParameterModel.setObjectName('inputParameters')
        self.inputParameterModel.setHorizontalHeaderLabels(inputParameterHeaderLabels)
        self.inputParameterModel.itemChanged.connect(self.inputParameterItemChanged) 

        self.inputParameterView.horizontalHeader().setVisible(True)
        self.inputParameterView.verticalHeader().setVisible(True)
        self.inputParameterView.setModel(self.inputParameterModel)
        self.inputParameterView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems) # https://doc.qt.io/qt-5/qabstractitemview.html#SelectionBehavior-enum
        self.inputParameterView.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection) # https://doc.qt.io/qt-5/qabstractitemview.html#SelectionMode-enum
        self.inputParameterView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu) # https://doc.qt.io/qt-5/qt.html#ContextMenuPolicy-enum
        self.inputParameterView.customContextMenuRequested.connect(self.inputParameterTableContextMenu)
        self.inputParameterView.selectionModel().selectionChanged.connect(self.inputParameterSelectionChanged) # https://doc.qt.io/qt-5/qitemselectionmodel.html
        self.inputParameterView.setItemDelegateForColumn(0, self.nameDelegator)
        self.inputParameterView.setItemDelegateForColumn(1, self.minDelegator)
        self.inputParameterView.setItemDelegateForColumn(2, self.defaultDelegator)
        self.inputParameterView.setItemDelegateForColumn(3, self.maxDelegator)

    # OutputParametersTab
        self.outputParameterMoveUp.setIcon(qta.icon('mdi.arrow-up-bold-box-outline', color='orange'))
        self.outputParameterMoveDown.setIcon(qta.icon('mdi.arrow-down-bold-box-outline', color='orange'))
        self.outputParameterAdd.setIcon(qta.icon('mdi.plus-box-outline', color='orange'))
        self.outputParameterDelete.setIcon(qta.icon('mdi.minus-box-outline', color='orange'))
        #TODO: Idea:
        #   limit the number of output parameters to 9, so we have a decade per test-number,
        #   and the '0' is the FTR 🙂

    # buttons
        self.CancelButton.clicked.connect(self.CancelButtonPressed)
        self.OKButton.clicked.connect(self.OKButtonPressed)
        self.OKButton.setEnabled(False)

        self.verify()
        self.show()

    # need to come after a show()
        T = {'Shmoo' : True, 'Min' : -40, 'Default' : 25, 'Max' : 170, '10ᵡ' : '', 'Unit' : '°C', 'fmt' : '.0f'}        
        self.setInputParameter('Temperature', T)







    def resizeEvent(self, event):
        QtWidgets.QWidget.resizeEvent(self, event)
        self.tableAdjust(self.inputParameterView)
        #self.tableAdjust(self.outputParameterView)
        
    def tableAdjust(self, TableView):
        TableView.resizeColumnsToContents()
        columns = TableView.model().columnCount()
        width = 0
        for column in range(1, columns):
            width+=TableView.columnWidth(column)
        available_width = TableView.geometry().width()
        TableView.setColumnWidth(0, available_width-width-TableView.verticalHeader().width()-columns)
    
    def unitContextMenu(self, setter):
        print(f"unitContexMenu(setter='{setter}')")
        menu = QtWidgets.QMenu(self)
        # unitContextMenu
        #    reference to SI : https://en.wikipedia.org/wiki/International_System_of_Units
        #    reference to unicode : https://en.wikipedia.org/wiki/List_of_Unicode_characters
        base_units = [
            ('s (time - second)', 
             lambda: setter('s','time - second')),
            ('m (length - meter)', 
             lambda: setter('m', 'length - meter')),
            ('kg (mass - kilogram)', 
             lambda: setter('kg', 'mass - kilogram')),
            ('A (electric current - ampères)', 
             lambda: setter('A', 'electric current - ampères')),
            ('K (temperature - Kelvin)', 
             lambda: setter('K', 'temperature - Kelvin')),
            ('mol (amount of substance - mole)', 
             lambda: setter('mol', 'amount of substance - mole')),
            ('cd (luminous intensity - candela)', 
             lambda: setter('cd', 'luminous intensity - candela'))]
        for unit in base_units:
            item = menu.addAction(unit[0])
            item.triggered.connect(unit[1])
        menu.addSeparator()

        derived_units = [
            ('rad (plane angle - radian = m/m)', 
             lambda: self.setInputParameterUnit('rad', 'plane angle - radian = m/m')),
            ('sr (solid angle - steradian = m²/m²)', 
             lambda: self.setInputParameterUnit('sr', 'solid angle - steradian = m²/m²')),
            ('Hz (frequency - hertz = s⁻¹)', 
             lambda: self.setInputParameterUnit('Hz', 'frequency - hertz = s⁻¹')),
            ('N (force, weight - newton = kg⋅m⋅s⁻²)', 
             lambda: self.setInputParameterUnit('N', 'force, weight - newton = kg⋅m⋅s⁻²')),
            ('Pa ( pressure, stress - pascal = kg⋅m⁻¹⋅s⁻²)', 
             lambda: self.setInputParameterUnit('Pa', 'pressure, stress - pascal = kg⋅m⁻¹⋅s⁻²')),
            ('J (energy, work, heat - joule = kg⋅m²⋅s⁻² = N⋅m = Pa⋅m³)', 
             lambda: self.setInputParameterUnit('J', 'energy, work, heat - joule = kg⋅m²⋅s⁻² = N⋅m = Pa⋅m³')),
            ('W (power, radiant flux - watt = kg⋅m²⋅s⁻³ = J/s)', 
             lambda: self.setInputParameterUnit('W', 'power, radiant flux - watt = kg⋅m²⋅s⁻³ = J/s')),
            ('C (electric charge - coulomb = s⋅A)', 
             lambda: self.setInputParameterUnit('C', 'electric charge - coulomb = s⋅A')),
            ('V (electric potential, emf - volt = kg⋅m²⋅s⁻³⋅A⁻¹ = W/A = J/C)', 
             lambda: self.setInputParameterUnit('V', 'electric potential, emf - volt = kg⋅m²⋅s⁻³⋅A⁻¹ = W/A = J/C')),
            ('F (electric capacitance - farad = kg⁻¹⋅m⁻²⋅s⁴⋅A² = C/V)', 
             lambda: self.setInputParameterUnit('F', 'electric capacitance - farad = kg⁻¹⋅m⁻²⋅s⁴⋅A² = C/V')),
            ('Ω (electric resistance, impedance, reactance - ohm = kg⋅m²⋅s⁻³⋅A⁻² = V/A)', 
             lambda: self.setInputParameterUnit('Ω', 'electric resistance, impedance, reactance - ohm = kg⋅m²⋅s⁻³⋅A⁻² = V/A')),
            ('S (electric conductance - siemens = kg⁻¹⋅m⁻²⋅s³⋅A² = Ω⁻¹)', 
             lambda: self.setInputParameterUnit('S', 'electric conductance - siemens = kg⁻¹⋅m⁻²⋅s³⋅A² = Ω⁻¹')),
            ('Wb (magnetic flux - weber = kg⋅m²⋅s⁻²⋅A⁻¹ = V⋅s)', 
             lambda: self.setInputParameterUnit('Wb', 'magnetic flux - weber = kg⋅m²⋅s⁻²⋅A⁻¹ = V⋅s')),
            ('T (magnetic flux density - tesla = kg⋅s⁻²⋅A⁻¹ = Wb/m²)', 
             lambda: self.setInputParameterUnit('T', 'magnetic flux density - tesla = kg⋅s⁻²⋅A⁻¹ = Wb/m²')),
            ('H (electric inductance - henry = kg⋅m²⋅s⁻²⋅A⁻² = Wb/A)', 
             lambda: self.setInputParameterUnit('H', 'electric inductance - henry = kg⋅m²⋅s⁻²⋅A⁻² = Wb/A')),
            ('lm (luminous flux - lumen = cd⋅sr)', 
             lambda: self.setInputParameterUnit('lm', 'luminous flux - lumen = cd⋅sr')),
            ('lx (illuminance - lux = m⁻²⋅cd = lm/m²)', 
             lambda: self.setInputParameterUnit('lx', 'illuminance - lux = m⁻²⋅cd = lm/m²')),
            ('Bq (radioactivity - Becquerel = s⁻¹)', 
             lambda: self.setInputParameterUnit('Bq', 'radioactivity - Becquerel = s⁻¹')),
            ('Gy (absorbed dose - gray = m²⋅s⁻² = J/kg)', 
             lambda: self.setInputParameterUnit('Gy', 'absorbed dose - gray = m²⋅s⁻² = J/kg')),
            ('Sv (equivalent dose - sievert = m²⋅s⁻² = J/kg)', 
             lambda: self.setInputParameterUnit('Sv', 'equivalent dose - sievert = m²⋅s⁻² = J/kg')),
            ('kat (catalytic activity - katal = mol⋅s⁻¹)', 
             lambda: self.setInputParameterUnit('kat', 'catalytic activity - katal = mol⋅s⁻¹'))]
        for unit in derived_units:
            item = menu.addAction(unit[0])
            item.triggered.connect(unit[1])
        menu.addSeparator()

        alternative_units = [
            ('°C (temperature - degree Celcius = K - 273.15)',
             lambda: self.setInputParameterUnit('°C', 'temperature - degree Celcius = K - 273.15')),
            ('Gs (magnetic flux density - gauss = 10⁻⁴ Tesla)',
             lambda: self.setInputParameterUnit('Gs', 'magnetic flux density - gauss = 10⁻⁴ Tesla')),
            ('˽ (no dimension / unit)',
             lambda: self.setInputParameterUnit('', 'no dimension / unit'))]
        for unit in alternative_units:
            item = menu.addAction(unit[0])
            item.triggered.connect(unit[1])
        return menu
    
    def multiplierContextMenu(self, multiplierSetter):
        menu = QtWidgets.QMenu(self)
        normal_multipliers = [
            ('y (yocto=10⁻²⁴)', 
             lambda: multiplierSetter('y', 'yocto=10⁻²⁴')),
            ('z (zepto=10⁻²¹)', 
             lambda: multiplierSetter('z', 'zepto=10⁻²¹')),
            ('a (atto=10⁻¹⁸)', 
             lambda: multiplierSetter('a', 'atto=10⁻¹⁸')),
            ('f (femto=10⁻¹⁵)', 
             lambda: multiplierSetter('f', 'femto=10⁻¹⁵')),
            ('p (pico=10⁻¹²)', 
             lambda: multiplierSetter('p', 'pico=10⁻¹²')),
            ('η (nano=10⁻⁹)', 
             lambda: multiplierSetter('η', 'nano=10⁻⁹')),
            ('μ (micro=10⁻⁶)', 
             lambda: multiplierSetter('μ', 'micro=10⁻⁶')),
            ('m (mili=10⁻³)', 
             lambda: multiplierSetter('m', 'mili=10⁻³')),
            ('c (centi=10⁻²)', 
             lambda: multiplierSetter('c', 'centi=10⁻²')),
            ('d (deci=10⁻¹)', 
             lambda: multiplierSetter('d', 'deci=10⁻¹')),
            ('˽ (no scaling=10⁰)', 
             lambda: multiplierSetter('', 'no scaling=10⁰')),
            ('㍲ (deca=10¹)', 
             lambda: multiplierSetter('㍲', 'deca=10¹')),
            ('h (hecto=10²)', 
             lambda: multiplierSetter('h', 'hecto=10²')),
            ('k (kilo=10³)', 
             lambda: multiplierSetter('k', 'kilo=10³')),
            ('M (mega=10⁶)', 
             lambda: multiplierSetter('M', 'mega=10⁶')),
            ('G (giga=10⁹)', 
             lambda: multiplierSetter('G', 'giga=10⁹')),
            ('T (tera=10¹²)', 
             lambda: multiplierSetter('T', 'tera=10¹²')),
            ('P (peta=10¹⁵)', 
             lambda: multiplierSetter('P', 'peta=10¹⁵)')),
            ('E (exa=10¹⁸)', 
             lambda: multiplierSetter('E', 'exa=10¹⁸')),
            ('Z (zetta=10²¹)', 
             lambda: multiplierSetter('Z', 'zetta=10²¹')),
            ('ϒ (yotta=10²⁴)', 
             lambda: multiplierSetter('ϒ', 'yotta=10²⁴'))]
        for multiplier in normal_multipliers:
            item = menu.addAction(multiplier[0])
            item.triggered.connect(multiplier[1])
        menu.addSeparator()

        dimensionless_multipliers = [
            ('ppm (parts per million=ᴺ/₁․₀₀₀․₀₀₀)', 
             lambda: multiplierSetter('ppm', 'parts per million=ᴺ/₁․₀₀₀․₀₀₀')),
            ('‰ (promille=ᴺ/₁․₀₀₀)', 
             lambda: multiplierSetter('‰', 'promille=ᴺ/₁․₀₀₀')),
            ('% (percent=ᴺ/₁₀₀)', 
             lambda: multiplierSetter('%', 'percent=ᴺ/₁₀₀')),
            ('dB (decibel=10·log[P/Pref])', 
             lambda: multiplierSetter('dB', 'decibel=10·log[P/Pref]')), 
            ('dBV (decibel=20·log[V/Vref])', 
             lambda: multiplierSetter('dBV', 'decibel=20·log[V/Vref]'))]
        for multiplier in dimensionless_multipliers:
            item = menu.addAction(multiplier[0])
            item.triggered.connect(multiplier[1])
        return menu
    
    def inputParameterTableContextMenu(self, point):
        '''
        here we select which context menu (for input_parameters) we need,
        based on the column where we activated the context menu on, and 
        dispatch to the appropriate context menu.
        '''
        index = self.inputParameterView.indexAt(point)
        objectName = index.model().objectName()
        if objectName == 'inputParameters':
            typeSetter = self.setInputParameterType
            valueSetter = self.setInputParameterValue
            multiplierSetter = self.setInputParameterMultiplier
            unitSetter = self.setInputParameterUnit
        elif objectName == 'outputParameters':
            pass
        else:
            print(f"What the fuck is '{objectName}'?")
        
        
        print(f"{objectName}({point.x()}, {point.y()})-->[{index.row()}, {index.column()}]")

        if index.column() == 0: # Name
            if index.row() != 0: # not for temperature
                menu = QtWidgets.QMenu(self)
                # http://www.cplusplus.com/reference/cstdio/fprintf/
                parameter_types =[
                    ("Real", lambda: typeSetter('Real')),
                    ("Integer (Decimal - '123...')", lambda: typeSetter('Decimal')),
                    ("Integer (Hexadecimal - '0xFE...')", lambda: typeSetter('Hexadecimal')),
                    ("Integer (Octal - '0o87...')", lambda: typeSetter('Octal')),
                    ("Integer (Binary - '0b10...')", lambda: typeSetter('Binary'))]
                
                check = qta.icon('mdi.check', color='orange')
                
                parameter = self.inputParameterTable.item(self.row, self.col)
                parameter_type = parameter.toolTip()
                
                for type_option in parameter_types:
                    if type_option[0] == parameter_type:
                        item = menu.addAction(check, type_option[0])
                    else:
                        item = menu.addAction(type_option[0])
                    item.triggered.connect(type_option[1])
                menu.exec_(QtGui.QCursor.pos())

        elif index.column() >= 1 and index.column() <= 3: # Min, Default, Max
            if index.row() != 0: # not for temperature
                menu = QtWidgets.QMenu(self)
                special_values = [
                    ('+∞', lambda: valueSetter('+∞')),
                    ('0', lambda: valueSetter('0')), 
                    ('-∞', lambda: valueSetter('-∞'))]
                for special_value in special_values:
                    item = menu.addAction(special_value[0])
                    item.triggered.connect(special_value[1])
                menu.exec_(QtGui.QCursor.pos())

        elif index.column() == 4: # multiplier --> reference = STDF V4.pdf @ page 50 & https://en.wikipedia.org/wiki/Order_of_magnitude
            if index.row() != 0: # temperature
                menu = self.multiplierContextMenu(multiplierSetter)
                menu.exec_(QtGui.QCursor.pos())

        elif index.column() == 5: # Unit
            if index.row() != 0: # not temperature
                menu = self.unitContextMenu(unitSetter)
                menu.exec_(QtGui.QCursor.pos())
                
    def inputParameterItemChanged(self, item):
        '''
        if one of the cells in self.inputParameterModel is changed, this 
        routine is called, and it could be cause to re-size the table columns,
        and it could be cause to make a checkbox change.
        '''
        name_item = self.inputParameterModel.item(item.row(), 0)
        min_item = self.inputParameterModel.item(item.row(), 1)
        default_item = self.inputParameterModel.item(item.row(), 2)
        max_item = self.inputParameterModel.item(item.row(), 3)
        
        print(f'type(max_item) = {type(max_item)}')
        
        
        Min = min_item.data(QtCore.Qt.DisplayRole)
        if Min == '-∞': 
            Min = -np.Inf
        else:
            Min = float(Min)
        Default = default_item.data(QtCore.Qt.DisplayRole)
        if Default == '-∞':
            Default = -np.Inf
        elif Default == '+∞':
            Default = np.Inf
        else:
            Default = float(Default)
        Max = max_item.data(QtCore.Qt.DisplayRole)
        if Max in ['∞', '+∞']:
            Max = np.Inf
        else:
            Max = float(Max)

        if Min <= Default <= Max and Min!=-np.Inf and Max!=np.Inf:
            name_item.setFlags(QtCore.Qt.ItemIsSelectable | 
                               QtCore.Qt.ItemIsEditable | 
                               QtCore.Qt.ItemIsEnabled |
                               QtCore.Qt.ItemIsUserCheckable)
        else:
            name_item.setFlags(QtCore.Qt.ItemIsSelectable | 
                               QtCore.Qt.ItemIsEditable | 
                               QtCore.Qt.ItemIsEnabled)
            
            
            
        self.tableAdjust(self.inputParameterView)
       
    def inputParameterSelectionChanged(self):
        '''
        this should set the buttons
        '''
        selectedIndexes = self.inputParameterView.selectedIndexes()
        max_rows = self.inputParameterModel.rowCount()
        selected_rows = []
        for index in selectedIndexes:
            selected_rows.append(index.row())
        number_of_selected_rows = len(selected_rows)

        if number_of_selected_rows == 0:
            self.inputParameterUnselect.setEnabled(False)
            self.inputParameterMoveUp.setEnabled(False)
            self.inputParameterDelete.setEnabled(False)
            self.inputParameterMoveDown.setEnabled(False)
        else:
            self.inputParameterUnselect.setEnabled(True)
            if number_of_selected_rows == 1:
                self.inputParameterDelete.setEnabled(True)
                selected_row = selected_rows[0]
                if selected_row == 0:
                    self.inputParameterMoveUp.setEnabled(False)
                    self.inputParameterMoveDown.setEnabled(False)            
                else:
                    if selected_row > 1: # can move up
                        self.inputParameterMoveUp.setEnabled(True)
                    else:
                        self.inputParameterMoveUp.setEnabled(False)
                    if selected_row < max_rows:
                        self.inputParameterMoveDown.setEnabled(True)
                    else:
                        self.inputParameterMoveDown.setEnabled(False)
            else:
                self.inputParameterMoveUp.setEnabled(False)
                self.inputParameterDelete.setEnabled(False)
                self.inputParameterMoveDown.setEnabled(False)

    def setInputParameterType(self, Type):
        selection = self.inputParameterView.selectedIndexes()

        for index in selection:
            pass

    # def setUnitReal(self):
    #     self.setUnit('𝓡', 'unitless real number')

    # def setUnitInteger(self):
    #     self.setUnit('№', 'unitless integer number')

    # def setParameterReal(self):
    #     print("self.setParameterReal")

    # def setParameterDecimal(self):
    #     print("self.setParameterDecimal")
        
    # def setParameterHexadecimal(self):
    #     print("self.setParameterHexadecimal")

    # def setParameterOctal(self):
    #     print("self.setParameterOctal")

    # def setParameterBinary(self):
    #     print("self.setParameterBinary")

    def setInputParameterValue(self, value):
        '''
        we arrive here after selecting one or more items, and evoking the 
        context menu for Value.
        This will evoke inputParameterItemchanged (which resizes the columms)
        At the end we clear the selection which evokes inputParameterSelectionChanged
        (which sets the buttons correctly)
        '''
        index_selection = self.inputParameterView.selectedIndexes()
        
        for index in index_selection:
            if value == '+∞': # only the max column can have +∞
                if index.row() != 0: # not for 'Temperature'
                    if index.column() == 3: # max column
                        max_item = self.inputParameterModel.itemFromIndex(index)
                        max_item.setData(value, QtCore.Qt.DisplayRole)
            elif value == '-∞': # only the min column can have -∞
                if index.row() != 0: # not for 'Temperature'
                    if index.column() == 1: # min column
                        min_item = self.inputParameterModel.itemFromIndex(index)
                        min_item.setData(value, QtCore.Qt.DisplayRole)
            elif value == '': # for name, min, default, max, multiplier AND unit
                if index.column() != 0: # not for 'Temperature'
                    item = self.inputParameterModel.itemFromIndex(index)
                    item.setData(value, QtCore.Qt.DisplayRole)
            elif value == '0': # for min, default, max
                if index.column() != 0: # not for 'Temperature'
                    item = self.inputParameterModel.itemFromIndex(index)
                    item.setData(value, QtCore.Qt.DisplayRole)
            else:
                raise Exception("shouldn't be able to reach this point")
        self.inputParameterView.clearSelection()

    def setInputParameterMultiplier(self, text, tooltip):
        selection = self.inputParameterView.selectedIndexes()
        
        for index in selection:
            if index.column() == 4: # multipliers are located in column#4
                self.inputParameterModel.setData(index, text, QtCore.Qt.DisplayRole)
                self.inputParameterModel.setData(index, tooltip, QtCore.Qt.ToolTipRole)

    def setInputParameterUnit(self, text, tooltip):
        selection = self.inputParameterView.selectedIndexes()
        
        for index in selection:
            if index.column() == 5: # units are located in column#5
                self.inputParameterModel.setData(index, text, QtCore.Qt.DisplayRole)
                self.inputParameterModel.setData(index, tooltip, QtCore.Qt.ToolTipRole)


    def setInputParameter(self, name, attributes, row=None):
        '''
        sets the inputParameter name and it's attribues
        if row==None, append to the list.
        if row is given, it **must** already exist!
        
        Structure (of all input parameters):
        
        input_parameters = {                          # https://docs.python.org/3.6/library/string.html#format-specification-mini-language
            'Temperature' : {'Shmoo' : True,  'Min' :     -40, 'Default' : 25, 'Max' :     170, '10ᵡ' :  '', 'Unit' : '°C', 'fmt' : '.0f'}, # Obligatory !
            'i'           : {'Shmoo' : False, 'Min' : -np.inf, 'Default' :  0, 'Max' : +np.inf, '10ᵡ' : 'μ', 'Unit' :  'A', 'fmt' : '.3f'},
            'j'           : {'Shmoo' : False, 'Min' :    '-∞', 'Default' :  0, 'Max' :    '+∞', '10ᵡ' : 'μ', 'Unit' :  'A', 'fmt' : '.3f'}}
        
        References:
            https://doc.qt.io/qt-5/qt.html#CheckState-enum
            https://doc.qt.io/qt-5/qt.html#ItemFlag-enum
            https://doc.qt.io/qt-5/qt.html#ItemDataRole-enum
            https://doc.qt.io/qt-5/qstandarditem.html
        '''
        rowCount = self.inputParameterModel.rowCount()
        if name == 'Temperature': # must be at row 0, regardless what row says
            if rowCount == 0: # make first entry
                self.inputParameterModel.appendRow([QtGui.QStandaardItem() for i in range(7)])
            item_row = 0
        else:
            if row == None: # append
                self.inputParameterModel.appendRow([QtGui.QStandaardItem() for i in range(7)])
                item_row = rowCount
            else: # update
                if row > rowCount:
                    raise Exception(f"row({row}) > rowCount({rowCount})")
                name_item = self.inputParameterModel.item(row, 0)
                item_row = row

        name_item = self.inputParameterModel.item(item_row, 0)
        min_item = self.inputParameterModel.item(item_row, 1)
        default_item = self.inputParameterModel.item(item_row, 2)
        max_item = self.inputParameterModel.item(item_row, 3)
        multiplier_item = self.inputParameterModel.item(item_row, 4)
        unit_item = self.inputParameterModel.item(item_row, 5)
        fmt_item = self.inputParameterModel.item(item_row, 6)               

    # fmt
        if name == 'Temperature':
            Fmt = '.0f'
            fmt_item.setData(Fmt, QtCore.Qt.DisplayRole)
            fmt_item.setData(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter, QtCore.Qt.TextAlignmentRole)
            fmt_item.setFlags(QtCore.Qt.NoItemFlags)
        else:
            if 'fmt' not in attributes:
                Fmt = '.3f'
            else:
                Fmt = attributes['fmt']
            fmt_item.setData(Fmt, QtCore.Qt.DisplayRole)
            fmt_item.setData(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter, QtCore.Qt.TextAlignmentRole)
            fmt_item.setFlags(QtCore.Qt.ItemIsSelectable, QtCore.Qt.ItemIsEditable, QtCore.Qt.ItemIsEnabled)

    # Min
        if name == 'Temperature':
            if isinstance(attributes['Min'], str):
                if '∞' in attributes['Min']: # forget about it --> -60
                    Min = -60.0
                else:
                    Min = float(attributes['Min'])
                    if Min < -60.0: Min = -60.0
            elif isinstance(attributes['Min'], (float, int)):
                Min = float(attributes['Min'])
                if Min < -60.0: Min = -60.0
            else:
                raise Exception("type(attribute['Min']) = {type(attribute['Min'])}, which is not (str, float or int) ... WTF?!?")
            min_item.setData(f"{Min:{Fmt}}", QtCore.Qt.DisplayRole)
        else:
            if isinstance(attributes['Min'], str):
                if '∞' in attributes['Min']:
                    Min = -np.inf
                    min_item.setData('-∞', QtCore.Qt.DisplayRole)
                else:
                    Min = float(attributes['Min'])
                    min_item.setData(f"{Min:{Fmt}}", QtCore.Qt.DisplayRole)
            elif isinstance(attributes['Min'], (float, int)):
                if attributes['Min'] == -np.inf:
                    Min = -np.inf
                    min_item.setData('-∞', QtCore.Qt.DisplayRole)
                else:
                    Min = float(attributes['Min'])
                    min_item.setData(f"{Min:{Fmt}}", QtCore.Qt.DisplayRole)
            else:
                raise Exception("type(attribute['Min']) = {type(attribute['Min'])}, which is not (str, float or int) ... WTF?!?")
            min_item.setData(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter, QtCore.Qt.TextAlignmentRole)
        min_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)

    # Max
        if name == 'Temperature':
            if isinstance(attributes['Max'], str):
                if '∞' in attributes['Max']: # forget about it --> 200
                    Max = 200.0
                else:
                    Max = float(attributes['Max'])
                    if Max > 200.0: Max = 200.0
            elif isinstance(attributes['Max'], (float, int)):
                Max = float(attributes['Max'])
                if Max > 200.0: Max = 200.0
            else:
                raise Exception("type(attribute['Max']) = {type(attribute['Max'])}, which is not (str, float or int) ... WTF?!?")
            max_item.setData(f"{Max:{Fmt}}", QtCore.Qt.DisplayRole)
        else:
            if isinstance(attributes['Max'], str):
                if '∞' in attributes['Max']:
                    Max = np.inf
                    max_item.setData('+∞', QtCore.Qt.DisplayRole)
                else:
                    Max = float(attributes['Max'])
                    max_item.setData(f"{Max:{Fmt}}", QtCore.Qt.DisplayRole)
            elif isinstance(attributes['Max'], (float, int)):
                if attributes['Max'] == np.inf:
                    Max = np.inf
                    max_item.setData('+∞', QtCore.Qt.DisplayRole)
                else:
                    Max = float(attributes['Max'])
                    max_item.setData(f"{Max:{Fmt}}", QtCore.Qt.DisplayRole)
            else:
                raise Exception("type(attribute['Max']) = {type(attribute['Max'])}, which is not (str, float or int) ... WTF?!?")
            max_item.setData(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, QtCore.Qt.TextAlignmentRole)
        max_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)

    # Default
        if name == 'Temperature':
            if isinstance(attributes['Default'], str):
                if '∞' in attributes['Default']: # forget about it --> 25
                    Default = 25.0
                else:
                    Default = float(attributes['Default'])
                    if Default > Max or Default < Min: Default = 25.0
            elif isinstance(attributes['Default'], (float, int)):
                Default = float(attributes['Default'])
                if Default > Max or Default < Min: Default = 25.0
            else:
                raise Exception("type(attribute['Default']) = {type(attribute['Default'])}, which is not (str, float or int) ... WTF?!?")
        else:
            if isinstance(attributes['Default'], str):
               if attributes['Default'] == '-∞' : Default = -np.inf
               elif attributes['Default'] in ['∞', '+∞']: Default = np.inf
               else: Default = float(attributes['Default'])
            elif isinstance(attributes['Default'], (float, int)):
                Default = float(attributes['Default'])
            else:
                raise Exception("type(attribute['Default']) = {type(attribute['Default'])}, which is not (str, float or int) ... WTF?!?")
            if Min == -np.inf and Max == np.inf:
                if Default == -np.inf: Default = 0
                if Default == np.inf: Default = 0
            elif Min == -np.inf:
                if Default > Max: Default = Max
                if Default == -np.inf: Default = Max
            elif Max == np.inf:
                if Default < Min: Default = Min
                if Default == np.inf: Default = Min
            else:
                if Default > Max: Default = Max
                if Default < Min: Default = Min
        default_item.setData(f"{Default:{Fmt}}", QtCore.Qt.DisplayRole)
        default_item.setData(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter, QtCore.Qt.TextAlignmentRole)
        default_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)

    # name
        name_item.setData(name, QtCore.Qt.DisplayRole) # https://doc.qt.io/qt-5/qt.html#ItemDataRole-enum
        name_item.setData(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, QtCore.Qt.TextAlignmentRole)
        if name == 'Temperature': # Shmoo is always enabled, user can not change
            name_item.setData(QtCore.Qt.Checked, QtCore.Qt.CheckStateRole) # https://doc.qt.io/qt-5/qt.html#CheckState-enum
            name_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable) # https://doc.qt.io/qt-5/qt.html#ItemFlag-enum
        else: # take Shmoo from attributes
            if attributes['Shmoo']:
                if Min <= Default <= Max and Min != -np.Inf and Max != np.Inf:
                    name_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)
                    name_item.setData(QtCore.Qt.Checked, QtCore.Qt.CheckStateRole) 
                else:
                    name_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)
                    name_item.setData(QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole) 
            else:
                if Min <= Default <= Max and Min != -np.Inf and Max != np.Inf:
                    name_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)
                else:
                    name_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)
                name_item.setData(QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole) 

    # Multiplier
        if name == 'Temperature': # fixed regardless what the attributes say
            multiplier_item.setData('', QtCore.Qt.DisplayRole)
            multiplier_item.setData(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter, QtCore.Qt.TextAlignmentRole)
            multiplier_item.setFlags(QtCore.Qt.NoItemFlags)
        else:
            multiplier_item.setData(str(attributes['10ᵡ']), QtCore.Qt.DisplayRole)
            multiplier_item.setData(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter, QtCore.Qt.TextAlignmentRole)
            multiplier_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)

    # Unit
        if name == 'Temperature': # fixed regardless what the attribues say
            unit_item.setData('°C', QtCore.Qt.DisplayRole)
            unit_item.setData(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, QtCore.Qt.TextAlignmentRole)
            unit_item.setFlags(QtCore.Qt.NoItemFlags)
        else:
            unit_item.setData(str(attributes['Unit']), QtCore.Qt.DisplayRole)
            unit_item.setData(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, QtCore.Qt.TextAlignmentRole)
            unit_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)
    
    def setInputpParameters(self, definition):
        for name in definition:
            attributes = definition[name]
            self.setInputParameter(name, attributes)
    
    def getInputParameter(self, row):
        attributes = {'shmoo' : None, 'Min' : None, 'Default' : None, 'Max' : None, '10ᵡ' : None, 'Unit' : None, 'fmt' : None}

        name_item = self.inputParameterModel.item(row, 0)
        name = name_item.data(QtCore.Qt.DisplayRole)

        shmoo = name_item.data(QtCore.Qt.CheckStateRole)
        if shmoo & QtCore.Qt.Checked:
            attributes['shmoo'] = True
        else:
            attributes['shmoo'] = False

        min_item = self.inputParameterModel.item(row, 1)
        Min = min_item.data(QtCore.Qt.DisplayRole)
        if Min == '-∞' :
            attributes['Min'] = -np.Inf
        else:
            attributes['Min'] = float(Min)

        default_item = self.inputParameterModel.item(row, 2)
        Default = default_item.data(QtCore.Qt.DisplayRole)
        attributes['Default'] = float(Default)

        max_item = self.inputParameterModel.item(row, 3)
        Max = max_item.data(QtCore.Qt.DisplayRole)
        if Max in ['+∞', '∞']:
            attributes['Max'] = np.Inf
        else:
            attributes['Max'] = float(Max)

        multiplier_item = self.inputParameterModel.item(row, 4)        
        Multiplier = multiplier_item.data(QtCore.Qt.DisplayRole)
        attributes['10ᵡ'] = Multiplier
        
        unit_item = self.inputParameterModel.item(row, 5)
        Unit = unit_item.data(QtCore.Qt.DisplayRole)
        attributes['Unit'] = Unit
                
        fmt_item = self.inputParameterModel.item(row, 6)
        Fmt = fmt_item.data(QtCore.Qt.DisplayRole)
        attributes['fmt'] = Fmt
        
        return name, attributes
    
    def getInputParameters(self):
        retval = {}
        rows = self.inputParameterModel.rowCount()
        for row in rows:
            name, attributes = self.getInputParameter(row)
            retval[name] = attributes
        return retval

    def moveInputParameterUp(self):
        selection = self.inputParameterView.selectedIndexes()

        selected_rows = []
        for index in selection:
            if index.row() not in selected_rows:
                selected_rows.append(index.row())

        #TODO: fix me
        if len(selected_rows) == 1: # can move only one row up at a time!
            selected_row = selected_rows[0]
            if selected_row == 0: # temperature
                print(f"Can not move-up 'Temperature' any further!")
            elif selected_row == 1:
                print(f"Can not move-up 'pname' any further as 'Temperature' is always the first input parameter!")
            else:
                print(f"move row {selected_row} one place up")
        else:
            print(f"Can move-up only one row at a time.") # the move up button should already be de-activated!

    def addInputParameter(self):
        new_row = self.inputParameterModel.rowCount()
        print('addInputParameter new_row = ', new_row)
        existing_parameters = []
        shmooed_parameters = []
        for item_row in range(new_row):
            item = self.inputParameterModel.item(item_row, 0)
            existing_parameters.append(item.text())
            if item.checkState() == QtCore.Qt.Checked:
                shmooed_parameters.append(item.text())

        existing_parameter_indexes = []
        for existing_parameter in existing_parameters:
            if existing_parameter.startswith('new_parameter'):
                existing_index = int(existing_parameter.split('new_parameter')[1])
                if existing_index not in existing_parameter_indexes:
                    existing_parameter_indexes.append(existing_index)

        if len(existing_parameter_indexes) == 0:
            new_parameter_index = 1
        else:
            new_parameter_index = max(existing_parameter_indexes)+1            

        reply = QtWidgets.QMessageBox.Yes
        print(f"shmooed parameters = {len(shmooed_parameters)}")
        if len(shmooed_parameters) >= 3:
            reply = QtWidgets.QMessageBox.question(
                self, 
                'Warning', 
                'It is not advisable to have more than 3 input parameters,\nbecause shmooing will become a nightmare.\n\ndo you still want to continue?', 
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, 
                QtWidgets.QMessageBox.No)
        
        if reply == QtWidgets.QMessageBox.Yes:
            
            name_item = QtGui.QStandardItem()
            self.inputParameterModel.appendRow(name_item)
    
            name_index = self.inputParameterModel.indexFromItem(name_item)
            self.inputParameterModel.setData(name_index, f'new_parameter{new_parameter_index}', QtCore.Qt.DisplayRole)
            self.inputParameterModel.setData(name_index, 'Real', QtCore.Qt.ToolTipRole)
            self.inputParameterModel.setData(name_index, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, QtCore.Qt.TextAlignmentRole)
            self.inputParameterModel.setData(name_index, QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole) 
            self.inputParameterModel.itemFromIndex(name_index).setFlags(QtCore.Qt.ItemIsSelectable | 
                                                                        QtCore.Qt.ItemIsEditable | 
                                                                        QtCore.Qt.ItemIsEnabled)

            min_index = self.inputParameterModel.index(name_index.row(), 1)
            self.inputParameterModel.setData(min_index, '-∞', QtCore.Qt.DisplayRole)
            self.inputParameterModel.setData(min_index, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter, QtCore.Qt.TextAlignmentRole)
            self.inputParameterModel.itemFromIndex(min_index).setFlags(QtCore.Qt.ItemIsSelectable | 
                                                                       QtCore.Qt.ItemIsEditable | 
                                                                       QtCore.Qt.ItemIsEnabled)

            default_index = self.inputParameterModel.index(name_index.row(), 2)
            self.inputParameterModel.setData(default_index, '0', QtCore.Qt.DisplayRole)
            self.inputParameterModel.setData(default_index, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter, QtCore.Qt.TextAlignmentRole)
            self.inputParameterModel.itemFromIndex(default_index).setFlags(QtCore.Qt.ItemIsSelectable | 
                                                                           QtCore.Qt.ItemIsEditable | 
                                                                           QtCore.Qt.ItemIsEnabled)
            
            max_index = self.inputParameterModel.index(name_index.row(), 3)
            self.inputParameterModel.setData(max_index, '+∞', QtCore.Qt.DisplayRole)
            self.inputParameterModel.setData(max_index, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, QtCore.Qt.TextAlignmentRole)
            self.inputParameterModel.itemFromIndex(max_index).setFlags(QtCore.Qt.ItemIsSelectable | 
                                                                       QtCore.Qt.ItemIsEditable | 
                                                                       QtCore.Qt.ItemIsEnabled)

            multiplier_index = self.inputParameterModel.index(name_index.row(), 4)
            self.inputParameterModel.setData(multiplier_index, '', QtCore.Qt.DisplayRole)
            self.inputParameterModel.setData(multiplier_index, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter, QtCore.Qt.TextAlignmentRole)
            self.inputParameterModel.itemFromIndex(multiplier_index).setFlags(QtCore.Qt.ItemIsSelectable | 
                                                                              QtCore.Qt.ItemIsEditable | 
                                                                              QtCore.Qt.ItemIsEnabled)

            unit_index = self.inputParameterModel.index(name_index.row(), 5)
            self.inputParameterModel.setData(unit_index, '?', QtCore.Qt.DisplayRole)
            self.inputParameterModel.setData(unit_index, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, QtCore.Qt.TextAlignmentRole)
            self.inputParameterModel.itemFromIndex(unit_index).setFlags(QtCore.Qt.ItemIsSelectable | 
                                                                        QtCore.Qt.ItemIsEditable | 
                                                                        QtCore.Qt.ItemIsEnabled)

    def unselectInputParameter(self):
        self.inputParameterView.clearSelection()

    def deleteInputParameter(self):
        selected_items = self.inputParameterTable.selectedItems()
        selected_rows = []
        for item in selected_items:
            if item.row() not in selected_rows:
                selected_rows.append(item.row())
        if len(selected_rows) == 1: # can move only delete one parameter at a time!
            if selected_rows[0] == 0: # can not remove the temperature!
                print(f"Can not delete 'temperature', it is an obligatory parameter !")
            else:
                print(f"remove row {selected_rows[0]}")

    def moveInputParameterDown(self):
        selected_items = self.inputParameterTable.selectedItems()
        last_row = self.inputParameterTable.rowCount()-1
        selected_rows = []
        for item in selected_items:
            if item.row() not in selected_rows:
                selected_rows.append(item.row())
        if len(selected_rows) == 1: # can move only one row down at a time!
            selected_row = selected_rows[0]
            if selected_row == 0: # temperature
                print(f"Can not move-down 'Temperature', it needs to be the first input parameter!")
            elif selected_row == last_row:
                pname = self.inputParameterTable.item(selected_row, 0).text()
                print(f"Can not move-down '{pname}' any further!")
            else: 
                print(f"move row {selected_row} one place up")
        else:
            print(f"Can move-down only one row at a time.")


    def outputParameterTableContextMenu(self):
        '''
        http://www.cplusplus.com/reference/cstdio/fprintf/
        '''
        pass
    
    
    
    
    

    def descriptionLength(self):
        retval = len(self.description.toPlainText().replace(' ','').replace('\n', '').replace('\t', ''))
        # print(f"{self.description_length}/{minimal_description_length}")
        return retval

    def verify(self):
        self.Feedback.setText("")
        # 1. Check that we have a hardware selected
        if self.ForHardwareSetup.currentText() == '':
            self.Feedback.setText("Select a 'hardware'")
        
        # 2. Check that we have a base selected
        if self.Feedback.text() == "":
            if self.WithBase.currentText() == '':
                self.Feedback.setText("Select a 'base'")
        
        # 3. Check if we have a test name
        if self.Feedback.text() == "":
            if self.TestName.text() == '':
                self.Feedback.setText("Supply a name for the test")
                
        # 4. Check if the test name is a valid python class name (covered by LineEdit, but it doesn't hurt)
        if self.Feedback.text() == "":
            if not is_valid_python_class_name(self.TestName.text()):
                fb = f"The test name '{self.TestName.text()}' is not a valid python class name. "
                fb += "(It doesn't comply to RegEx '{valid_python_class_name_regex}'"
                self.Feedback.setText(fb)
            
        # 5. Check if the test name holds an underscore (useless, as covered by the LineEdit, but it doesn't hurt)
        if self.Feedback.text() == "":
            if '_' in self.TestName.text():
                fb = f"The usage of underscore(s) is disallowed!"
                self.Feedback.setText(fb)
                
        # 6. Check if the test name holds the word 'Test' in any form
        if self.Feedback.text() == "":
            if not is_valid_test_name(self.TestName.text()):
                fb = "The test name can not contain the word 'TEST' in any form!"
                self.Feedback.setText(fb)
        
        # 7. Check if the test name already exists
        if self.Feedback.text() == "":
            existing_tests = self.project_info.get_tests_from_files(
                self.ForHardwareSetup.currentText(),
                self.WithBase.currentText())
            if self.TestName.text() in existing_tests:
                self.Feedback.setText("Test already exists!")

        # 8. see if we have at least XX characters in the description.
        if self.Feedback.text() == "":
            self.description_length = len(self.description.toPlainText().replace(' ','').replace('\n', '').replace('\t', ''))
            if self.description_length < minimal_description_length:
                self.Feedback.setText(f"Describe the test in at least {minimal_description_length} characters (spaces don't count, you have {self.description_length} characters)")
        
        # 9. Check the input parameters
        if self.Feedback.text() == "":
            pass
        
        # 10. Check the output parameters
        if self.Feedback.text() == "":
            pass
        
        # 11. Enable/disable the OKButton
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
        test_type = "custom"

        self.project_info.add_test(name, hardware, base, test_type, test_data)        
        self.accept()

def new_test_dialog(project_info):
    newTestWizard = TestWizard(project_info)
    newTestWizard.exec_()
    del(newTestWizard)


def edit_test_dialog(project_info): #TODO: add the data still
    editTestWizard = TestWizard(project_info)
    editTestWizard.exec_()
    del(editTestWizard)

def new_standard_test_dialog(project_info): #TODO: move the standard test wizard here too !!!
    pass

def edit_standard_test_dialog(project_info): #TODO: does this make sense ?!?
    pass


if __name__ == '__main__':
    import sys, qdarkstyle
    from ATE.org.actions.dummy_main import DummyMainWindow

    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    dummyMainWindow = DummyMainWindow()
    dialog = TestWizard(dummyMainWindow)
    dummyMainWindow.register_dialog(dialog)
    sys.exit(app.exec_())
