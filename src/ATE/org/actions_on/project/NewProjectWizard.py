'''
Created on Nov 18, 2019

@author: hoeren
'''
import os
import re

from PyQt5 import QtCore, QtGui, QtWidgets, uic

from ATE.org.validation import is_valid_project_name, valid_project_name_regex
from ATE.org.listings import list_ATE_projects

class NewProjectWizard(QtWidgets.QDialog):

    def __init__(self, parent):
        self.parent = parent
        super().__init__()
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        my_ui = __file__.replace('.py', '.ui')
        if not os.path.exists(my_ui):
            raise Exception("can not find %s" % my_ui)
        uic.loadUi(my_ui, self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle(' '.join(re.findall('.[^A-Z]*', os.path.basename(__file__).replace('.py', ''))))


        rxProjectName = QtCore.QRegExp(valid_project_name_regex)
        ProjectName_validator = QtGui.QRegExpValidator(rxProjectName, self)
        self.ProjectName.setValidator(ProjectName_validator)
        self.ProjectName.setText("")
        self.ProjectName.textChanged.connect(self.verify)
        # self.ProjectName.returnPressed.connect(self.PressedEnter)

        self.existing_projects = list_ATE_projects(self.parent.workspace_path)

        self.Feedback.setStyleSheet('color: orange')

        self.OKButton.clicked.connect(self.OKButtonPressed)
        self.CancelButton.clicked.connect(self.CancelButtonPressed)

        self.verify()
        self.show()

    def verify(self):
        feedback = ""

        project_name = self.ProjectName.text()
        if project_name == "":
            feedback = "Invalid project name"
        elif project_name in self.existing_projects:
            feedback = "project already defined"
        else:
            if not is_valid_project_name(project_name):
                feedback = "Invalid project name"

        self.Feedback.setText(feedback)

        if feedback == "":
            self.OKButton.setEnabled(True)
        else:
            self.OKButton.setEnabled(False)

    def OKButtonPressed(self):
        project_name = self.ProjectName.text()
        #switch the parent to this new project
        self.parent.active_project = project_name
        self.parent.active_project_path = os.path.join(self.parent.workspace_path, self.parent.active_project)
        
        if self.parent.project_info is None:
            from ATE.org.navigation import project_navigator
            self.parent.project_info = project_navigator(self.parent.active_project_path)
            
        else:
            self.parent.project_info(self.parent.active_project_path)
        self.parent.update_tree()      
        self.accept()

    def CancelButtonPressed(self):
        self.accept()



def new_project_dialog(parent):
    newProjectWizard = NewProjectWizard(parent)
    newProjectWizard.exec_()
    del(newProjectWizard)

if __name__ == '__main__':
    import sys, qdarkstyle
    from ATE.org.actions.dummy_main import DummyMainWindow

    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    dummyMainWindow = DummyMainWindow()
    dialog = NewProjectWizard(dummyMainWindow)
    dummyMainWindow.register_dialog(dialog)
    sys.exit(app.exec_())
