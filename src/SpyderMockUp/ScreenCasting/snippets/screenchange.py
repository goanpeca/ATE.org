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

def printQRect(message, QRect):
    print(f'{message} : ({QRect.x()}, {QRect.y()}) ({QRect.width()}x{QRect.height()})')

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self,  *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self,  *args, **kwargs)

        self.setMinimumSize(QtCore.QSize(buttonx, buttony))
        self.setWindowTitle("Main Window") 

        self.button = QtWidgets.QPushButton('Center', self)
        self.button.clicked.connect(self.center)
        self.button.resize(buttonx, buttony)
        
    def center(self):
        print('center the main window')
        screenRect = QtWidgets.QDesktopWidget().availableGeometry(self)
        printQRect(f'screen#{QtWidgets.QDesktopWidget().screenNumber(self)}', screenRect)
        windowRect = self.frameGeometry()
        printQRect('window', windowRect)
        self.move(int((screenRect.width()-windowRect.width())/2)+screenRect.x(), 
                  int((screenRect.height()-windowRect.height())/2)+screenRect.y())

    def resizeEvent(self, event):
        print('main window is resized')
        QtWidgets.QMainWindow.resizeEvent(self, event)
        self.button.move(int((self.size().width()-buttonx)/2),
                         int((self.size().height()-buttony)/2))        

    def moveEvent(self, event):
        print(f'main window is moved (screen={QtWidgets.QDesktopWidget().screenNumber(self)})')
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

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())

