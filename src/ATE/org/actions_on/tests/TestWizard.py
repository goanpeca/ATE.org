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
                                valid_max_float_regex,
                                valid_fmt_regex)

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
        self.nameDelegator = Delegator(valid_test_parameter_name_regex, self)

        self.fmtDelegator = Delegator(valid_fmt_regex, self)

        self.minDelegator = Delegator(valid_min_float_regex, self)
        self.defaultDelegator = Delegator(valid_default_float_regex, self)
        self.maxDelegator = Delegator(valid_max_float_regex, self)

        self.LSLDelegator = Delegator(valid_min_float_regex, self)
        self.LTLDelegator = Delegator(valid_min_float_regex, self)
        self.NomDelegator = Delegator(valid_default_float_regex, self)
        self.UTLDelegator = Delegator(valid_max_float_regex, self)
        self.USLDelegator = Delegator(valid_max_float_regex, self)
        
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
        
        self.inputParameterFormat.setIcon(qta.icon('mdi.settings', color='orange'))
        self.inputParameterFormat.setToolTip('Show parameter formats')
        self.inputParameterFormat.clicked.connect(self.toggleInputParameterFormatVisible)
        self.inputParameterFormatVisible = False
        
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
        self.inputParameterView.customContextMenuRequested.connect(self.inputParameterContextMenu)
        self.inputParameterView.selectionModel().selectionChanged.connect(self.inputParameterSelectionChanged) # https://doc.qt.io/qt-5/qitemselectionmodel.html

        self.inputParameterView.setItemDelegateForColumn(0, self.nameDelegator)
        self.inputParameterView.setItemDelegateForColumn(1, self.minDelegator)
        self.inputParameterView.setItemDelegateForColumn(2, self.defaultDelegator)
        self.inputParameterView.setItemDelegateForColumn(3, self.maxDelegator)
        self.inputParameterView.setItemDelegateForColumn(6, self.fmtDelegator)

        attributes = {'Shmoo' : True, 'Min' : -40, 'Default' : 25, 'Max' : 170, '10ᵡ' : '', 'Unit' : '°C', 'fmt' : '.0f'}        
        self.setInputParameter('Temperature', attributes)
        self.inputParameterView.setColumnHidden(6, True)
        self.inputParameterSelectionChanged()
        
    # OutputParametersTab
        self.outputParameterMoveUp.setIcon(qta.icon('mdi.arrow-up-bold-box-outline', color='orange'))
        self.outputParameterMoveUp.setToolTip('Move selected parameter Up')
        self.outputParameterMoveUp.clicked.connect(self.moveOutputParameterUp)

        self.outputParameterAdd.setIcon(qta.icon('mdi.plus-box-outline', color='orange'))
        self.outputParameterAdd.setToolTip('Add a parameter')
        self.outputParameterAdd.clicked.connect(self.addOutputParameter)

        self.outputParameterUnselect.setIcon(qta.icon('mdi.select-off', color='orange'))
        self.outputParameterUnselect.setToolTip('Clear selection')
        self.outputParameterUnselect.clicked.connect(self.unselectOutputParameter)
        
        self.outputParameterFormat.setIcon(qta.icon('mdi.settings', color='orange'))
        self.outputParameterFormat.setToolTip('Show parameter formats')
        self.outputParameterFormat.clicked.connect(self.toggleOutputParameterFormatVisible)
        self.outputParameterFormatVisible = False
        
        self.outputParameterMoveDown.setIcon(qta.icon('mdi.arrow-down-bold-box-outline', color='orange'))
        self.outputParameterMoveDown.setToolTip('Move selected parameter Down')
        self.outputParameterMoveDown.clicked.connect(self.moveOutputParameterDown)
        
        self.outputParameterDelete.setIcon(qta.icon('mdi.minus-box-outline', color='orange'))
        self.outputParameterDelete.setToolTip('Delete selected parameter')
        self.outputParameterDelete.clicked.connect(self.deleteOutputParameter)

        outputParameterHeaderLabels = ['Name', 'LSL', 'LTL', 'Nom', 'UTL', 'USL', '10ᵡ', 'Unit', 'fmt']
        self.outputParameterModel = QtGui.QStandardItemModel()
        self.outputParameterModel.setObjectName('outputParameters')
        self.outputParameterModel.setHorizontalHeaderLabels(outputParameterHeaderLabels)
        self.outputParameterModel.itemChanged.connect(self.outputParameterItemChanged) 

        self.outputParameterView.horizontalHeader().setVisible(True)
        self.outputParameterView.verticalHeader().setVisible(True)
        self.outputParameterView.setModel(self.outputParameterModel)
        self.outputParameterView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems) # https://doc.qt.io/qt-5/qabstractitemview.html#SelectionBehavior-enum
        self.outputParameterView.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection) # https://doc.qt.io/qt-5/qabstractitemview.html#SelectionMode-enum
        self.outputParameterView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu) # https://doc.qt.io/qt-5/qt.html#ContextMenuPolicy-enum
        self.outputParameterView.customContextMenuRequested.connect(self.outputParameterContextMenu)
        self.outputParameterView.selectionModel().selectionChanged.connect(self.outputParameterSelectionChanged) # https://doc.qt.io/qt-5/qitemselectionmodel.html

        {'LSL' :  5.0, 'LTL' :  9.0, 'Nom' : 10.0, 'UTL' : 11.0, 'USL' : 20.0, '10ᵡ' : 'k', 'Unit' : 'Hz', 'fmt' : '.1f'}

        self.outputParameterView.setItemDelegateForColumn(0, self.nameDelegator)
        self.outputParameterView.setItemDelegateForColumn(1, self.LSLDelegator)
        self.outputParameterView.setItemDelegateForColumn(2, self.LTLDelegator)
        self.outputParameterView.setItemDelegateForColumn(3, self.NomDelegator)
        self.outputParameterView.setItemDelegateForColumn(4, self.UTLDelegator)
        self.outputParameterView.setItemDelegateForColumn(5, self.USLDelegator)

        self.outputParameterView.setColumnHidden(8, True)
        self.outputParameterSelectionChanged()

        #TODO: Idea:
        #   limit the number of output parameters to 9, so we have a decade per test-number,
        #   and the '0' is the FTR 🙂

    # Tabs
        self.testTabs.currentChanged.connect(self.testTabChanged)
        self.testTabs.setTabEnabled(self.testTabs.indexOf(self.dependenciesTab), False)
        
    # buttons
        self.CancelButton.clicked.connect(self.CancelButtonPressed)
        self.OKButton.clicked.connect(self.OKButtonPressed)
        self.OKButton.setEnabled(False)

        self.show()
        self.resize(735, 400)     
        self.verify()
        
    def testTabChanged(self, activatedTabIndex):
        if activatedTabIndex == self.testTabs.indexOf(self.inputParametersTab):
            self.tableAdjust(self.inputParameterView)
        elif activatedTabIndex == self.testTabs.indexOf(self.outputParametersTab):
            self.tableAdjust(self.outputParameterView)
        else:
            pass

    def resizeEvent(self, event):
        QtWidgets.QWidget.resizeEvent(self, event)
        self.tableAdjust(self.inputParameterView)
        self.tableAdjust(self.outputParameterView)
        
    def tableAdjust(self, TableView):
        TableView.resizeColumnsToContents()
        autoVisibleWidth = 0
        for column in range(TableView.model().columnCount()):
            if column!=0:
                autoVisibleWidth+=TableView.columnWidth(column)
        vHeaderWidth = TableView.verticalHeader().width()
        availableWidth = TableView.geometry().width()
        nameWidth = availableWidth - vHeaderWidth - autoVisibleWidth - 6 # no clue where this '6' comes from, but it works
        TableView.setColumnWidth(0, nameWidth)
    
    def unitContextMenu(self, setter):
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
    
    def inputParameterContextMenu(self, point):
        '''
        here we select which context menu (for input_parameters) we need,
        based on the column where we activated the context menu on, and 
        dispatch to the appropriate context menu.
        '''
        index = self.inputParameterView.indexAt(point)
        col = index.column()
        row = index.row()
        formatSetter = self.setInputParameterFormat
        valueSetter = self.setInputParameterValue
        multiplierSetter = self.setInputParameterMultiplier
        unitSetter = self.setInputParameterUnit

        if col == 0 or col == 6: # Name or format
            if row != 0: # not for temperature
                menu = QtWidgets.QMenu(self)
                parameter_formats =[
                    ("6 decimal places float", lambda: formatSetter('.6f')),
                    ("3 decimal places float", lambda: formatSetter('.3f')),
                    ("2 decimal places float", lambda: formatSetter('.2f')),
                    ("1 decimal places float", lambda: formatSetter('.1f')),
                    ("0 decimal places float", lambda: formatSetter('.0f'))]
                
                for format_option in parameter_formats:
                    item = menu.addAction(format_option[0])
                    item.triggered.connect(format_option[1])
                menu.exec_(QtGui.QCursor.pos())

        elif index.column() >= 1 and index.column() <= 3: # Min, Default, Max
            if index.row() != 0: # not for temperature
                menu = QtWidgets.QMenu(self)
                special_values = [
                    ('+∞', lambda: valueSetter('+∞')),
                    ('0', lambda: valueSetter('0')), 
                    ('<clear>', lambda: valueSetter('')),
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
                
    def inputParameterItemChanged(self, item=None):
        '''
        if one of the cells in self.inputParameterModel is changed, this 
        routine is called, and it could be cause to re-size the table columns,
        and it could be cause to make a checkbox change.
        '''
        if isinstance(item, type(None)): # process the whole table
            rows = self.inputParameterModel.rowCount()
            for row in range(rows):
                name, attributes = self.getInputParameter(row)
                self.setInputParameter(name, attributes, row)
        else: # process only the one line
            row = item.row()
            name, attributes = self.getInputParameter(row)
            self.setInputParameter(name, attributes, row)

        # shmooed_parameters = 0
        # for item_row in range(self.inputParameterModel.rowCount()):
        #     name_item = self.inputParameterModel.item(item_row, 0)
        #     if name_item.checkState() == QtCore.Qt.Checked:
        #         shmooed_parameters+=1

        # if shmooed_parameters > 2:
        #     QtWidgets.QMessageBox.question(
        #         self, 
        #         'Warning', 
        #         'It is not advisable to have more than\n2 input parameters Shmoo-able.', 
        #         QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
       
        self.inputParameterView.clearSelection()

    def inputParameterSelectionChanged(self):
        '''
        here we enable the right buttons.
        '''
        selectedIndexes = self.inputParameterView.selectedIndexes()
        rowCount = self.inputParameterModel.rowCount()
        lastRow = rowCount - 1
        selectedRows = set()
        for index in selectedIndexes:
            selectedRows.add(index.row())
        numberOfSelectedRows = len(selectedRows)

        if numberOfSelectedRows == 0:
            self.inputParameterUnselect.setEnabled(False)
            self.inputParameterMoveUp.setEnabled(False)
            self.inputParameterDelete.setEnabled(False)
            self.inputParameterMoveDown.setEnabled(False)
        elif numberOfSelectedRows == 1:
            selectedRow = list(selectedRows)[0]
            self.inputParameterUnselect.setEnabled(True)
            if selectedRow > 1:
                self.inputParameterMoveUp.setEnabled(True)
            else:
                self.inputParameterMoveUp.setEnabled(False)
            self.inputParameterDelete.setEnabled(True)
            if selectedRow < lastRow:
                self.inputParameterMoveDown.setEnabled(True)
            else:
                self.inputParameterMoveDown.setEnabled(False)
        else:
            self.inputParameterUnselect.setEnabled(True)
            self.inputParameterMoveUp.setEnabled(False)
            self.inputParameterDelete.setEnabled(False)
            self.inputParameterMoveDown.setEnabled(False)

    def setInputParameterFormat(self, Format):
        index_selection = self.inputParameterView.selectedIndexes()
        
        for index in index_selection:
            if index.row()!=0: # not for 'Temperature'
                fmt_item = self.inputParameterModel.item(index.row(), 6)
                fmt_item.setData(Format, QtCore.Qt.DisplayRole)

        self.inputParameterView.clearSelection()

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
            elif value == '': # for multiplier and unit
                if index.row() != 0: # not for 'Temperature'
                    if index.column() in [4, 5]:
                        item = self.inputParameterModel.itemFromIndex(index)
                        item.setData(value, QtCore.Qt.DisplayRole)
            elif value == '0': # for min, default, max
                if index.row() != 0: # not for 'Temperature'
                    if index.column() in [1, 2, 3]:
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
                self.inputParameterModel.appendRow([QtGui.QStandardItem() for i in range(len(attributes))])
            item_row = 0
        else:
            if row == None: # append
                self.inputParameterModel.appendRow([QtGui.QStandardItem() for i in range(len(attributes))])
                item_row = rowCount
            else: # update
                if row > rowCount:
                    raise Exception(f"row({row}) > rowCount({rowCount})")
                item_row = row

        name_item = self.inputParameterModel.item(item_row, 0)
        min_item = self.inputParameterModel.item(item_row, 1)
        default_item = self.inputParameterModel.item(item_row, 2)
        max_item = self.inputParameterModel.item(item_row, 3)
        multiplier_item = self.inputParameterModel.item(item_row, 4)
        unit_item = self.inputParameterModel.item(item_row, 5)
        fmt_item = self.inputParameterModel.item(item_row, 6)               

        self.inputParameterModel.blockSignals(True)

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
            fmt_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)

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
        
        self.inputParameterModel.blockSignals(False)
        self.tableAdjust(self.inputParameterView)

    def setInputpParameters(self, definition):
        for name in definition:
            attributes = definition[name]
            self.setInputParameter(name, attributes)
    
    def getInputParameter(self, row):
        attributes = {'Shmoo' : None, 'Min' : None, 'Default' : None, 'Max' : None, '10ᵡ' : None, 'Unit' : None, 'fmt' : None}

        name_item = self.inputParameterModel.item(row, 0)

        if not isinstance(name_item, QtGui.QStandardItem):
            raise Exception("WTF")

        name = name_item.data(QtCore.Qt.DisplayRole)
        shmoo = name_item.data(QtCore.Qt.CheckStateRole)
        
        
        if shmoo == QtCore.Qt.Checked:
            attributes['Shmoo'] = True
        else:
            attributes['Shmoo'] = False

        fmt_item = self.inputParameterModel.item(row, 6)
        Fmt = fmt_item.data(QtCore.Qt.DisplayRole)
        attributes['fmt'] = Fmt

        min_item = self.inputParameterModel.item(row, 1)
        Min = min_item.data(QtCore.Qt.DisplayRole)
        if '∞' in Min:
            attributes['Min'] = -np.Inf
        else:
            Min = float(Min)
            attributes['Min'] = float(f"{Min:{Fmt}}")

        default_item = self.inputParameterModel.item(row, 2)
        Default = float(default_item.data(QtCore.Qt.DisplayRole))
        attributes['Default'] = float(f"{Default:{Fmt}}")

        max_item = self.inputParameterModel.item(row, 3)
        Max = max_item.data(QtCore.Qt.DisplayRole)
        if '∞' in Max:
            attributes['Max'] = np.Inf
        else:
            Max = float(Max)
            attributes['Max'] = float(f"{Max:{Fmt}}")

        multiplier_item = self.inputParameterModel.item(row, 4)        
        Multiplier = multiplier_item.data(QtCore.Qt.DisplayRole)
        attributes['10ᵡ'] = Multiplier
        
        unit_item = self.inputParameterModel.item(row, 5)
        Unit = unit_item.data(QtCore.Qt.DisplayRole)
        attributes['Unit'] = Unit
                
        return name, attributes
    
    def getInputParameters(self):
        retval = {}
        rows = self.inputParameterModel.rowCount()
        for row in range(rows):
            name, attributes = self.getInputParameter(row)
            retval[name] = attributes
        return retval

    def moveInputParameterUp(self):
        selectedIndexes = self.inputParameterView.selectedIndexes()
        selectedRows = set()
        for index in selectedIndexes:
            if index.row() not in selectedRows:
                selectedRows.add(index.row())
        if len(selectedRows) == 1: # can move only delete one parameter at a time!
            row = list(selectedRows)[0]        
            data = self.inputParameterModel.takeRow(row)
            self.inputParameterModel.insertRow(row-1, data)
            self.inputParameterView.clearSelection()
            self.inputParameterView.selectRow(row-1)
            
    def addInputParameter(self):
        new_row = self.inputParameterModel.rowCount()
        existing_parameters = []
        for item_row in range(new_row):
            item = self.inputParameterModel.item(item_row, 0)
            existing_parameters.append(item.text())

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
        name = f'new_parameter{new_parameter_index}'
        attributes = {'Shmoo' : False, 'Min' : '-∞', 'Default' : 0, 'Max' : '+∞', '10ᵡ' : '', 'Unit' : '?', 'fmt' : '.3f'}        
        self.setInputParameter(name, attributes)

    def unselectInputParameter(self):
        self.inputParameterView.clearSelection()
        
    def toggleInputParameterFormatVisible(self):
        if self.inputParameterFormatVisible:
            self.inputParameterFormat.setIcon(qta.icon('mdi.settings', color='orange'))
            self.inputParameterFormatVisible = False
            self.inputParameterFormat.setToolTip('Show parameter formats')
            self.inputParameterView.setColumnHidden(6, True)
        else:
            self.inputParameterFormat.setIcon(qta.icon('mdi.settings-outline', color='orange'))
            self.inputParameterFormatVisible = True
            self.inputParameterFormat.setToolTip('Hide parameter formats')
            self.inputParameterView.setColumnHidden(6, False)
        self.tableAdjust(self.inputParameterView)
        
    def deleteInputParameter(self):
        selectedIndexes = self.inputParameterView.selectedIndexes()
        selectedRows = set()
        for index in selectedIndexes:
            if index.row() not in selectedRows:
                selectedRows.add(index.row())
        if len(selectedRows) == 1: # can move only delete one parameter at a time!
            row = list(selectedRows)[0]        
            self.inputParameterModel.takeRow(row)
            self.inputParameterView.clearSelection()

    def moveInputParameterDown(self):
        selectedIndexes = self.inputParameterView.selectedIndexes()
        selectedRows = set()
        for index in selectedIndexes:
            if index.row() not in selectedRows:
                selectedRows.add(index.row())
        if len(selectedRows) == 1: # can move only delete one parameter at a time!
            row = list(selectedRows)[0]        
            data = self.inputParameterModel.takeRow(row)
            self.inputParameterModel.insertRow(row+1, data)
            self.inputParameterView.clearSelection()
            self.inputParameterView.selectRow(row+1)

    def outputParameterContextMenu(self, point):
        index = self.outputParameterView.indexAt(point)
        col = index.column()
        row = index.row()
        formatSetter = self.setOutputParameterFormat
        valueSetter = self.setOutputParameterValue
        multiplierSetter = self.setOutputParameterMultiplier
        unitSetter = self.setOutputParameterUnit

        if col == 0 or col == 8: # Name or format
            menu = QtWidgets.QMenu(self)
            parameter_formats =[
                ("6 decimal places float", lambda: formatSetter('.6f')),
                ("3 decimal places float", lambda: formatSetter('.3f')),
                ("2 decimal places float", lambda: formatSetter('.2f')),
                ("1 decimal places float", lambda: formatSetter('.1f')),
                ("0 decimal places float", lambda: formatSetter('.0f'))]
            
            for format_option in parameter_formats:
                item = menu.addAction(format_option[0])
                item.triggered.connect(format_option[1])
            menu.exec_(QtGui.QCursor.pos())

        elif index.column() >= 1 and index.column() <= 5: # LSL, (LTL), Nom, (UTL), USL
            menu = QtWidgets.QMenu(self)
            special_values = [
                ('+∞', lambda: valueSetter('+∞')),
                ('0', lambda: valueSetter('0')), 
                ('<clear>', lambda: valueSetter('')),
                ('-∞', lambda: valueSetter('-∞'))]
            for special_value in special_values:
                item = menu.addAction(special_value[0])
                item.triggered.connect(special_value[1])
            menu.exec_(QtGui.QCursor.pos())

        elif index.column() == 6: # multiplier --> reference = STDF V4.pdf @ page 50 & https://en.wikipedia.org/wiki/Order_of_magnitude
            menu = self.multiplierContextMenu(multiplierSetter)
            menu.exec_(QtGui.QCursor.pos())

        elif index.column() == 7: # Unit
            menu = self.unitContextMenu(unitSetter)
            menu.exec_(QtGui.QCursor.pos())

    def outputParameterItemChanged(self, item=None):
        if isinstance(item, type(None)): # process the whole table
            rows = self.outputParameterModel.rowCount()
            for row in range(rows):
                name, attributes = self.getOutputParameter(row)
                self.setOutputParameter(name, attributes, row)
        else: # process only the one line
            row = item.row()
            name, attributes = self.getOutputParameter(row)
            self.setOutputParameter(name, attributes, row)
       
        self.outputParameterView.clearSelection()
    
    def outputParameterSelectionChanged(self):
        '''
        here we enable the right buttons.
        '''
        selectedIndexes = self.outputParameterView.selectedIndexes()
        rowCount = self.outputParameterModel.rowCount()
        lastRow = rowCount - 1
        selectedRows = set()
        for index in selectedIndexes:
            selectedRows.add(index.row())
        numberOfSelectedRows = len(selectedRows)

        if numberOfSelectedRows == 0:
            self.outputParameterUnselect.setEnabled(False)
            self.outputParameterMoveUp.setEnabled(False)
            self.outputParameterDelete.setEnabled(False)
            self.outputParameterMoveDown.setEnabled(False)
        elif numberOfSelectedRows == 1:
            selectedRow = list(selectedRows)[0]
            self.outputParameterUnselect.setEnabled(True)
            if selectedRow > 1:
                self.outputParameterMoveUp.setEnabled(True)
            else:
                self.outputParameterMoveUp.setEnabled(False)
            self.outputParameterDelete.setEnabled(True)
            if selectedRow < lastRow:
                self.outputParameterMoveDown.setEnabled(True)
            else:
                self.outputParameterMoveDown.setEnabled(False)
        else:
            self.outputParameterUnselect.setEnabled(True)
            self.outputParameterMoveUp.setEnabled(False)
            self.outputParameterDelete.setEnabled(False)
            self.outputParameterMoveDown.setEnabled(False)
    
    def setOutputParameterFormat(self, Format):
        index_selection = self.outputParameterView.selectedIndexes()
        
        for index in index_selection:
            if index.column() == 8:
                fmt_item = self.outputParameterModel.item(index.row(), 8)
                fmt_item.setData(Format, QtCore.Qt.DisplayRole)
        self.outputParameterView.clearSelection()
    
    def setOutputParameterValue(self, Value):
        pass
    
    def setOutputParameterMultiplier(self, text, tooltip):
        selection = self.outputParameterView.selectedIndexes()
        
        for index in selection:
            if index.column() == 6: # multipliers are located in column#6 for output parameters
                self.outputParameterModel.setData(index, text, QtCore.Qt.DisplayRole)
                self.outputParameterModel.setData(index, tooltip, QtCore.Qt.ToolTipRole)
        self.outputParameterView.clearSelection()
    
    def setOutputParameterUnit(self, text, tooltip):
        selection = self.outputParameterView.selectedIndexes()
        
        for index in selection:
            if index.column() == 7: # units are located in column#7 for output parameters
                self.outputParameterModel.setData(index, text, QtCore.Qt.DisplayRole)
                self.outputParameterModel.setData(index, tooltip, QtCore.Qt.ToolTipRole)
        self.outputParameterView.clearSelection()
    
    def setOutputParameter(self, name, attributes, row=None):
        '''
        sets the outputParameter name and it's attribues
        if row==None, append to the list.
        if row is given, it **must** already exist!
        
        Structure (of all output parameters):
        output_parameters = {                          # https://docs.python.org/3.6/library/string.html#format-specification-mini-language
            'parameter1_name' : {'LSL' : -inf, 'LTL' : None, 'Nom' :    0, 'UTL' : None, 'USL' :  inf, '10ᵡ' :  '', 'Unit' :  'Ω', 'fmt' : '.3f'}, 
            'parameter2_name' : {'LSL' :  0.0, 'LTL' : None, 'Nom' :  3.5, 'UTL' : None, 'USL' :  2.5, '10ᵡ' : 'μ', 'Unit' :  'V', 'fmt' : '.3f'},
            'R_vdd_contact'   : {'LSL' :  5.0, 'LTL' :  9.0, 'Nom' : 10.0, 'UTL' : 11.0, 'USL' : 20.0, '10ᵡ' : 'k', 'Unit' : 'Hz', 'fmt' : '.1f'}}
        
        References:
            https://doc.qt.io/qt-5/qt.html#CheckState-enum
            https://doc.qt.io/qt-5/qt.html#ItemFlag-enum
            https://doc.qt.io/qt-5/qt.html#ItemDataRole-enum
            https://doc.qt.io/qt-5/qstandarditem.html
        '''
        print(f"setOutputParameter {name} = {attributes}")
        rowCount = self.outputParameterModel.rowCount()

        if row == None: # append
            self.outputParameterModel.appendRow([QtGui.QStandardItem() for i in range(9)])
            item_row = rowCount
        else: # update
            if row > rowCount:
                raise Exception(f"row({row}) > rowCount({rowCount})")
            item_row = row

        name_item = self.outputParameterModel.item(item_row, 0)
        LSL_item = self.outputParameterModel.item(item_row, 1)
        LTL_item = self.outputParameterModel.item(item_row, 2)
        Nom_item = self.outputParameterModel.item(item_row, 3)
        UTL_item = self.outputParameterModel.item(item_row, 4)
        USL_item = self.outputParameterModel.item(item_row, 5)
        multiplier_item = self.outputParameterModel.item(item_row, 6)
        unit_item = self.outputParameterModel.item(item_row, 7)
        fmt_item = self.outputParameterModel.item(item_row, 8)               

        self.outputParameterModel.blockSignals(True)

    # fmt
        if 'fmt' not in attributes:
            Fmt = '.3f'
        else:
            Fmt = attributes['fmt']
        fmt_item.setData(Fmt, QtCore.Qt.DisplayRole)
        fmt_item.setData(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter, QtCore.Qt.TextAlignmentRole)
        fmt_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)

    # LSL
        if isinstance(attributes['LSL'], type(None)):
            LSL_ = -np.inf
            LSL = '-∞'
        elif isinstance(attributes['LSL'], (float, int)):
            if abs(attributes['LSL']) == np.inf:
                LSL_ = -np.inf
                LSL = '-∞'
            elif attributes['LSL'] == float('nan'):
                LSL_ = -np.inf
                LSL = '-∞'
            else:
                LSL_ = float(attributes['LSL'])
                LSL = f"{LSL_:{Fmt}}"
        else:
            raise Exception("type(attribute['LSL']) = {type(attribute['LSL'])}, which is not (str, float or int) ... WTF?!?")
        LSL_item.setData(LSL, QtCore.Qt.DisplayRole)
        LSL_item.setData(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter, QtCore.Qt.TextAlignmentRole)
        LSL_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)

    # LTL
        print(f"{attributes['LTL']} == {float('nan')} --> {attributes['LTL'] == float('nan')}")
        if isinstance(attributes['LTL'], type(None)):
            LTL_ = float('nan')
            LTL = ''
        elif isinstance(attributes['LTL'], (float, int)):
            if abs(attributes['LTL']) == np.inf:
                LTL_ = -np.inf
                LTL = '-∞'
            elif attributes['LTL'] == float('nan'):
                LTL_ = float('nan')
                LTL = ''
            else:
                LTL_ = float(attributes['LTL'])
                LTL = f"{LTL_:{Fmt}}"
        else:
            raise Exception("type(attribute['LTL']) = {type(attribute['LTL'])}, which is not (None, float or int) ... WTF?!?")
        LTL_item.setData(LTL, QtCore.Qt.DisplayRole)
        LTL_item.setData(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter, QtCore.Qt.TextAlignmentRole)
        LTL_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)

    # USL
        if isinstance(attributes['USL'], type(None)):
            USL_ = np.inf
            USL = '+∞'
        elif isinstance(attributes['USL'], (float, int)):
            if abs(attributes['USL']) == np.inf:
                USL_ = np.inf
                USL = '+∞'
            elif attributes['USL'] == float('nan'):
                USL_ = np.inf
                USL = '+∞'
            else:
                USL_ = float(attributes['USL'])
                USL = f"{USL_:{Fmt}}"
        else:
            raise Exception("type(attribute['USL']) = {type(attribute['USL'])}, which is not (str, float or int) ... WTF?!?")
        USL_item.setData(USL, QtCore.Qt.DisplayRole)
        USL_item.setData(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, QtCore.Qt.TextAlignmentRole)
        USL_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)

    # UTL
        if isinstance(attributes['UTL'], type(None)):
            UTL_ = float('nan')
            UTL = ''
        elif isinstance(attributes['UTL'], (float, int)):
            if abs(attributes['UTL']) == np.inf:
                UTL_ = float('nan')
                UTL = ''
            elif attributes['UTL'] == float('nan'):
                UTL_ = float('nan')
                UTL = ''
            else:
                UTL_ = float(attributes['UTL'])
                UTL = f"{UTL_:{Fmt}}"
        else:
            raise Exception("type(attribute['UTL']) = {type(attribute['UTL'])}, which is not (None, float or int) ... WTF?!?")
        UTL_item.setData(UTL, QtCore.Qt.DisplayRole)
        UTL_item.setData(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter, QtCore.Qt.TextAlignmentRole)
        UTL_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)

    # Nom
        if isinstance(attributes['Nom'], type(None)):
            Nom_ = 0.0
        elif isinstance(attributes['Nom'], (float, int)):
            Nom_ = float(attributes['Nom'])
        else:
            raise Exception(f"type(attribute['Nom']) = {type(attributes['Nom'])}, which is not (float or int) ... WTF?!?")
        # complience to SL
        if LSL_ == -np.inf and USL_ == np.inf:
            if Nom_ == -np.inf or Nom_ == np.inf or Nom_ == float('nan'): Nom_ = 0.0
            if LTL_ == -np.inf and UTL_ == np.inf:
                pass
            elif LTL_ == -np.inf and UTL_ == float('nan'):
                pass
            elif LTL_ == -np.inf and UTL_ != float('nan') and UTL != np.inf:
                pass
            elif LTL_ == float('nan') and UTL_ == np.inf:
                pass
            elif LTL_ == float('nan') and UTL_ == float('nan'):
                pass
            elif LTL_ == float('nan') and (UTL_ != float('nan') and UTL_ != np.inf):
                pass
            elif (LTL_ != -np.inf and LTL_ != float('nan')) and UTL_ == np.inf:
                pass
            elif (LTL_ != -np.inf and LTL_ != float('nan')) and UTL_ == float('nan'):
                pass
            else:
                if Nom_ > UTL_: Nom_ = UTL_
                if Nom_ < LTL_: Nom_ = LTL_
        elif LSL_ == -np.inf:
            if Nom_ > USL_: Nom_ = USL_
            if LTL_ == -np.inf:
                pass
            elif LTL_ == float('nan'):
                pass
            else:
                pass
        elif USL_ == np.inf:
            if Nom_ < LSL_: Nom_ = LSL_
            if UTL_ == -np.inf:
                pass
            elif UTL_ == float('nan'):
                pass
            else:
                if Nom_ < LTL_: Nom_ = LTL_
        else:
            if Nom_ > USL_: Nom_ = USL_
            if Nom_ > UTL_: Nom_ = UTL_
            if Nom_ < LSL_: Nom_ = LSL_
            if Nom_ < LTL_: Nom_ = LTL_
        Nom = f"{Nom_:{Fmt}}"
        Nom_item.setData(Nom, QtCore.Qt.DisplayRole)
        Nom_item.setData(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter, QtCore.Qt.TextAlignmentRole)
        Nom_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)

    # name
        name_item.setData(name, QtCore.Qt.DisplayRole) # https://doc.qt.io/qt-5/qt.html#ItemDataRole-enum
        name_item.setData(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, QtCore.Qt.TextAlignmentRole)
        name_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)

    # Multiplier
        multiplier_item.setData(str(attributes['10ᵡ']), QtCore.Qt.DisplayRole)
        multiplier_item.setData(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter, QtCore.Qt.TextAlignmentRole)
        multiplier_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)
    # Unit
        unit_item.setData(str(attributes['Unit']), QtCore.Qt.DisplayRole)
        unit_item.setData(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, QtCore.Qt.TextAlignmentRole)
        unit_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)
        
        self.outputParameterModel.blockSignals(False)
        self.tableAdjust(self.outputParameterView)
    
    def setOuputParameters(self, definition):
        for name in definition:
            attributes = definition[name]
            self.setOutputParameter(name, attributes)

    def getOutputParameter(self, row):
        attributes = attributes = {'LSL' : None, 'LTL' : None, 'Nom' : None, 'UTL' : None, 'USL' : None, '10ᵡ' : '', 'Unit' : '', 'fmt' : ''}

        name_item = self.outputParameterModel.item(row, 0)
        name = name_item.data(QtCore.Qt.DisplayRole)

        LSL_item = self.outputParameterModel.item(row, 1)
        attributes['LSL'] = LSL_item.data(QtCore.Qt.DisplayRole)

        LTL_item = self.outputParameterModel.item(row, 2)
        attributes['LTL'] = float(LTL_item.data(QtCore.Qt.DisplayRole))

        Nom_item = self.outputParameterModel.item(row, 3)
        attributes['Nom'] = float(Nom_item.data(QtCore.Qt.DisplayRole))

        UTL_item = self.outputParameterModel.item(row, 4)
        attributes['UTL'] = float(UTL_item.data(QtCore.Qt.DisplayRole))

        USL_item = self.outputParameterModel.item(row, 5)
        attributes['USL'] = float(USL_item.data(QtCore.Qt.DisplayRole))

        multiplier_item = self.outputParameterModel.item(row, 6)
        attributes['10ᵡ'] = multiplier_item.data(QtCore.Qt.DisplayRole)

        unit_item = self.outputParameterModel.item(row, 7)
        attributes['Unit'] = unit_item.data(QtCore.Qt.DisplayRole)

        fmt_item = self.outputParameterModel.item(row, 8)               
        attributes['fmt'] = fmt_item.data(QtCore.Qt.DisplayRole)
                
        return name, attributes
    
    def getOutputParameters(self):
        retval = {}
        rows = self.outputParameterModel.rowCount()
        for row in range(rows):
            name, attributes = self.getoutputParameter(row)
            retval[name] = attributes
        return retval
    
    def moveOutputParameterUp(self, row):
        selectedIndexes = self.outputParameterView.selectedIndexes()
        selectedRows = set()
        for index in selectedIndexes:
            if index.row() not in selectedRows:
                selectedRows.add(index.row())
        if len(selectedRows) == 1: # can move only delete one parameter at a time!
            row = list(selectedRows)[0]        
            data = self.outputParameterModel.takeRow(row)
            self.outputParameterModel.insertRow(row-1, data)
            self.outputParameterView.clearSelection()
            self.outputParameterView.selectRow(row-1)
    
    def addOutputParameter(self):
        new_row = self.outputParameterModel.rowCount()
        existing_parameters = []
        for item_row in range(new_row):
            item = self.outputParameterModel.item(item_row, 0)
            existing_parameters.append(item.text())

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
        name = f'new_parameter{new_parameter_index}'
        attributes = {'LSL' :  -np.inf, 'LTL' : '', 'Nom' : 3.14, 'UTL' : '', 'USL' : np.inf, '10ᵡ' : '', 'Unit' : '?', 'fmt' : '.3f'}        
        self.setOutputParameter(name, attributes)
    
    def unselectOutputParameter(self):
        self.outputParameterView.clearSelection()
    
    def toggleOutputParameterFormatVisible(self):
        if self.outputParameterFormatVisible:
            self.outputParameterFormat.setIcon(qta.icon('mdi.settings', color='orange'))
            self.outputParameterFormatVisible = False
            self.outputParameterFormat.setToolTip('Show parameter formats')
            self.outputParameterView.setColumnHidden(8, True)
        else:
            self.outputParameterFormat.setIcon(qta.icon('mdi.settings-outline', color='orange'))
            self.outputParameterFormatVisible = True
            self.outputParameterFormat.setToolTip('Hide parameter formats')
            self.outputParameterView.setColumnHidden(8, False)
        self.tableAdjust(self.outputParameterView)
    
    def deleteOutputParameter(self, row):
        selectedIndexes = self.outputParameterView.selectedIndexes()
        selectedRows = set()
        for index in selectedIndexes:
            if index.row() not in selectedRows:
                selectedRows.add(index.row())
        if len(selectedRows) == 1: # can move only delete one parameter at a time!
            row = list(selectedRows)[0]        
            self.outputParameterModel.takeRow(row)
            self.outputParameterView.clearSelection()
    
    def moveOutputParameterDown(self, row):
        selectedIndexes = self.outputParameterView.selectedIndexes()
        selectedRows = set()
        for index in selectedIndexes:
            if index.row() not in selectedRows:
                selectedRows.add(index.row())
        if len(selectedRows) == 1: # can move only delete one parameter at a time!
            row = list(selectedRows)[0]        
            data = self.outputParameterModel.takeRow(row)
            self.outputParameterModel.insertRow(row+1, data)
            self.outputParameterView.clearSelection()
            self.outputParameterView.selectRow(row+1)
    
    def getDescription(self):
        return self.description.toPlainText().split('\n')
    
    def descriptionLength(self):
        retval = ''.join(self.getDescription(), '\n').replace(' ', '').replace('\n', '').replace('\t', '')
        return len(retval)

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
        self.reject()

    def OKButtonPressed(self):
        name = self.TestName.text()
        hardware = self.ForHardwareSetup.currentText()
        base = self.WithBase.currentText()
        test_data = {'input_parameters' : {},
                     'output_parameters' : {}}
        test_type = "custom"

        # self.project_info.add_test(name, hardware, base, test_type, test_data)        
        self.accept()

