'''
Created on Nov 18, 2019

@author: hoeren
'''
import os
import re

from PyQt5 import QtCore, QtGui, QtWidgets, uic

from ATE.org.validation import is_valid_project_name, valid_project_name_regex
from ATE.org.listings import list_ATE_projects


class ProjectWizard(QtWidgets.QDialog):

    def __init__(self, parent, navigator, title):
        super().__init__(parent)

        my_ui = __file__.replace('.py', '.ui')
        if not os.path.exists(my_ui):
            raise Exception("can not find %s" % my_ui)
        uic.loadUi(my_ui, self)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle(title)

        rxProjectName = QtCore.QRegExp(valid_project_name_regex)
        ProjectName_validator = QtGui.QRegExpValidator(rxProjectName, self)
        self.ProjectName.setValidator(ProjectName_validator)
        self.ProjectName.setText("")
        self.ProjectName.textChanged.connect(self.verify)

        self.existing_projects = navigator.list_ATE_projects(self.parent().workspace_path)

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
        self.project_name = self.ProjectName.text()
        self.project_quality = self.projectQuality.currentText()
        self.accept()

    def CancelButtonPressed(self):
        self.reject()


def NewProjectDialog(parent, navigator):
    newProjectWizard = ProjectWizard(parent, navigator, 'New Project Wizard')
    if newProjectWizard.exec_():  # OK button pressed
        project_name = newProjectWizard.project_name
        project_quality = newProjectWizard.project_quality
    else:
        project_name = ''
        project_quality = ''
    del(newProjectWizard)
    return project_name, project_quality


if __name__ == '__main__':
    import sys
    import qdarkstyle
    from ATE.org.actions.dummy_main import DummyMainWindow

    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    dummyMainWindow = DummyMainWindow()
    dialog = NewProjectWizard(dummyMainWindow)
    dummyMainWindow.register_dialog(dialog)
    sys.exit(app.exec_())
