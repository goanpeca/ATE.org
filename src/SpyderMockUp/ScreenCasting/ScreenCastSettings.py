# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 18:13:27 2019

@author: hoeren
"""
import os
import re

from ATE.org.actions import Create_ATE_Project
from ATE.org.listings import list_ATE_projects
from ATE.org.validation import is_valid_project_name
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QDialog


class ScreenCastSettings(QDialog):

    def __init__(self, parent):
        super(ScreenCastSettings, self).__init__()

        my_ui = __file__.replace('.py', '.ui')
        if not os.path.exists(my_ui):
            raise Exception("can not find %s" % my_ui)
        uic.loadUi(my_ui, self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle(' '.join(re.findall('.[^A-Z]*', os.path.basename(__file__).replace('.py', ''))))

        self.parent = parent