class NewStandardTestWizard(QtWidgets.QDialog):

    def __init__(self, project_info, fixed=True):
        super().__init__()

        my_ui = __file__.replace('.py', '.ui')
        if not os.path.exists(my_ui):
            raise Exception("can not find %s" % my_ui)
        uic.loadUi(my_ui, self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle(' '.join(re.findall('.[^A-Z]*', os.path.basename(__file__).replace('.py', ''))))

        self.project_info = project_info

    # ForHardwareSetup ComboBox
        self.existing_hardwaresetups = self.project_info.get_available_hardwares()
        self.ForHardwareSetup.blockSignals(True)
        self.ForHardwareSetup.clear()
        self.ForHardwareSetup.addItems(self.existing_hardwaresetups)
        # TODO: fix this
        self.ForHardwareSetup.setCurrentIndex(self.ForHardwareSetup.findText(self.project_info.active_hardware))
        # TODO: 
        # self.ForHardwareSetup.setDisabled(fixed)
        self.ForHardwareSetup.setDisabled(False)
        self.ForHardwareSetup.currentTextChanged.connect(self._verify)
        self.ForHardwareSetup.blockSignals(False)
        
    # WithBase ComboBox
        self.WithBase.blockSignals(True)
        self.WithBase.clear()
        self.WithBase.addItems(['PR', 'FT'])
        # TODO: fix this
        self.WithBase.setCurrentIndex(self.WithBase.findText(self.project_info.active_base))
        # self.WithBase.setDisabled(fixed)
        self.WithBase.setDisabled(False)
        self.WithBase.currentTextChanged.connect(self._verify)
        self.WithBase.blockSignals(False)

    # StandardTestName ComboBox
        self.model = QtGui.QStandardItemModel()
    
        from ATE.org.coding.standard_tests import names as standard_test_names
        existing_standard_test_names = \
            self.project_info.tests_get_standard_tests(
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
        self.StandardTestName.currentTextChanged.connect(self._verify)            
        self.StandardTestName.blockSignals(False)

    # feedback
        self.feedback.setText("")
        self.feedback.setStyleSheet('color: orange')

    # buttons
        self.CancelButton.clicked.connect(self.CancelButtonPressed)
        self.OKButton.clicked.connect(self.OKButtonPressed)
        self.OKButton.setEnabled(False)

    # go
        self._verify()
        self.show()
        
        
    def _verify(self):
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
        self.reject()

    def OKButtonPressed(self):
        name = self.StandardTestName.currentText()
        hardware = self.ForHardwareSetup.currentText()
        type = 'standard'
        base = self.WithBase.currentText()
        definition = {'doc_string': [], # list of lines
                      'input_parameters': {},
                      'output_parameters': {}}

        self.project_info.standard_test_add(name, hardware, base)
        self.accept()


def new_test_dialog(project_info):
    newTestWizard = TestWizard(project_info)
    if newTestWizard.exec_(): # OK button pressed, thus exited with accept() and **NOT** with reject()
        test_name = newTestWizard.TestName.text()
        hardware = newTestWizard.ForHardwareSetup.currentText()
        base = newTestWizard.WithBase.currentText()
        input_parameters = newTestWizard.get<s()
        output_parameters = newTestWizard.getOutputParameters()
        doc_string =  newTestWizard.getDescription()
        dependencies = newTestWizard.getDependencies()
        
    
    
    del(newTestWizard)


def edit_test_dialog(project_info): #TODO: add the data still
    editTestWizard = TestWizard(project_info)
    editTestWizard.exec_()
    del(editTestWizard)

def new_standard_test_dialog(project_info): #TODO: move the standard test wizard here too !!!
    pass

def edit_standard_test_dialog(project_info): #TODO: does this make sense ?!? -->yes,open with TestWizard
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
