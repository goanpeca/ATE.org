# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 18:13:27 2019

@author: hoeren
"""
import os
import platform
import time
import shutil

from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia, uic

import qtawesome as qta

import ffmpeg
import cv2

# 240p (462x240)
# 360p (640x360)
# 360p (640x360)
# 480p (854x480)
# 720p (1280x720)  # ---> will be our default to start off with
# 1080p (1920x1080 aka 1K)
# 1440p (2560x1440 aka 2K)
# 2160p (3840x2160 aka 4K)

video_sizes = {'240p': (462, 240),
               '360p': (640, 360),
               '360p': (640, 360),
               '480p': (854, 480),
               '720p': (1280, 720),
               '1080p': (1920, 1080),
               '1440p': (2560, 1440),
               '2160p': (3840, 2160)}

default_video_size = '720p'

video_file_convention = 'Spyder_ScreenCast_#.mp4'


class ScreenCastSettings(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.window_resolution = video_sizes[default_video_size]
        self._load_ui()
        self._setup()

    def _load_ui(self):
        import os
        ui = os.path.splitext(os.path.basename(__file__))[0] + '.ui'
        ui_path = os.path.join(os.path.dirname(__file__), ui)
        uic.loadUi(ui_path, self)

    def _setup(self):
        self.resolution.addItems(video_sizes)
        self.resolution.setCurrentText(default_video_size)
        self.ok_button.clicked.connect(self._accept)
        self.cancel_button.clicked.connect(self.reject)

    def _accept(self):
        current_resolution = self.resolution.currentText()
        self.window_resolution = video_sizes[current_resolution]
        self.accept()


class ScreenCast(QtWidgets.QToolButton):
    rightClicked = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)

        self.counter = 0
        self.setIcon(qta.icon('mdi.video', color='orange'))
        self.setIconSize(QtCore.QSize(16, 16))
        self.screencast_state = 'idle'
        # self.clicked.connect(self.start_stop_recording)
        # self.rightClicked.connect(self.settings)

        if platform.system() == 'Windows':
            self.desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        elif platform.system() == 'Linux':
            self.desktop_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
        elif platform.system() == 'Darwin':  # TODO: check on mac if this works
            self.desktop_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
        else:
            raise Exception("unrecognized operating system")

        self.parent = parent
        self.resolution = video_sizes[default_video_size]

        self.audio = os.path.join(self.desktop_path, 'audio.wav')
        self.video = os.path.join(self.desktop_path, 'video.avi')
        self.images = os.path.join(self.desktop_path, "images")

        self.screencast_file = self.get_next_screencast_name()
        self.output = os.path.join(self.desktop_path, self.screencast_file)

        self.generator = ScreenCastGenerator(self.parent, self.images, self.video, self.audio, self.output, 14)

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

        if len(existing_screencasts) == 0:
            next_number = 1
        else:
            next_number = max(existing_screencasts) + 1
        return f"{prefix}{next_number}.{extension}"

    def mousePressEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            self._open_settings()
        else:
            self._start_stop_recording()

    def _open_settings(self):
        screenCastSettings = ScreenCastSettings(self)
        screenCastSettings.exec_()
        self.resolution = screenCastSettings.window_resolution
        del(screenCastSettings)

    def _start_stop_recording(self):
        # TODO: do we need pause as a state
        # if self.record.state() == QtMultimedia.QMediaRecorder.StoppedState:
        if self.screencast_state == "idle":
            self._start_recording()
        else:
            self._stop_recording()

    def _start_recording(self):
        self.generator.start()
        self._set_icon(True)
        self.screencast_state = "running"

    def _stop_recording(self):
        self.generator.stop()
        self._set_icon(False)
        self.screencast_state = "idle"

    def _set_icon(self, is_stoped):
        icon = "mdi.video"
        if is_stoped:
            icon = "mdi.stop"

        self.screencast_state = 'idle'
        self.setIcon(qta.icon(icon, color='orange'))

    def settings(self):
        '''
        this method handles the settings on the screenCast (context menu)
        '''
        current_size, current_width, current_height = self.get_mainwindow_size()

        menu = QtWidgets.QMenu(self)
        # audit = menu.addAction(qta.icon("mdi.incognito", color='orange') ,"audit")
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
        # pack = menu.addAction(qta.icon("mdi.gift-outline", color='orange'), "pack")

        print(f"menu height = {menu.height()}, menu width = {menu.width()}")
        # TODO
        menu.exec_(QtGui.QCursor.pos())

    def resize(self, width, height):
        # self.parent.setGeometry()
        print(width, height)

    @property
    def recording_state(self):
        return self.screencast_state


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
class VideoRecorder(QtCore.QTimer):
    def __init__(self, main_window, output_path, images_path, interval):
        super().__init__()
        self.main_window = main_window
        self.output = output_path
        self.images = images_path
        self.counter = 0
        self.fps = int(1 / interval)
        self._setup()
        self._connect_event_handler()

    def _setup(self):
        self.setInterval(self.fps)
        if os.path.exists(self.images):
            shutil.rmtree(self.images)

        os.makedirs(self.images, exist_ok=True)

    def _connect_event_handler(self):
        self.timeout.connect(self._save_image)

    def _save_image(self):
        q_rec = self.main_window.geometry()
        import qtawesome as qta
        arrow = QtGui.QPixmap(qta.icon("mdi.cursor-default-outline", color="white").pixmap(10, 10))
        self.px = QtWidgets.QApplication.primaryScreen().grabWindow(QtWidgets.QApplication.desktop().winId(),
                                                                    q_rec.x(),
                                                                    q_rec.y(),
                                                                    q_rec.width(),
                                                                    q_rec.height())
        painter = QtGui.QPainter(self.px)
        painter.drawPixmap(QtGui.QCursor.pos(), arrow)
        image = os.path.join(self.images, "image" + str(self.counter) + ".jpg")
        self.px.save(image, 'jpg')
        self.counter += 1


class ScreenCastGenerator(object):
    def __init__(self, main_window, images_path, video_path, audio_path, output_path, interval):
        super().__init__()
        self.images = images_path
        self.video = video_path
        self.audio = audio_path
        self.output = output_path
        self._cleanup()
        self.audio_recorder = AudioRecorder(self.audio)
        self.video_recorder = VideoRecorder(main_window, self.output, self.images, interval)

    def start(self):
        self.audio_recorder.start()
        self.video_recorder.start()

    def stop(self):
        self.audio_recorder.stop()
        self.video_recorder.stop()
        self._mix()

    def _mix(self):
        img_array = []
        size = None
        for num in range(1, len(os.listdir(self.images))):  # glob.glob(os.path.join(self.path, '*.jpg')):
            filename = os.path.join(self.images, "image" + str(num) + ".jpg")
            img = cv2.imread(filename)
            height, width, layers = img.shape
            size = (width, height)
            img_array.append(img)

        if size is None:
            return

        out = cv2.VideoWriter(self.video, cv2.VideoWriter_fourcc(*'DIVX'), 14, size)

        for i in range(len(img_array)):
            out.write(img_array[i])

        out.release()

        self.combine()

    def combine(self):
        video = ffmpeg.input(self.video)
        audio = ffmpeg.input(self.audio)
        ffmpeg.output(video.video, audio.audio, self.output, acodec="aac", vcodec="copy", format='mp4').overwrite_output().run()
        # self._cleanup()

    def _cleanup(self):
        if os.path.exists(self.images):
            shutil.rmtree(self.images)

        if os.path.exists(self.video):
            os.remove(self.video)

        if os.path.exists(self.audio):
            os.remove(self.audio)
