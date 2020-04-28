# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 15:17:00 2020

@author: hoeren
"""

import sys
import qdarkstyle
from PyQt5 import QtGui, QtWidgets, QtCore

regex = "[+-]?[0-9]+(\\.[0-9]+)?([Ee][+-]?[0-9]+)?"


class TableWidgetItemDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self, regex, parent=None):
        QtWidgets.QStyledItemDelegate.__init__(self, parent)
        self.validator = QtGui.QRegExpValidator(QtCore.QRegExp(regex))

    def createEditor(self, parent, option, index):
        line_edit = QtWidgets.QLineEdit(parent)
        line_edit.setValidator(self.validator)
        return line_edit


class Table(QtWidgets.QDialog):
    def __init__(self,):
        super(Table, self).__init__()
        self.build_ui()
        self.show()

    def build_ui(self):       
        self.table_model = QtGui.QStandardItemModel(4, 2)
        self.delegate = TableWidgetItemDelegate(regex)
        self.table_view = QtWidgets.QTableView()
        self.table_view.setItemDelegateForColumn(0, self.delegate)
        self.table_view.setModel(self.table_model)

        self.setLayout(QtWidgets.QGridLayout())
        self.layout().addWidget(self.table_view)
        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    table = Table()
    res = app.exec_()

    sys.exit(res)
