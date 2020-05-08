#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 06:46:30 2020

@author: tom
"""

import sys, os

from PyQt5 import QtCore, QtGui, QtWidgets

import qdarkstyle


buttonx = 100
buttony = 32


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self,  *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self,  *args, **kwargs)

        self.setMinimumSize(QtCore.QSize(buttonx, buttony))
        self.setWindowTitle("Main Window") 

        self.button = QtWidgets.QPushButton('Splash', self)
        self.button.clicked.connect(self.splash)
        self.button.resize(buttonx, buttony)
    
        self.splashscreen = QtWidgets.QSplashScreen(self)
        
        
        
        
            
    def getSplashCoordinates(self):
        '''
        this method will return the coordinates to put the splash screen
        in the middle of our MainWindow, the gif is a 500x500 image-sequence.
        return value is a QPoint (LeftTop)
        '''
        return QtCore.QPoint(100, 100)
        
    def splash(self):
        print('splash')
        








    def resizeEvent(self, event):
        print('main window is resized')
        QtWidgets.QMainWindow.resizeEvent(self, event)
        self.button.move(int((self.size().width()-buttonx)/2),
                         int((self.size().height()-buttony)/2))        


class CountDown(QtCore.QSplashScreen):
    
    def __init__(self, parent): # parent must be of type QScreenCast
        movie_name = os.path.join(os.path.dirname(__file__), 'countdown.gif')
        self.movie = QtGui.QMovie(movie_name)
        self.movie.jumpToFrame(0)
        pixmap = QtGui.QPixmap(self.movie.frameRect().size())
        super(CountDown, self).__init__(pixmap)
        self.movie.jumpToFrame(0)
        self.setParent(mainWindow)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | 
                            QtCore.Qt.FramelessWindowHint)
        self.setEnabled(False)
        self.movie.frameChanged.connect(self.repaint)
    
    def __call__(self):
        '''
        this is the entry point to do the countdown.
        '''
        self.parent().
        # get the parent (=mainwindow), put the 
        pass
    
    def showEvent(self, event):
        self.movie.start()
        super(CountDown, self).showEvent(event)

    def hideEvent(self, event):
        self.movie.stop()
        super(CountDown, self).hideEvent(event)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        pixmap = self.movie.currentPixmap()
        self.setMask(pixmap.mask())
        painter.drawPixmap(0, 0, pixmap)

    def sizeHint(self):
        return self.movie.scaledSize()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())

