# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 18:13:27 2019

@author: hoeren
"""
import os, sys, platform

from pathlib import Path as touching

import importlib

from PyQt5 import QtCore, QtGui, QtWidgets

import qtawesome as qta
import qdarkstyle

video_sizes = {'240p (462x240)' : (462, 240), 
               '360p (640x360)' : (640, 360),
               '360p (640x360)' : (640, 360),
               '480p (854x480)' : (854, 480),
               '720p (1280x720)' : (1280, 720),  # ---> will be our default to start off with
               '1080p (1920x1080 aka 1K)' : (1920, 1080),
               '1440p (2560x1440 aka 2K)' : (2560, 1440),
               '2160p (3840x2160 aka 4K)' : (3840, 2160)}

default_video_size = '720p (1280x720)'

video_file_convention = 'Spyder_ScreenCast_#.mp4'


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


class ScreenCast(QtWidgets.QToolButton):
    
    rightClicked = QtCore.pyqtSignal()
    
    def __init__(self, parent):
        super().__init__(parent) # WindowFlags ?!?
        
        self.setIcon(qta.icon('mdi.video', color='orange'))
        self.setIconSize(QtCore.QSize(16, 16))
        self.state = 'idle'
        self.clicked.connect(self.start_stop_recording)
        self.rightClicked.connect(self.settings)
        
        if platform.system() == 'Windows':
            self.desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') 
        elif platform.system() == 'Linux':
            self.desktop_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop') 
        elif platform.system() == 'Darwin': #TODO: check on mac if this works
            self.desktop_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop') 
        else:
            raise Exception("unrecognized operating system")

        self.next_screencast_file = self.get_next_screencast_name()
        
        self.show()
        
    def get_next_screencast_name(self):
        '''
        this method will look on the desktop for existing screencast files,
        and determine what is the next available name (no path!)
        '''
        prefix, extension = video_file_convention.replace('#', '').split('.')
        files = os.listdir(self.desktop_path)
        existing_screencasts = []
        for File in files:
            if File.startswith(prefix) and File.endswith(extension):
                existing_screencasts.append(int(File.replace(prefix, '').replace('.', '').replace(extension, '')))
        if existing_screencasts == []: # nothing available on the desktop
            next_number = 1
        else:
            next_number = max(existing_screencasts)+1
        return f"{prefix}{next_number}.{extension}"

    def mousePressEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            self.rightClicked.emit()
        else:
            self.clicked.emit()
        
    def start_stop_recording(self):
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
    
    
    def stop_recording(self):
        '''
        this method will communicate with the spawend recording process to 
        tell it to stop recording and save the recording.
        '''
        self.state = 'idle'
        self.setIcon(qta.icon('mdi.video', color='orange'))

        #placeholder
        screencast_file = os.path.join(self.desktop_path, self.next_screencast_file)
        print(f"creating {screencast_file} ... ", end='')
        touching(screencast_file).touch()
        print("Done.")
        
        self.next_screencast_file = self.get_next_screencast_name()
    
    def get_mainwindow_size(self):
        '''
        this method will return one of the keys in 'video_sizes' if the main
        window conforms, or an empty string if not.
        '''
        height = self.parent().parent().height() #TODO: figure out why parent of parent ?
        width = self.parent().parent().width()
        for video_size in video_sizes:
            print(f"{video_size} <-> {width}x{height}")
            if video_sizes[video_size] == (width, height):
                return video_size, width, height
        return '', width, height
    
    def settings(self):
        '''
        this method handles the settings on the screenCast (context menu)
        '''
        current_size, current_width, current_height = self.get_mainwindow_size()
        
        menu = QtWidgets.QMenu(self)
        #audit = menu.addAction(qta.icon("mdi.incognito", color='orange') ,"audit")
        # audit.triggered.connect(self.resize)
        menu.addSeparator()
        for video_size in video_sizes:
            if video_size == current_size:
                menu.addAction(qta.icon('mdi.check-bold', color='orange'), video_size)
            else:
                menu.addAction(video_size)
            
        if current_size not in video_sizes:
            menu.addSeparator()
            menu.addAction(qta.icon('mdi.alert', color='orange'),
                           f"{current_width}x{current_height} -> {default_video_size.split(' ')[0]}")
            
            
        # mdi-check-bold --> current size
        # mdi-checkbox-blank-outline --> the default 
#        pack = menu.addAction(qta.icon("mdi.gift-outline", color='orange'), "pack")
        
        
        
        print(f"menu height = {menu.height()}, menu width = {menu.width()}")
        #TODO 
        menu.exec_(QtGui.QCursor.pos())

    def resize(self, width, height):
        '''
        this method will resize the main window to 'width' x 'height' 
        '''
        print(resize)
        
class recorder(object):
    pass



class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, app):
        super().__init__()

        self.app = app
        self.setWindowTitle('Dummy Main Window')
        self.setGeometry(100, 100, 1280, 720)
        self.statusbar = QtWidgets.QStatusBar(self)        

        spec = importlib.util.find_spec('cv2')
        self.open_cv_available = spec is not None

        if self.open_cv_available:
            self.screenCast = ScreenCast(self)
            self.statusbar.addPermanentWidget(self.screenCast)

        self.setStatusBar(self.statusbar)
        self.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainWindow = MainWindow(app)
    app.exec_()