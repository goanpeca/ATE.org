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

        self.existing_masksets = [''] + self.parent.project_info.get_masksets()
        self.existing_dies = self.parent.project_info.get_dies()
        self.existing_hardwares = self.parent.project_info.get_hardwares()
        if len(self.existing_hardwares)==0:
            self.existing_hardwares = ['']

        rxDieName = QtCore.QRegExp(valid_die_name_regex)
        DieName_validator = QtGui.QRegExpValidator(rxDieName, self)
        self.NewDieName.setText("")
        self.NewDieName.setValidator(DieName_validator)
        self.NewDieName.textChanged.connect(self.verify)

        self.FromMaskset.blockSignals(True)
        self.FromMaskset.clear()
        self.FromMaskset.addItems(self.existing_masksets)
        self.FromMaskset.setCurrentIndex(0) # this is the empty string !
        self.FromMaskset.currentIndexChanged.connect(self.verify)
        self.FromMaskset.blockSignals(False)

        self.WithHardware.blockSignals(True)
        self.WithHardware.clear()
        for index, hardware in enumerate(self.existing_hardwares):
            self.WithHardware.addItem(hardware)
            if hardware == self.parent.active_hw:
                self.WithHardware.setCurrentIndex(index)
        self.WithHardware.currentIndexChanged.connect(self.hardware_changed)
        self.WithHardware.blockSignals(False)

        self.Feedback.setText("No die name")
        self.Feedback.setStyleSheet('color: orange')

        self.CancelButton.clicked.connect(self.CancelButtonPressed)
        self.OKButton.clicked.connect(self.OKButtonPressed)
        self.OKButton.setEnabled(False)

        self.verify()
        self.show()

    def hardware_changed(self):
        '''
        if the selected hardware changes, make sure the active_hardware 
        at the parent level is also changed.
        '''
        self.parent.active_hw = self.WithHardware.currentText()

    def verify(self):
        if self.NewDieName.text() in self.existing_dies:
            self.Feedback.setText("Die name already exists !")
            self.OKButton.setEnabled(False)
        else:
            if self.FromMaskset.currentText() == "":
                self.Feedback.setText("No maskset selected")
                self.OKButton.setEnabled(False)
            else:
                self.Feedback.setText("")
                self.OKButton.setEnabled(True)

        #TODO: and the hardware ?!?


    def CancelButtonPressed(self):
        self.accept()

    def OKButtonPressed(self):
        name = self.NewDieName.text()
        maskset = self.FromMaskset.currentText()
        hardware = self.WithHardware.currentText()
        
        self.parent.project_info.add_die(name, maskset, hardware)
        self.parent.tree_update()
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
