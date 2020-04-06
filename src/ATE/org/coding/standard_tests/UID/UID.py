# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 16:44:18 2020

@author: hoeren
"""
import os

from PyQt5 import QtCore, QtGui, QtWidgets, uic

def generator(parent, definition):
    if definition != {}:
        from ATE.org.coding import test_generator

        project_path = parent.active_project_path
        hardware = parent.active_hardware
        base = parent.active_base
        
        my_name = '.'.join(os.path.basename(__file__).split('.')[:-1])
    
        return test_generator(project_path, my_name, hardware, base, definition, Type='standard')

class Wizard(QtWidgets.QDialog):

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
        self.setWindowTitle('UID')
        self.base = self.parent.project_info.active_base
        self.hardware = self.parent.project_info.active_hardware
        
        if self.base == 'FT':
            my_target = 'device'
        else:
            my_target = 'die'
        
        self.definition = {
            'doc_string' : [
                f'The UID (Unique IDentification) test will read out the UID from the {my_target}',
                f'using {self.hardware} and add it to the STDF in the right place.'],
            'input_parameters' : {},
            'output_parameters' : {},
            'data' : {}
        }
        
    def verify(self):
        self.feedback.setText("")

    def OKButtonPressed(self):
        self.accept()
        return self.definition

    def CancelButtonPressed(self):
        self.accept()
        return {}


def dialog(parent):
    wizard = Wizard(parent)
    definition = wizard.exec_()
    del(wizard)
    generator(parent, definition)

if __name__ == "__main__":
    pass
    # from ATE.org.navigation import project_navigator, run_dummy_main
    
    # project_info = project_navigator(r'C:\Users\hoeren\__spyder_workspace__\BROL')
    # run_dummy_main(project_info, DieWizard)
