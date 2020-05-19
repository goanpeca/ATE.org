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
import os
import sys
import platform
import shutil
import tempfile

from multiprocessing import Process

from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia

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

    video_sizes = {240: ((462, 240), ''),
                   360: ((640, 360), ''),
                   480: ((854, 480), ''),
                   720: ((1280, 720), ''),
                   1080: ((1920, 1080), 'aka 1K'),
                   1440: ((2560, 1440), 'aka 2K'),
                   2160: ((3840, 2160), 'aka 4K')}

    icon_size = 16
    fps = 14

    def __init__(self, main_window, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_window = main_window

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
        elif self.os == 'Darwin':  # TODO: check on mac if this works
            self.desktop_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
        else:
            raise Exception("unrecognized operating system")

        # for test purposes:
        self.dependenciesMet = True
        # TODO: check if I have all dependencies

        # find a microphone
        # TODO: implement the microphone-find-thingy
        self.microphone_available = False

        # initialize the countdown
        # self.countdown = ScreenCastCountDown(self.parent())

        # initialize the tool button itself.
        self.setIcon(qta.icon('mdi.video', color='orange'))
        self.setIconSize(QtCore.QSize(self.icon_size, self.icon_size))
        self.setEnabled(self.dependenciesMet)
        self.state = 'idle'
        self.clicked.connect(self.toggle_recording)
        self.rightClicked.connect(self.settings)

        self.generator = ScreenCastRecorder(self.main_window, self.desktop_path, self.fps)

    def _poll(self):
        self.client.send('continue')

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

        self.generator.start_recording()

        # TODO: impl. this
        # self.countdown.do()

    def stop_recording(self):
        '''
        this method will communicate with the spawend recording process to
        tell it to stop recording and save the recording.
        '''
        self.state = 'idle'
        self.setIcon(qta.icon('mdi.video', color='orange'))

        self.generator.stop_recording()

    def settings(self):
        '''
        this method handles the settings on the screenCast (context menu)
        '''
        def is_enabled(psize):
            if psize <= screenAG.height():  # TODO: maybe screenG instead ?
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
            if icon is not None:
                action.setIcon(icon)
            if item == 240 or ((item == mws.height()) and bmws.height() == 240):
                action.triggered.connect(lambda: self.resize(240))
            elif item == 360 or ((item == mws.height()) and bmws.height() == 360):
                action.triggered.connect(lambda: self.resize(360))
            elif item == 480 or ((item == mws.height()) and bmws.height() == 480):
                action.triggered.connect(lambda: self.resize(480))
            elif item == 720 or ((item == mws.height()) and bmws.height() == 720):
                action.triggered.connect(lambda: self.resize(720))
            elif item == 1080 or ((item == mws.height()) and bmws.height() == 1080):
                action.triggered.connect(lambda: self.resize(1080))
            elif item == 1440 or ((item == mws.height()) and bmws.height() == 1440):
                action.triggered.connect(lambda: self.resize(1440))
            elif item == 2160 or ((item == mws.height()) and bmws.height() == 2160):
                action.triggered.connect(lambda: self.resize(2160))
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
        menuPoint = QtCore.QPoint(cursorPoint.x() - menuSize.width(),
                                  cursorPoint.y() - menuSize.height())
        menu.exec_(menuPoint)

    def resize(self, psize=-1):
        '''
        this method will resize the main window to the psize resolution.
        if none is provided (-1) then resize to the biggest possible.
        '''
        newRect = self.calculateGrabRegion(psize)
        if newRect.height() != 0:  # new size needs to make sense ;-)
            mainWindow = self.parent().parent()
            Δx = mainWindow.frameGeometry().width() - mainWindow.geometry().width()
            Δy = mainWindow.frameGeometry().height() - mainWindow.geometry().height()
            mainWindow.move(newRect.x(), newRect.y())
            mainWindow.resize(newRect.width() - Δx, newRect.height() - Δy)

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

            x = int(((screenRect.width() - width) / 2) + screenRect.x())
            y = int(((screenRect.height() - height) / 2) + screenRect.y())

        elif psize in self.video_sizes:
            width = self.video_sizes[psize][0][0]
            height = self.video_sizes[psize][0][1]
            if width <= screenRect.width() and height <= screenRect.height():
                x = int(((screenRect.width() - width) / 2) + screenRect.x())
                y = int(((screenRect.height() - height) / 2) + screenRect.y())
            else:
                width = height = 0
                x = int(((screenRect.width() - width) / 2) + screenRect.x())
                y = int(((screenRect.height() - height) / 2) + screenRect.y())
        else:
            width = height = 0
            x = int(((screenRect.width() - width) / 2) + screenRect.x())
            y = int(((screenRect.height() - height) / 2) + screenRect.y())
        retval = QtCore.QRect(x, y, width, height)
        return retval


class AudioRecorder(QtMultimedia.QAudioRecorder):
    def __init__(self, audio_path):
        super().__init__()
        self.audio = audio_path
        self._setup()

    def _setup(self):
        self.audio_encoder_settings = QtMultimedia.QAudioEncoderSettings()
        self.audio_encoder_settings.setCodec('audio/aac')
        self.audio_encoder_settings.setQuality(QtMultimedia.QMultimedia.HighQuality)
        self.audio_encoder_settings.setEncodingMode(QtMultimedia.QMultimedia.ConstantBitRateEncoding)
        self.setAudioSettings(self.audio_encoder_settings)
        self.setOutputLocation(QtCore.QUrl.fromLocalFile(self.audio))

        # TODO: do we need to specify audio input
        # self.setAudioInput(self.audioInputs()[1])

    def start(self):
        self.record()


# possible to start the timer after a given time
class VideoRecorder:
    def __init__(self, main_window, images_path, fps):
        super().__init__()
        self.main_window = main_window
        self.images = images_path
        self.counter = 0
        self.timer = QtCore.QTimer()
        self.interval = int(1000 / fps)
        self.timer.setInterval(self.interval)
        self._connect_event_handler()

    def _connect_event_handler(self):
        self.timer.timeout.connect(self._save_image)

    def start(self):
        self.timer.start()

    def stop(self):
        self.timer.stop()

    def _save_image(self):
        os.makedirs(self.images, exist_ok=True)
        q_rec = self.main_window.geometry()
        import qtawesome as qta
        arrow = QtGui.QPixmap(qta.icon("mdi.cursor-default-outline", color="white").pixmap(13, 13))
        self.px = QtWidgets.QApplication.primaryScreen().grabWindow(0,
                                                                    q_rec.x(),
                                                                    q_rec.y(),
                                                                    q_rec.width(),
                                                                    q_rec.height())

        painter = QtGui.QPainter(self.px)
        painter.drawPixmap(QtGui.QCursor.pos() - q_rec.topLeft(), arrow)
        image = os.path.join(self.images, "image" + str(self.counter).zfill(7) + ".jpg")
        self.px.save(image, 'jpg')
        self.counter += 1


class ScreenCastRecorder:

    video_file = 'SSC#.mp4'
    temp_file = tempfile.gettempdir()

    def __init__(self, main_window, desktop_path, interval):
        super().__init__()
        self.desktop_path = desktop_path
        self.audio = os.path.join(self.temp_file, 'audio.wav')
        self.video = os.path.join(self.temp_file, 'video.avi')
        self.images = os.path.join(self.temp_file, "images")

        self._setup()
        self.audio_recorder = AudioRecorder(self.audio)
        self.video_recorder = VideoRecorder(main_window, self.images, interval)
        self.main_window = main_window

    def _setup(self):
        if os.path.exists(self.images):
            shutil.rmtree(self.images)

        os.makedirs(self.images, exist_ok=True)

        if os.path.exists(self.video):
            os.remove(self.video)

        if os.path.exists(self.audio):
            os.remove(self.audio)

    def start_recording(self):
        self.audio_recorder.start()
        self.video_recorder.start()

    def stop_recording(self):
        self.output = os.path.join(self.desktop_path, self._get_next_screencast_file())
        self.video_recorder.counter = 0
        self.audio_recorder.stop()
        self.video_recorder.stop()
        q_rec = self.main_window.geometry()
        combine_process = Combiner(self.video, self.images, self.audio, self.output, (q_rec.height(), q_rec.width()))
        combine_process.start()

    def _get_next_screencast_file(self):
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
        if existing_screencasts == []:  # nothing available on the desktop
            next_number = 1
        else:
            next_number = max(existing_screencasts) + 1
        return f"{prefix}{next_number}{extension}"


class Combiner(Process):
    def __init__(self, video_path, images_path, audio_path, output_path, window_resolution):
        super().__init__()
        self.video = video_path

        self.images = images_path
        self.audio = audio_path
        self.output = output_path

    def run(self):
        '''
            to produce the video with its assosiated audio, we muss calculate the frame rate new
            each time we do recording to prevent any overlapping error between audio and video.
        '''
        import wave
        import contextlib
        with contextlib.closing(wave.open(self.audio, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
        frame_rate = int(len(os.listdir(self.images)) / duration)
        images = os.path.join(self.images, "image%7d.jpg")
        os.system(f"ffmpeg -framerate {frame_rate} -start_number 0 -i {images} -i {self.audio} -c:v libx264 -crf 25 -pix_fmt yuv420p {self.output}")


class ScreenCastCountDown(QtWidgets.QSplashScreen):
    action = QtCore.pyqtSignal(int)  # emitted when contdown is finished

    def __init__(self, parent):
        if not isinstance(parent, QtWidgets.QMainWindow):
            raise Exception(f"parent must by of type 'PyQt5.QtWidgets.QMainWindow', not {type(parent)}")
        super().__init__(parent)

        movie_name = os.path.join(os.path.dirname(__file__), 'countdown.gif')
        self.movie = QtGui.QMovie(movie_name)
        self.movie.jumpToFrame(1)
        pixmap = QtGui.QPixmap(self.movie.frameRect().size())
        self.setPixmap(pixmap)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
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
        self.move(0, 0)
        printQ('pos', self.pos())

        self.show()

    def showEvent(self, event):
        self.movie.start()
        super(ScreenCastCountDown, self).showEvent(event)

    def hideEvent(self, event):
        self.movie.stop()
        super(ScreenCastCountDown, self).hideEvent(event)
        self.action.emit(10000)  # how to determine the number ?!?

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        pixmap = self.movie.currentPixmap()
        self.setMask(pixmap.mask())
        painter.drawPixmap(0, 0, pixmap)

    def sizeHint(self):
        return self.movie.scaledSize()


if __name__ == '__main__':

    class MainWindow(QtWidgets.QMainWindow):

        def __init__(self, app):
            super().__init__()

            self.app = app  # work-around for the 'spydercustomize.SpyderQApplication' stuff ... not sure what is going on there ...

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
