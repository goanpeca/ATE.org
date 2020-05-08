# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 19:00:00 2020

@author: hoeren
"""

import os
import threading
import time

from PyQt5 import QtCore, QtGui, QtWidgets

import pandas as pd


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


class MovieSplashScreen(QtWidgets.QSplashScreen):
    def __init__(self, movie, parent=None):
        self._movie = movie
        self.movie.jumpToFrame(0)
        pixmap = QtGui.QPixmap(movie.frameRect().size())
        super(MovieSplashScreen, self).__init__(pixmap)
        self.setParent(parent)
        self.movie.frameChanged.connect(self.repaint)

    @property
    def movie(self):
        return self._movie

    def showEvent(self, event):
        self.movie.start()
        super(MovieSplashScreen, self).showEvent(event)

    def hideEvent(self, event):
        self.movie.stop()
        super(MovieSplashScreen, self).hideEvent(event)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        pixmap = self.movie.currentPixmap()
        self.setMask(pixmap.mask())
        painter.drawPixmap(0, 0, pixmap)

    def sizeHint(self):
        return self.movie.scaledSize()


class Processor(QtCore.QObject):
    started = QtCore.pyqtSignal(int)
    filteredResultsSignal = QtCore.pyqtSignal(pd.DataFrame)

    def execute(self, selectedCoins, selectedCoinsText):
        threading.Thread(
            target=self._execute, args=(selectedCoins, selectedCoinsText)
        ).start()

    def _execute(self, selectedCoins, selectedCoinsText):
        print("=====getFilteredSignals====")
        dfFilter = []
        noResults = []
        print("selectedCoins: ", selectedCoins)
        zeit = len(selectedCoins)
        self.started.emit(zeit)

        for i, (coin, text) in enumerate(zip(selectedCoins, selectedCoinsText)):
            print("i: {} {}".format(i, coin))
            if i >= 6:
                time.sleep(6)
            result = makeSignals(selectedCoins[i])
            print("results.empty: ", result.empty)
            if not result.empty:
                result = result.set_index("Pair", inplace=False)
                dfFilter.append(result)
            else:
                print("selectedCoinsText{}: {}".format(i, text))
                noResults.append(text)

        print("\nlen(dfFilter): ", len(dfFilter))
        if len(dfFilter) == 0:
            print("\n\n====in if len(dfFilter) == 0: \n dfFilter: ", dfFilter)
            # Creating an empty Dataframe with column names only
            filteredResults = pd.DataFrame(columns=["User_ID", "UserName", "Action"])
            print(
                "Empty Dataframe ",
                filteredResults,
                "\n dfempty.empty: ",
                filteredResults.empty,
            )
        elif len(dfFilter) > 0:
            for i, df_filter in enumerate(dfFilter):
                print(
                    "\n\n====in for loop=== \n dfFilter [{}]: \n{}".format(i, df_filter)
                )

            filteredResults = pd.concat(dfFilter, axis=0, sort=False)
            # filteredResults['Gain (%)'] = pd.to_numeric(filteredResults['Gain (%)'], errors='coerce')
            filteredResults = filteredResults.sort_values(
                by="Gain (%)", ascending=False, inplace=False
            )
            filteredResults = filteredResults.reset_index(inplace=False)
            print(
                "\nfilteredResults: \n", filteredResults, "\n", filteredResults.dtypes
            )

        self.filteredResultsSignal.emit(filteredResults)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        font = QtGui.QFont("Helvetica", 9)
        self.setFont(font)

        self.processor = Processor(self)
        self.processor.started.connect(self.on_started)
        self.processor.filteredResultsSignal.connect(self.on_filteredResultsSignal)
        self.processor.execute("a", "aText")

        movie_path = os.path.join(CURRENT_DIR, "img", "fuchs.gif")

        movie = QtGui.QMovie(movie_path)
        self.splash = MovieSplashScreen(movie)
        self.splash.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint
        )
        self.splash.setEnabled(False)

        # adding progress bar
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Highlight, QtCore.Qt.green)
        self.progressBar = QtWidgets.QProgressBar()

        self.progressBar.setPalette(palette)
        self.progressBar.setWindowFlags(
            QtCore.Qt.SplashScreen
            | QtCore.Qt.FramelessWindowHint
            | QtCore.Qt.WindowStaysOnTopHint
        )
        self.progressBar.move(self.splash.pos() + QtCore.QPoint(0, -30))
        self.progressBar.resize(self.splash.width(), 30)
        self.counter = 0
        self.gerundet = 0
        self.timer = QtCore.QTimer(interval=100, timeout=self.on_timeout)

    @QtCore.pyqtSlot(pd.DataFrame)
    def on_filteredResultsSignal(self, df):
        print(df)

    @QtCore.pyqtSlot()
    @QtCore.pyqtSlot(int)
    def on_started(self, zeit=0):
        gerundet = 50 if zeit <= 2 else zeit + 60
        print("gerundet = ", gerundet)
        gerundet = gerundet + 1
        self.progressBar.setMaximum(gerundet)
        # splash.setMask(splash_pix.mask())
        self.progressBar.show()
        self.splash.show()
        self.splash.showMessage(
            "<h1><font color='red'></font></h1>",
            QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter,
            QtCore.Qt.black,
        )
        self.counter = 1
        self.gerundet = gerundet
        self.timer.start()

    @QtCore.pyqtSlot()
    def on_timeout(self):
        self.progressBar.setValue(self.counter)
        self.counter += 1
        if self.counter > self.gerundet:
            self.timer.stop()
            self.progressBar.hide()
            self.splash.close()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())