# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 14:43:48 2020

@author: hoeren
"""

from PyQt5 import QtWidgets, QtGui, QtCore

regex = r"[+]?\d*\.?\d?"


class TableWidgetItem(QtWidgets.QTableWidgetItem):
    
    def __init__(self, regex):
        self.setValidator(regex)
        self.old_text = ''
        self.text = ''
    
    def setValidator(self, regex):
        self.validator = QtGui.QRegExpValidator(QtCore.QRegExp(regex))
    
    def setText(self, text):
        v = self.validator.validate(text, len(text))[0]
        print(v)
        if v != QtGui.QValidator.Invalid:
            self.text = text
        else:
            self.text = self.old_text

if __name__ == '__main__':
    tableWidgetItem = TableWidgetItem(regex)
    tableWidgetItem.setText('fubar')
    print(tableWidgetItem.text)
    tableWidgetItem.setText('3.14')
    print(tableWidgetItem.text)