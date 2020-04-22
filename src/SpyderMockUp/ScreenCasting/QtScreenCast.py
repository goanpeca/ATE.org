# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 18:13:27 2019

@author: hoeren
"""
import os, sys, platform, copy

from pathlib import Path as touching

import importlib

from PyQt5 import QtCore, QtGui, QtWidgets

import qtawesome as qta
import qdarkstyle



# class screenCast(QtWidgets.QLabel):
#     clicked = QtCore.pyqtSignal()
#     rightClicked = QtCore.pyqtSignal()

#     def __init(self, parent):
#         super().__init__(parent)

#     def mousePressEvent(self, ev):
#         if ev.button() == QtCore.Qt.RightButton:
#             self.rightClicked.emit()
#         else:
#             self.clicked.emit()
###########
    # def screencast_settings(self):
    #     print("start screencast settings")
    #     from ScreenCastSettings import ScreenCastSettings
    #     screenCastSettings = ScreenCastSettings(self)
    #     screenCastSettings.exec_()
    #     del(screenCastSettings)
    #     print("end screencast settings")

    # def screencast_start_stop(self):
    #     if self.screencast_state == 'recording':

    #         print("recording stopped")
    #         self.screencast_state = 'idle'
    #         self.screencast.setPixmap(qta.icon('mdi.video', color='orange').pixmap(16,16))
    #     else:

    #         print("recording started")
    #         self.screencast_state = 'recording'
    #         self.screencast.setPixmap(qta.icon('mdi.video', 'fa5s.ban', options=[{'color' : 'orange'},{'color' : 'red'}]).pixmap(16,16))

        #https://riverbankcomputing.com/pipermail/pyqt/2009-April/022668.html
        #https://doc.qt.io/qt-5/qtreewidget-members.html
        #https://www.qtcentre.org/threads/18929-QTreeWidgetItem-have-contextMenu
        #https://cdn.materialdesignicons.com/4.9.95/


class QtScreenCast(QtWidgets.QToolButton):
    
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
        

        
        
        
        # try to find the countdown
        countdown = None
        countdown_path=os.path.join(os.path.dirname(__file__), 'countdown.gif')
        if os.path.exists(countdown_path):
            countdown = QtGui.QMovie(countdown_path)  
        # probably need to add a splashscreen where to play this 'movie'    
            
            
        #TODO: enlarge list of dependencies ?
   
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
    
        # QMovie *movie = new QMovie(":/images/other/images/16x16/loading.gif");
        # QLabel *processLabel = new QLabel(this);
        # processLabel->setMovie(movie);
        # movie->start();    
    
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
        
    def mainWindowSize(self):
        '''
        this method returns the size and position of the main window as a QRect
        '''
        mainWindow = self.parent().parent()
        return QtCore.QRect(mainWindow.x(), mainWindow.y(), mainWindow.width(), mainWindow.height())
        
    def activeScreenSize(self):
        '''
        this method returns the active screen size as a QRect
        '''
        return QtGui.QScreen.geometry(QtGui.QGuiApplication.primaryScreen())

    def activeScreenGeometry(self):
        '''
        this method returns the active Screen Geometry as a QRect
        '''
        return QtGui.QScreen.availableGeometry(QtGui.QGuiApplication.primaryScreen())

    def resizeRect(self, psize=-1):
        '''
        this method will determine the ideal resizing Size and position and return it as a QRect
        '''
        if psize == -1:
            width = height = 0
            for video_size in self.video_sizes:
                if video_size <= self.activeScreenGeometry().height():
                    width = self.video_sizes[video_size][0][0]
                    height = self.video_sizes[video_size][0][1]
                
            if width > self.activeScreenGeometry().width(): # width takes precedence (rare but possible)
                width = height = 0
                for video_size in self.video_sizes:
                    if self.video_sizes[video_size][0][0] <= self.activeScreenGeometry.width():
                        width = self.video_sizes[video_size][0][0]
                        height = self.video_sizes[video_size][0][1]
            
            x = self.activeScreenGeometry().x() + int((self.activeScreenGeometry().width() - width) / 2)
            y = self.activeScreenGeometry().y() + int((self.activeScreenGeometry().height() - height) / 2)
        elif psize in self.video_sizes:
            width = self.video_sizes[psize][0][0]
            height = self.video_sizes[psize][0][1]
            if width <= self.activeScreenGeometry().width() and height <= self.activeScreenGeometry().height():
                x = self.activeScreenGeometry().x() + int((self.activeScreenGeometry().width() - width) / 2)
                y = self.activeScreenGeometry().y() + int((self.activeScreenGeometry().height() - height) / 2)
            else:
                width = heigth = 0
                x = self.activeScreenGeometry().x() + int(self.activeScreenGeometry().width() / 2)
                y = self.activeScreenGeometry().y() + int(self.activeScreenGeometry().height() / 2)
        else:
            width = heigth = 0
            x = self.activeScreenGeometry().x() + int(self.activeScreenGeometry().width() / 2)
            y = self.activeScreenGeometry().y() + int(self.activeScreenGeometry().height() / 2)
        
        return QtCore.QRect(x, y, width, height)

    def settings(self):
        '''
        this method handles the settings on the screenCast (context menu)
        '''
        def is_enabled(psize):
            if psize <= self.activeScreenGeometry().height():
                return True
            return False
        
        print(f"-->{self.parent().parent().screen.manufacturer()}")
        
        
        menu = QtWidgets.QMenu(self)
        
        # fps_spinbox = QtWidgets.QSpinBox()
        # fps_spinbox.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        # fps_spinbox.setMaximum(25)
        # fps_spinbox.setMinimum(5)
        # fps_spinbox.setValue(14)
        # fps_spinbox.valueChanged.connect(self.fpsChanged)
        # fps_label = QtWidgets.QLabel('Frames per second')
        # fps_label.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        # fps_layout = QtWidgets.QHBoxLayout()
        # fps_layout.addWidget(fps_spinbox)
        # fps_layout.addWidget(fps_label)
        # fps = menu.addAction(fps_layout)        

        menu.addSeparator()

        mws = self.mainWindowSize()
        mwrs = self.resizeRect()
        itemset = sorted(set(list(self.video_sizes) + [mws.height()]))
        for item in itemset:        
            if item in self.video_sizes:
                text = f"{item}p ({self.video_sizes[item][0][0]}x{self.video_sizes[item][0][1]}) {self.video_sizes[item][1]}"
                icon = None
                if mws.height() == item:
                    icon = qta.icon('mdi.check-bold', color='orange')
                enabled = is_enabled(item)
            else:
                text = f"{mws.width()}x{mws.height()} --> {mwrs.height()}p"
                icon = qta.icon('mdi.check-bold', color='orange')
                enabled = True
            action = menu.addAction(text)
            if not icon == None:
                action.setIcon(icon)
            if item == 240:
                action.triggered.connect(self.resize_to_240p)
            elif item == 360:
                action.triggered.connect(self.resize_to_360p)
            elif item == 480:
                action.triggered.connect(self.resize_to_480p)
            elif item == 720:
                action.triggered.connect(self.resize_to_720p)
            elif item == 1080:
                action.triggered.connect(self.resize_to_1080p)
            elif item == 1440:
                action.triggered.connect(self.resize_to_1440p)
            elif item == 2160:
                action.triggered.connect(self.resize_to_2160p)
            action.setEnabled(enabled)
            
        menu.addSeparator()

        menu.addAction(qta.icon('mdi.monitor', color='orange'),
                       f"{self.activeScreenSize().width()}x{self.activeScreenSize().height()}")
        menu.addAction(qta.icon('mdi.monitor-screenshot', color='orange'),
                       f"{self.activeScreenGeometry().width()}x{self.activeScreenGeometry().height()}")

        pos = QtGui.QCursor.pos()
        pos.setX(pos.x()-100)
        pos.setY(pos.y()-30)
      
        print(f"menu height = {menu.height()}, menu width = {menu.width()}")
        print(f"menu size height = {menu.size().height()}, menu size width = {menu.size().width()}")

        
        print(type(self.parent().parent().app.desktop))
        
        
        #TODO 
        menu.exec_(pos)

    def fpsChanged(new_frames_per_second):
        print(f"{type(new_frames_per_second)}")
        
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
        if none is provided (-1) then reseze to the biggest possible.
        '''
        newRect = self.resizeRect(psize)
        if newRect.height() != 0: # new size needs to make sense ;-)
            mainWindow = self.parent().parent()
            mainWindow.pos().setX(newRect.x())
            mainWindow.pos().setY(newRect.y())
            mainWindow.resize(newRect.width(), newRect.height())

class recorder(object):
    pass




if __name__ == '__main__':
    
    class MainWindow(QtWidgets.QMainWindow):
    
        def __init__(self, app):
            super().__init__()
    
            self.app = app # work-around for the 'spydercustomize.SpyderQApplication' stuff ... not sure what is going on there ...
    
            self.setWindowTitle('Dummy Main Window')
            self.setGeometry(100, 100, 1280, 720)
            self.statusbar = QtWidgets.QStatusBar(self)        
    
            self.screencast = QtScreenCast(self)
            self.statusbar.addPermanentWidget(self.screencast)
    
            self.setStatusBar(self.statusbar)
            self.show()
            
    
    app = QtWidgets.QApplication(sys.argv)
    # desktop = app.desktop()
    # print(desktop)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainWindow = MainWindow(app)
    app.exec_()