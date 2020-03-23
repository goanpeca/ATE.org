'''
Created on Nov 20, 2019

@author: hoeren
'''
import os
import re

from PyQt5 import QtCore, QtGui, QtWidgets, uic

import qtawesome as qta

from ATE.org.validation import is_valid_maskset_name

standard_flat_height = 7 # mm
standard_scribe = 100 # um

class NewMasksetWizard(QtWidgets.QDialog):

    def __init__(self, parent):
        super().__init__()

        my_ui = __file__.replace('.py', '.ui')
        if not os.path.exists(my_ui):
            raise Exception("can not find %s" % my_ui)
        uic.loadUi(my_ui, self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle(' '.join(re.findall('.[^A-Z]*', os.path.basename(__file__).replace('.py', ''))))

        self.parent = parent

        from ATE.org.validation import valid_positive_integer_regex
        rxi = QtCore.QRegExp(valid_positive_integer_regex)
        positive_integer_validator = QtGui.QRegExpValidator(rxi, self)

        from ATE.org.validation import valid_positive_float_1_regex
        rxf = QtCore.QRegExp(valid_positive_float_1_regex)
        positive_float_validator = QtGui.QRegExpValidator(rxf, self)

        from ATE.org.validation import valid_maskset_name_regex
        rxMaskSetName = QtCore.QRegExp(valid_maskset_name_regex)
        MasksetName_validator = QtGui.QRegExpValidator(rxMaskSetName, self)

    # maskset
        self.masksetName.blockSignals(True)
        self.existing_masksets = self.parent.project_info.get_masksets()
        self.masksetName.setText("")
        self.masksetName.setValidator(MasksetName_validator)
        self.masksetName.textChanged.connect(self.nameChanged)
        self.masksetName.blockSignals(False)

    # Type & Customer
        self.Type.blockSignals(True)
        self.Type.setCurrentText('ASSP')
        self.Type.currentTextChanged.connect(self.typeChanged)
        self.Type.blockSignals(False)
        self.customerLabel.setVisible(False)
        self.customer.blockSignals(True)
        self.customer.setText('')
        self.customer.setVisible(False)
        self.customer.textChanged.connect(self.customerChanged)
        self.customer.blockSignals(False)

    # wafer diameter
        self.waferDiameter.blockSignals(True)
        self.waferDiameter.setCurrentIndex(self.waferDiameter.findText('200'))
        self.waferDiameter.currentTextChanged.connect(self.waferDiameterChanged)
        self.waferDiameter.blockSignals(False)
    
    # bondpads
        self.bondpads.blockSignals(True)
        self.bondpads.setMinimum(2)
        self.bondpads.setMaximum(99)
        self.bondpads.setValue(3)
        self.bondpads.valueChanged.connect(self.bondpadsChanged)
        self.bondpads.blockSignals(False)

    # die size X
        self.dieSizeX.blockSignals(True)
        self.dieSizeX.setText("")
        self.dieSizeX.setValidator(positive_integer_validator)
        self.dieSizeX.textChanged.connect(self.dieSizeXChanged)
        self.dieSizeX.blockSignals(False)

    # die size Y
        self.dieSizeY.blockSignals(True)
        self.dieSizeY.setText("")
        self.dieSizeY.setValidator(positive_integer_validator)
        self.dieSizeY.textChanged.connect(self.dieSizeYChanged)
        self.dieSizeY.blockSignals(False)

    # XY Flip Button
        self.XYFlipButton.blockSignals(True)
        self.XYFlipButton.setText("")
        self.XYFlipButton.setIcon(qta.icon('mdi.arrow-up-down', color='white'))
        self.XYFlipButton.clicked.connect(self.XYFlip)
        self.XYFlipButton.blockSignals(False)

    # die Ref X
        self.dieRefX.blockSignals(True)
        self.dieRefX.setText("")
        self.dieRefX.setValidator(positive_float_validator)
        self.dieRefX.textChanged.connect(self.dieRefXChanged)
        self.dieRefX.blockSignals(False)
    
    # die Ref Y
        self.dieRefY.blockSignals(True)
        self.dieRefY.setText("")
        self.dieRefY.setValidator(positive_float_validator)
        self.dieRefY.textChanged.connect(self.dieRefYChanged)
        self.dieRefY.blockSignals(False)
    
    # X Offset
        self.xOffset.blockSignals(True)
        self.xOffset.setText("0")
        self.xOffset.setValidator(positive_float_validator)
        self.xOffset.textChanged.connect(self.xOffsetChanged)
        self.xOffset.blockSignals(False)
        
    # Y Offset
        self.yOffset.blockSignals(True)
        self.yOffset.setText("0")
        self.yOffset.setValidator(positive_float_validator)
        self.yOffset.textChanged.connect(self.yOffsetChanged)
        self.yOffset.blockSignals(False)
    
    # scribe X
        self.scribeX.blockSignals(True)
        self.scribeX.setText(str(standard_scribe))
        self.scribeX.setValidator(positive_float_validator)
        self.scribeX.textChanged.connect(self.scribeXChanged)
        self.scribeX.blockSignals(False)

    # scribe Y
        self.scribeY.blockSignals(True)
        self.scribeY.setText(str(standard_scribe))
        self.scribeY.setValidator(positive_float_validator)
        self.scribeY.textChanged.connect(self.scribeYChanged)
        self.scribeY.blockSignals(False)

    # Flat
        WaferDiameter = int(self.waferDiameter.currentText())
        Flat = (WaferDiameter/2) - standard_flat_height
        if Flat-int(Flat) == 0:
            self.flat.setText(str(int(Flat)))
        else:
            self.flat.setText(str(Flat))    

    # Wafer Map Editor
        self.editWaferMapButton.clicked.connect(self.editWaferMap)

    # bondpad table
        self.bondpadTable.setRowCount(self.bondpads.value())
        #TODO: fromat the table better
        #TODO: the context menus on the table
        
    # view die button
        self.viewDieButton.setText("")
        self.viewDieButton.setIcon(qta.icon('mdi.eye-outline', color='white'))
        self.viewDieButton.clicked.connect(self.viewDie)
        
    # import For
        companies = ['', 'Micronas', 'InvenSense', 'IC-Sense', '...']
        self.importFor.clear()
        self.importFor.addItems(companies)
        self.importFor.setCurrentIndex(0) # empty string
        self.importFor.currentTextChanged.connect(self.importForChanged)

    # feedback    
        self.feedback.setText("")
        self.feedback.setStyleSheet('color: orange')

    # buttons
        self.OKButton.clicked.connect(self.OKButtonPressed)
        self.CancelButton.clicked.connect(self.CancelButtonPressed)

        self.validate()
        self.show()

    def nameChanged(self, MaskSetName):
        self.validate(MaskSetName)

    def typeChanged(self, SelectedType):
        if SelectedType == 'ASSP':
            self.customerLabel.setVisible(False)
            self.customer.blockSignals(True)
            self.customer.setText('')
            self.customer.setVisible(False)
            self.customer.blockSignals(False)
        else: # 'ASIC'
            self.customerLabel.setVisible(True)
            self.customer.blockSignals(True)
            self.customer.setText('')
            self.customer.setVisible(True)
            self.customer.blockSignals(False)

    def customerChanged(self, Customer):
        print(f"customer changed to {Customer}")
    
    def waferDiameterChanged(self, WaferDiameter):
        WaferDiameter = int(WaferDiameter)
        Flat = (WaferDiameter/2) - standard_flat_height
        if Flat-int(Flat) == 0:
            self.flat.setText(str(int(Flat)))
        else:
            self.flat.setText(str(Flat))
        self.validate()

    def bondpadsChanged(self, Bondpads):
        self.bondpadTable.setRowCount(Bondpads)
        self.validate()
        
    def dieSizeXChanged(self, DieSizeX):
        if DieSizeX != '':
            DieSizeX = int(DieSizeX)
            mid = int(DieSizeX)/2
            if mid-int(mid) == 0:
                self.dieRefX.setText(str(int(mid)))
            else:
                self.dieRefX.setText(str(mid))
        else:
            self.dieRefX.setText('')
        self.validate()

    def dieSizeYChanged(self, DieSizeY):
        if DieSizeY != '':
            DieSizeY = int(DieSizeY)
            mid = int(DieSizeY)/2
            if mid-int(mid) == 0:
                self.dieRefY.setText(str(int(mid)))
            else:
                self.dieRefY.setText(str(mid))
        else:
            self.dieRefY.setText('')
        self.validate()

    def XYFlip(self):
        old_die_size_x = self.DieSizeX.text()
        old_die_size_y = self.DieSizeY.text()
        old_die_ref_x = self.DieRefX.text()
        old_die_ref_y = self.DieRefY.text()
        
        self.DieSizeX.setText(old_die_size_y)
        self.DieSizeY.setText(old_die_size_x)
        self.DieRefX.setText(old_die_ref_y)
        self.DieRefY.setText(old_die_ref_x)

        # self.validate() # ?!?

    def dieRefXChanged(self, DieRefX):
        pass

    def dieRefYChanged(self, DieRefY):
        pass

    def xOffsetChanged(self, XOffset):
        pass
    
    def yOffsetChanged(self, YOffset):
        pass

    def scribeXChanged(self, ScribeX):
        pass
    
    def scribeYChanged(self, ScribeY):
        pass




    def importForChanged(self, Company):
        if Company == '':
            self.OKButton.setText("OK")
            self.validate()
        else:
            self.OKButton.setText("Import")
            self.OKButton.setEnabled(True)
            self.feedback.setText("About to import a MaskSet from the {self.importFor.currentText()} system")

    def validateTable(self):
        '''
        this method returns an 'error string' (that can be copied into the feedback line)
        if everything is ok, an empty string is returned.
        '''
        retval = ''
        #TODO: Implement the validation of the table
        return retval

    def validate(self, MaskSetName=''):
        self.feedback.setText('')
        # MasksetName
        if MaskSetName=='':
            MaskSetName = self.masksetName.text()
        if MaskSetName == "":
            self.feedback.setText("Supply a MaskSet name")
        else:
            if MaskSetName in self.existing_masksets:
                self.feedback.setText("MaskSet name already defined")
            if not is_valid_maskset_name(MaskSetName):
                self.feedback.setText("Invalid MaskSet name")
        # DieSizeX
        if self.feedback.text() == '':
            if self.dieSizeX.text() == '':
                self.feedback.setText("Supply a Die Size X value")
        
        # DieSizeY
        if self.feedback.text() == '':
            if self.dieSizeY.text() == '':
                self.feedback.setText("Supply a Die Size Y value")

        # DieRefX
        if self.feedback.text() == '':
            if self.dieRefX.text() == '':
                self.feedback.setText("Supply a Die Ref X value")

        # DieRefY
        if self.feedback.text() == '':
            if self.dieRefY.text() == '':
                self.feedback.setText("Supply a Die Ref Y value")

        # XOffset
        if self.feedback.text() == '':
            if self.xOffset.text() == '':
                self.feedback.setText("Supply an X Offset value")

        # YOffset
        if self.feedback.text() == '':
            if self.yOffset.text() == '':
                self.feedback.setText("Supply an Y Offset value")

        # ScribeX
        if self.feedback.text() == '':
            if self.scribeX.text() == '':
                self.feedback.setText("Supply a Scribe Size X value")

        # ScribeY
        if self.feedback.text() == '':
            if self.scribeY.text() == '':
                self.feedback.setText("Supply a Scribe Size Y value")

        # Flat
        if self.feedback.text() == '':
            if self.flat.text() == '':
                self.feedback.setText("Supply a Flat distance value")
        # Table
        if self.feedback.text() == '':
            retval = self.validateTable()
            if retval != '':
                self.feedback.setText(retval)

        if self.feedback.text() == "":
            self.OKButton.setEnabled(True)
        else:
            self.OKButton.setEnabled(False)

    def editWaferMap(self):
        print("Wafer Map Editor not yet implemented")
        #TODO: add the wafer map editor here

    def viewDie(self):
        print("Die Viewer not yet implemented")
        #TODO: add the die viewer (based ont the table here)

    def OKButtonPressed(self):
        if self.OKButton.text() == 'OK': 
            name = self.masksetName.text()
            if self.Type.currentText() == 'ASSP':
                customer = ''
            else: # 'ASIC' so need a customer !
                if self.customer.text()=='':
                    raise Exception("an ASIC *MUST* have a customer! (should not be able to get here!)")
                customer = self.customer.text()
            definition = {
                'WaferDiameter'       : int(self.waferDiameter.currentText()),
                'Bondpads'            : self.bondpads.value(),
                'DieSize'             : (int(self.dieSizeX.text()), int(self.dieSizeY.text())),
                'DieRef'              : (int(self.dieRefX.text()), int(self.dieRefY.text())),
                'Offset'              : (int(self.xOffset.text()), int(self.yOffset.text())),
                'Scribe'              : (int(self.scribeX.text()), int(self.scribeY.text())),
                'Flat'                : int(self.flat.text()),
                'BondpadTable' : {
                    1: ('bondpad1name', 100,      100,       90,      90),
                    2: ('bondpad2name', -100,     -100,      90,      90)                    
                    }, # implement bondpad table
                'Wafermap'     : {
                    'rim' : [(100, 80), (-80, -100)], # list of x- and y- coordinates of dies that are not to be tested (belong to rim)
                    'blank' : [(80, 80)], # list of x- and y- coordinates of dies that don't exist (blank silicon)
                    'test_insert' : [], # list of x- and y- coodinates of dies that don't exist (test inserts)
                    'unused' : [] # list of x- and y- coordinates of dies taht are not used (probing optimization ?)                     
                    }  # implement wafermap
                }
    
            self.parent.project_info.add_maskset(name, customer, definition)
            self.parent.update_tree()
            self.accept()

        else: # Import stuff
            #TODO: add the company specific plugins here
            print("Import stuff not implemented yet")
            
            self.importFor.setCurrentIndex(0)
            self.OKButton.setText("OK")
            self.validate()
            
    def CancelButtonPressed(self):
        self.accept()

def new_maskset_dialog(parent):
    newMasksetWizard = NewMasksetWizard(parent)
    newMasksetWizard.exec_()
    del(newMasksetWizard)

if __name__ == '__main__':
    import sys, qdarkstyle
    from ATE.org.actions.dummy_main import DummyMainWindow

    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    dummyMainWindow = DummyMainWindow()
    dialog = NewMasksetWizard(dummyMainWindow)
    dummyMainWindow.register_dialog(dialog)
    sys.exit(app.exec_())
