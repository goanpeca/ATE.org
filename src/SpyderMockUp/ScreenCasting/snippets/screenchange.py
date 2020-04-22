#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 06:46:30 2020

@author: tom
"""

import sys

from PyQt5 import QtCore, QtGui, QtWidgets

import qdarkstyle


buttonx = 100
buttony = 32


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        self.setMinimumSize(QtCore.QSize(buttonx, buttony))
        self.setWindowTitle("Main Window") 

        self.button = QtWidgets.QPushButton('Center', self)
        self.button.clicked.connect(self.center)
        self.button.resize(buttonx, buttony)

    def center(self):
        print('center the main window')
        print(f"{self.size().width()}x{self.size().height()}")

    def resizeEvent(self, event):
        print('main window is resized')
        QtWidgets.QMainWindow.resizeEvent(self, event)
        self.button.move(int((self.size().width()-buttonx)/2),
                         int((self.size().height()-buttony)/2))        

    def moveEvent(self, event):
        print('main window is moved')
        QtWidgets.QMainWindow.moveEvent(self, event)

    def closeEvent(self, event):
        print('main window is closed')
        QtWidgets.QMainWindow.closeEvent(self, event)

    def changeEvent(self, event): # state change !!!
        print(f'main window state changed ({event.type()})')
        QtWidgets.QMainWindow.changeEvent(self, event)
        if event == QtCore.QEvent.WindowStateChange:
            if self.isMaximized():
                print('main window is maximized')
            elif self.isMinimized():
                print('main window is minimized')
                
        
        
        

    def screenchange(self):
        print('main window changed screen')



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())

