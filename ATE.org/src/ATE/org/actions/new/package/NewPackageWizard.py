# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 18:18:41 2019

@author: hoeren
"""
import os
import pickle
import re

from ATE.org.listings import dict_project_paths, list_packages
from ATE.org.validation import (
    is_ATE_project,
    valid_integer_regex,
    valid_package_name_regex
)
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
        
        self.existing_packages = self.parent.project_info.get_packages()

        rxi = QtCore.QRegExp(valid_integer_regex)
        integer_validator = QtGui.QRegExpValidator(rxi, self)
        rxPackageName = QtCore.QRegExp(valid_package_name_regex)
        package_validator = QtGui.QRegExpValidator(rxPackageName, self)

        self.PackageName.setValidator(package_validator)
        self.PackageName.textChanged.connect(self.validate)

        self.Pins.setValidator(integer_validator)
        self.Pins.textChanged.connect(self.validate)

        # self.PinListTableView

        self.Feedback.setText("")
        self.Feedback.setStyleSheet('color: orange')

        self.OKButton.clicked.connect(self.OKButtonPressed)
        self.CancelButton.clicked.connect(self.CancelButtonPressed)

        self.validate()
        self.show()

    def validate(self):

        feedback = ""

        package_name = self.PackageName.text()
        if package_name == "":
            feedback = "invalid package name"
        else:
            if package_name in self.existing_packages:
                feedback = "Package already defined"

        number_of_pins = self.Pins.text()
        if number_of_pins == "" and feedback == "":
            feedback = "invalid number of pins"

        self.Feedback.setText(feedback)
        if feedback == "":
            self.OKButton.setEnabled(True)
        else:
            self.OKButton.setEnabled(False)

    def OKButtonPressed(self):
        name = self.PackageName.text()
        definition = {'number_of_pins' : int(self.Pins.text()),
                      'area'           : {} #TODO: work out further
                     }
        
        self.parent.project_info.add_package(name, definition)
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
