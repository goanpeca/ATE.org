'''
Created on Nov 20, 2019

@author: hoeren
'''
import os
import re

from PyQt5 import QtCore, QtGui, QtWidgets, uic

from ATE.org.validation import is_valid_maskset_name

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

        self.existing_masksets = self.parent.project_info.get_masksets()

        from ATE.org.validation import valid_integer_regex
        rxi = QtCore.QRegExp(valid_integer_regex)
        integer_validator = QtGui.QRegExpValidator(rxi, self)
        from ATE.org.validation import valid_maskset_name_regex
        rxMaskSetName = QtCore.QRegExp(valid_maskset_name_regex)
        MasksetName_validator = QtGui.QRegExpValidator(rxMaskSetName, self)

        self.MasksetName.setText("")
        self.MasksetName.setValidator(MasksetName_validator)
        self.MasksetName.textChanged.connect(self.validate)

        self.WaferDiameter.setText("200")
        self.WaferDiameter.setValidator(integer_validator)
        self.WaferDiameter.textChanged.connect(self.validate)

        self.Bondpads.setValidator(integer_validator)
        self.Bondpads.textChanged.connect(self.validate)

        self.DieSizeX.setValidator(integer_validator)
        self.DieSizeX.textChanged.connect(self.validate)

        self.DieSizeY.setValidator(integer_validator)
        self.DieSizeY.textChanged.connect(self.validate)

        self.ScribeX.setValidator(integer_validator)
        self.ScribeX.textChanged.connect(self.validate)

        self.ScribeY.setValidator(integer_validator)
        self.ScribeY.textChanged.connect(self.validate)

        #TODO: self.NewMasksetTableView

        self.Feedback.setText("")
        self.Feedback.setStyleSheet('color: orange')

        self.OKButton.clicked.connect(self.OKButtonPressed)
        self.CancelButton.clicked.connect(self.CancelButtonPressed)

        self.validate()
        self.show()

    def validate(self):

        feedback = ""

        maskset_name = self.MasksetName.text()
        if maskset_name == "":
            feedback = "Invalid maskset name"
        else:
            if maskset_name in self.existing_masksets:
                feedback = "maskset already defined"
            if not is_valid_maskset_name(maskset_name):
                feedback = "Invalid maskset name"

        number_of_bond_pads = self.Bondpads.text()
        if number_of_bond_pads == "" and feedback == "":
            feedback = "No valid number of bond pads"

        die_size_x = self.DieSizeX.text()
        if die_size_x == ""  and feedback == "":
            feedback = "No valid die size X"

        die_size_y = self.DieSizeY.text()
        if die_size_y == ""  and feedback == "":
            feedback = "No valid die size Y"

        scribe_x = self.ScribeX.text()
        if scribe_x == "" and feedback == "":
            feedback = "No valid scribe X"

        scribe_y = self.ScribeY.text()
        if scribe_y == "" and feedback == "":
            feedback = "No valid scribe Y"

        self.Feedback.setText(feedback)
        if feedback == "":
            self.OKButton.setEnabled(True)
        else:
            self.OKButton.setEnabled(False)

    def OKButtonPressed(self):
        name = self.MasksetName.text()
        definition = {
            'number_of_bond_pads' : int(self.Bondpads.text()),
            'die_size_x'          : int(self.DieSizeX.text()),
            'die_size_y'          : int(self.DieSizeY.text()),
            'scribe_x'            : int(self.ScribeX.text()),
            'scribe_y'            : int(self.ScribeY.text()),
            #            pinNr  Name           xcoord    ycoord     xsize    ysize
            'bond_pads' : {1: ('bondpad1name', 100,      100,       90,      90),
                           2: ('bondpad2name', -100,     -100,      90,      90)
                          #TODO: recuperate above info from wizard
                           },
            'rotation_to_flat' : 0
            #TODO: add the rotation (0, 90, 180, 270) to the ui
            }

        self.parent.project_info.add_maskset(name, definition)
        self.parent.update_tree()
        self.accept()

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
