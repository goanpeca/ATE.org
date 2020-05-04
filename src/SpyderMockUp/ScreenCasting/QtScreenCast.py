# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 18:13:27 2019

@author: hoeren

hints:
    
    Window Geometry:
        https://doc.qt.io/qt-5/application-windows.html#window-geometry

    Splash:    
        QMovie *movie = new QMovie(":/images/other/images/16x16/loading.gif");
        QLabel *processLabel = new QLabel(this);
        processLabel->setMovie(movie);
        movie->start();    

"""
import os, sys, platform

from pathlib import Path as touching

import importlib

from PyQt5 import QtCore, QtGui, QtWidgets

import qtawesome as qta
import qdarkstyle


def printQ(message, QObj):
    if isinstance(QObj, QtCore.QRect):
        print(f'QRect {message} : ({QObj.x()}, {QObj.y()}) ({QObj.width()}x{QObj.height()})')
    elif isinstance(QObj, QtCore.QSize):
        print(f'QSize {message} : ({QObj.width()}x{QObj.height()})')
    elif isinstance(QObj, QtCore.QPoint):
        print(f'QPoint {message} : ({QObj.x()}, {QObj.y()})')
    else:
        print('not supported')
        
class ScreenCastToolButton(QtWidgets.QToolButton):
    
    rightClicked = QtCore.pyqtSignal()
    
    video_sizes = {240 : ((462, 240), ''),
                   360 : ((640, 360), ''),
                   480 : ((854, 480), ''),
                   720 : ((1280, 720), ''),
                   1080 : ((1920, 1080), 'aka 1K'),
                   1440 : ((2560, 1440), 'aka 2K'),
                   2160 : ((3840, 2160), 'aka 4K')}

    video_file = 'SSC#.mp4'
    
    icon_size = 16
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # safety check
        for video_size in self.video_sizes:
            if video_size != self.video_sizes[video_size][0][1]:
                raise Exception("problem with declared video sizes")
        
        # check OS
        self.os = platform.system()
        if self.os == 'Windows':
            self.desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') 
        elif self.os == 'Linux':
            self.desktop_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop') 
        elif self.os == 'Darwin': #TODO: check on mac if this works
            self.desktop_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop') 
        else:
            raise Exception("unrecognized operating system")
        
        # check dependencies
        self.dependenciesMet = True
        cv2_spec = importlib.util.find_spec('cv2')
        self.cv2_is_available = cv2_spec is not None
        if not self.cv2_is_available:
            self.dependenciesMet = False
        numpy_spec = importlib.util.find_spec('numpy')
        self.numpy_is_available = numpy_spec is not None
        if not self.numpy_is_available:
            self.dependenciesMet = False
        #TODO: check if I have all dependencies

        # find a microphone
        #TODO: implement the microphone-find-thingy
        self.microphone_available=False
        
        # initialize the countdown
        self.countdown = ScreenCastCountDown(self.parent())

        # set the fps
        self.fps = 14
        
        # initialize the tool button itself.
        self.setIcon(qta.icon('mdi.video', color='orange'))
        self.setIconSize(QtCore.QSize(self.icon_size, self.icon_size))
        self.setEnabled(self.dependenciesMet)
        self.state = 'idle'
        self.clicked.connect(self.toggle_recording)
        self.rightClicked.connect(self.settings)

        self.nextScreencastFile = self.getNextScreencastFile()

        self.show()
        
    def getNextScreencastFile(self):
        '''
        this method will look on the desktop for existing screencast files,
        and determine what is the next available name (no path!)
        '''
        prefix, extension = self.video_file.split('#')
        if extension.upper() != '.MP4':
            raise Exception("only .mp4 is supported!")

        files = os.listdir(self.desktop_path)
        existing_screencasts = []
        for File in files:
            if File.startswith(prefix) and File.endswith(extension):
                existing_screencasts.append(int(File.replace(prefix, '').replace(extension, '')))
        if existing_screencasts == []: # nothing available on the desktop
            next_number = 1
        else:
            next_number = max(existing_screencasts)+1
        return f"{prefix}{next_number}{extension}"

    def mousePressEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            self.rightClicked.emit()
        else:
            self.clicked.emit()
        
    def toggle_recording(self):
        if self.state == 'idle':
            self.start_recording()
        else:
            self.stop_recording()
        
    def start_recording(self):
        '''
        this method will spawn a process (besided spyder) that will do 
        the actual recording stuff.
        '''
        self.state = 'recording'
        self.setIcon(qta.icon('mdi.stop', color='red'))
        
        grabRegion = self.getGrabRegion()
        if grabRegion.height() not in self.video_sizes:
            self.resize()
        else:
            if grabRegion.width() != self.video_sizes[grabRegion.height()][0][0]:
                self.resize()
        grabRegion = self.getGrabRegion()

        self.countdown.do()
    
    def stop_recording(self):
        '''
        this method will communicate with the spawend recording process to 
        tell it to stop recording and save the recording.
        '''
        self.state = 'idle'
        self.setIcon(qta.icon('mdi.video', color='orange'))

        #placeholder
        screencast_file = os.path.join(self.desktop_path, self.nextScreencastFile)
        print(f"creating {screencast_file} ... ", end='')
        touching(screencast_file).touch()
        print("Done.")
        
        self.nextScreencastFile = self.getNextScreencastFile()

    def settings(self):
        '''
        this method handles the settings on the screenCast (context menu)
        '''
        def is_enabled(psize):
            if psize <= screenAG.height(): #TODO: maybe screenG instead ?
                return True
            return False
        
        mainWindow = self.parent().parent()
        screenAG = QtWidgets.QDesktopWidget().availableGeometry(mainWindow)
        screenG = QtWidgets.QDesktopWidget().screenGeometry(mainWindow)

        menu = QtWidgets.QMenu(self)
        
        action = menu.addAction(f'&& {self.fps} Frames per second')  
        if self.microphone_available:
            action.setIcon(qta.icon('mdi.microphone', color='orange'))
        else:
            action.setIcon(qta.icon('mdi.microphone-off', color='orange'))
        menu.addAction(action)

        menu.addSeparator()

        mws = self.getGrabRegion()
        bmws = self.calculateGrabRegion()
        itemset = sorted(set(list(self.video_sizes) + [mws.height()]))
        for item in itemset:        
            if item in self.video_sizes:
                text = f"{item}p ({self.video_sizes[item][0][0]}x{self.video_sizes[item][0][1]}) {self.video_sizes[item][1]}"
                icon = None
                if mws.height() == item:
                    icon = qta.icon('mdi.check-bold', color='orange')
                enabled = is_enabled(item)
            else:
                text = f"({mws.width()}x{mws.height()}) → {bmws.height()}p"
                icon = qta.icon('mdi.check-bold', color='orange')
                enabled = True
            action = menu.addAction(text)
            if not icon == None:
                action.setIcon(icon)
            if item == 240 or ((item==mws.height()) and bmws.height()==240):
                action.triggered.connect(self.resize_to_240p)
            elif item == 360 or ((item==mws.height()) and bmws.height()==360):
                action.triggered.connect(self.resize_to_360p)
            elif item == 480 or ((item==mws.height()) and bmws.height()==480):
                action.triggered.connect(self.resize_to_480p)
            elif item == 720 or ((item==mws.height()) and bmws.height()==720):
                action.triggered.connect(self.resize_to_720p)
            elif item == 1080 or ((item==mws.height()) and bmws.height()==1080):
                action.triggered.connect(self.resize_to_1080p)
            elif item == 1440 or ((item==mws.height()) and bmws.height()==1440):
                action.triggered.connect(self.resize_to_1440p)
            elif item == 2160 or ((item==mws.height()) and bmws.height()==2160):
                action.triggered.connect(self.resize_to_2160p)
            action.setEnabled(enabled)
            
        menu.addSeparator()

        action = menu.addAction(qta.icon('mdi.monitor', color='orange'),
                                f"{screenG.width()}x{screenG.height()}")
        action.setEnabled(True)
        action = menu.addAction(qta.icon('mdi.monitor-screenshot', color='orange'),
                                f"{screenAG.width()}x{screenAG.height()}")
        action.setEnabled(True)
        
        cursorPoint = QtGui.QCursor.pos()
        menuSize = menu.sizeHint()
        menuPoint = QtCore.QPoint(cursorPoint.x()-menuSize.width(),
                                  cursorPoint.y()-menuSize.height())
        menu.exec_(menuPoint)

    def fpsChanged(self, fps):
        '''
        This is the slot where fps can be changed.
        Note : 5 <= fps <= 25, if fps is outside this interval, it will be
               adjusted to the nearest limit.
        '''
        if fps < 5:
            self.fps = 5
        elif fps > 25:
            self.fps = 25
        else:
            self.fps = fps
        
    def resize_to_240p(self):
        self.resize(240)
        
    def resize_to_360p(self):
        self.resize(360)
        
    def resize_to_480p(self):
        self.resize(480)
        
    def resize_to_720p(self):
        self.resize(720)
        
    def resize_to_1080p(self):
        self.resize(1080)
        
    def resize_to_1440p(self):
        self.resize(1440)
        
    def resize_to_2160p(self):
        self.resize(2160)

    def resize(self, psize=-1):
        '''
        this method will resize the main window to the psize resolution.
        if none is provided (-1) then resize to the biggest possible.
        '''
        newRect = self.calculateGrabRegion(psize)
        if newRect.height() != 0: # new size needs to make sense ;-)
            mainWindow = self.parent().parent()
            Δx = mainWindow.frameGeometry().width() - mainWindow.geometry().width()
            Δy = mainWindow.frameGeometry().height() - mainWindow.geometry().height()
            mainWindow.move(newRect.x(), newRect.y())
            mainWindow.resize(newRect.width()-Δx, newRect.height()-Δy)

        self.getGrabRegion()

    def getGrabRegion(self):
        '''
        this method will get the 'GrabRegion' of the main window, and 
        return it as a QRect.
        '''
        mainWindow = self.parent().parent()
        retval = QtCore.QRect(mainWindow.x(), 
                              mainWindow.y(), 
                              mainWindow.frameGeometry().width(), 
                              mainWindow.frameGeometry().height())
        return retval        
        
    def calculateGrabRegion(self, psize=-1):
        '''
        this method will determine the ideal 'GrabRegion' on the screen
        where the MainWindow currently resides given psize.
        If psize=-1, the biggest possible psize given the screen is used.
        return value is a QRect.
        '''
        screenRect = QtWidgets.QDesktopWidget().availableGeometry(self)

        if psize == -1:
            width = height = 0
            for video_size in self.video_sizes:
                if video_size <= screenRect.height():
                    width = self.video_sizes[video_size][0][0]
                    height = self.video_sizes[video_size][0][1]
                
            if width > screenRect.width(): # width takes precedence (rare but possible)
                width = height = 0
                for video_size in self.video_sizes:
                    if self.video_sizes[video_size][0][0] <= self.activeScreenGeometry.width():
                        width = self.video_sizes[video_size][0][0]
                        height = self.video_sizes[video_size][0][1]
                       
            x = int(((screenRect.width()-width)/2)+screenRect.x()) 
            y = int(((screenRect.height()-height)/2)+screenRect.y())
            
        elif psize in self.video_sizes:
            width = self.video_sizes[psize][0][0]
            height = self.video_sizes[psize][0][1]
            if width <= screenRect.width() and height <= screenRect.height():
                x = int(((screenRect.width()-width)/2)+screenRect.x()) 
                y = int(((screenRect.height()-height)/2)+screenRect.y())
            else:
                width = height = 0
                x = int(((screenRect.width()-width)/2)+screenRect.x()) 
                y = int(((screenRect.height()-height)/2)+screenRect.y())
        else:
            width = height = 0
            x = int(((screenRect.width()-width)/2)+screenRect.x()) 
            y = int(((screenRect.height()-height)/2)+screenRect.y())
        retval = QtCore.QRect(x, y, width, height)
        return retval

class ScreenCastCountDown(QtWidgets.QSplashScreen):
    '''
    hint:
    '''
    action = QtCore.pyqtSignal(int) # emitted when contdown is finished
    
    def __init__(self, parent): 
        if not isinstance(parent, QtWidgets.QMainWindow):
            raise Exception(f"parent must by of type 'PyQt5.QtWidgets.QMainWindow', not {type(parent)}")
        super().__init__(parent)
        
        movie_name = os.path.join(os.path.dirname(__file__), 'countdown.gif')
        self.movie = QtGui.QMovie(movie_name)
        self.movie.jumpToFrame(1)
        pixmap = QtGui.QPixmap(self.movie.frameRect().size())
        self.setPixmap(pixmap)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | 
                            QtCore.Qt.FramelessWindowHint)
        self.setEnabled(True)
        self.movie.frameChanged.connect(self.repaint)
        self.movie.finished.connect(self.hideEvent)
    
    def do(self):
        '''
        this is the entry point to do the countdown.
        '''
        grabRegion = self.parent().frameGeometry()
        
        printQ('do countdown', grabRegion)
 
        print(f"movie has {self.movie.frameCount()} frames")   
 
        movie = self.sizeHint()
        printQ('movie', movie)
        
        # x = grabRegion.x() + int(grabRegion.width()/2) - int(self.sizeHint().width()/2)
        # y = grabRegion.y() + int(grabRegion.height()/2) - int(self.sizeHint().height()/2)
        
        # print(f"x={x}, y={y}")
        self.move(0,0)
        printQ('pos', self.pos())
        
        self.show()
        
    def showEvent(self, event):
        self.movie.start()
        super(ScreenCastCountDown, self).showEvent(event)

    def hideEvent(self, event):
        self.movie.stop()
        super(ScreenCastCountDown, self).hideEvent(event)
        self.action.emit(10000) # how to determine the number ?!?

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        pixmap = self.movie.currentPixmap()
        self.setMask(pixmap.mask())
        painter.drawPixmap(0, 0, pixmap)

    def sizeHint(self):
        return self.movie.scaledSize()


class ScreenCastRecorder(object):
    pass


if __name__ == '__main__':
    
    class MainWindow(QtWidgets.QMainWindow):
    
        def __init__(self, app):
            super().__init__()
    
            self.app = app # work-around for the 'spydercustomize.SpyderQApplication' stuff ... not sure what is going on there ...
    
            self.setWindowTitle('Dummy Main Window')
            self.setGeometry(100, 100, 1280, 720)
            self.statusbar = QtWidgets.QStatusBar(self)        
    
            self.screenCastToolButton = ScreenCastToolButton(self)
            self.statusbar.addPermanentWidget(self.screenCastToolButton)
    
            self.setStatusBar(self.statusbar)
            self.show()
            
    
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainWindow = MainWindow(app)
    app.exec_()
