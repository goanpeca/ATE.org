# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 18:18:41 2019

@author: hoeren
"""
import os
import shutil
import re
import tempfile

from ATE.org.validation import valid_package_name_regex

from PyQt5 import QtCore, QtGui, QtWidgets, uic

class NewPackageWizard(QtWidgets.QDialog):

    def __init__(self, parent):
        super(NewPackageWizard, self).__init__()

        my_ui = __file__.replace('.py', '.ui')
        if not os.path.exists(my_ui):
            raise Exception("can not find %s" % my_ui)
        uic.loadUi(my_ui, self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle(' '.join(re.findall('.[^A-Z]*', os.path.basename(__file__).replace('.py', ''))))

        self.parent = parent
        
        self.temp_dir = tempfile.mkdtemp()
        self.temp_drawing = None
        
        rxPackageName = QtCore.QRegExp(valid_package_name_regex)
        PackageName_validator = QtGui.QRegExpValidator(rxPackageName, self)

        self.existing_packages = self.parent.project_info.get_packages()

        self.PackageName.setValidator(PackageName_validator)
        self.PackageName.textChanged.connect(self.validate)

        self.isNakedDie.setChecked(False)
        self.isNakedDie.toggled.connect(self.NakedDieChanged)

        self.leads.setMinimum(2)
        self.leads.setMaximum(99)
        self.leads.setValue(3)

        self.DrawingGroup.setVisible(False)

        self.drawingLabel.setText("N/A")
        
        self.findOnFilesystem.clicked.connect(self.FindOnFileSystem)

        companies = ['', 'Micronas', 'InvenSense', 'IC-Sense', '...']
        self.importFor.clear()
        self.importFor.addItems(companies)
        self.importFor.setCurrentIndex(0) # empty string
        self.importFor.currentTextChanged.connect(self.importForChanged)

        self.doImport.setEnabled(False)
        self.doImport.clicked.connect(self.doImportFor)        
        
        self.Feedback.setText("")
        self.Feedback.setStyleSheet('color: orange')

        self.OKButton.clicked.connect(self.OKButtonPressed)
        self.CancelButton.clicked.connect(self.CancelButtonPressed)

        self.validate()
        self.show()

    def __del__(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def NakedDieChanged(self, State):
        print(f"NakedDieChanged : {State} ({type(State)})")

    def FindOnFileSystem(self):
        print("Find On File System not yet implemented")

    def importForChanged(self, Company):
        if Company == '':
            self.doImport.setEnabled(False)
            self.validate()
        else:
            self.doImport.setEnabled(True)
            self.OKButton.setEnabled(False)

    def doImportFor(self):
        '''
        this method will find (per company) somehow the drawings for 
        the package and save it in the self.temp_dir directory with the 
        name of the package with the .png extension.
        upon OK button, this file is copied in ~/src/drawings/packages.
        '''
        
        #TODO: Implement, save the file in self.temp_dir under the name of the package !!!
        
        self.importFor.setCurrentIndex(0) # empty
        self.drawingLabel.setText(f"imported for '{self.importFor.currentText()}'")
        self.doImport.setEnabled(False)

    def validate(self):
        self.Feedback = ''
        
        package_name = self.PackageName.text()
        if package_name == "":
            self.Feedback = "Supply a name for the Package"
            self.DrawingGroup.setVisible(False)
        else:
            if package_name in self.existing_packages:
                self.Feedback = "Package already defined"
            else:
                self.DrawingGroup.setVisible(True)

        if self.Feedback == "":
            self.OKButton.setEnabled(True)
        else:
            self.OKButton.setEnabled(False)

    def OKButtonPressed(self):
        pname = self.PackageName.text()
        if self.isNakedDie.isChecked():
            ptype = 'naked'
        else:
            ptype = 'regular'
        pleads = self.leads.value()
        
        self.parent.project_info.add_package(pname, ptype, pleads)

        self.parent.update_tree()
        self.accept()

    def CancelButtonPressed(self):
        self.accept()

def new_package_dialog(parent):
    newPackageWizard = NewPackageWizard(parent)
    newPackageWizard.exec_()
    del(newPackageWizard)

if __name__ == '__main__':
    import sys, qdarkstyle
    from ATE.org.actions.dummy_main import DummyMainWindow

    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    dummyMainWindow = DummyMainWindow()
    dialog = NewPackageWizard(dummyMainWindow)
    dummyMainWindow.register_dialog(dialog)
    sys.exit(app.exec_())
