'''
Created on Nov 22, 2019

@author: hoeren
'''
import sys

from PyQt5 import QtCore, QtGui, QtWidgets, uic

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("cleanlooks")

    data = ['one', 'two', 'three', 'four', 'five']

    model = QtCore.QStringListModel(data)

    listView = QtWidgets.QListView()
    listView.setModel(model)
    listView.show()

    combobox = QtWidgets.QComboBox()
    combobox.setModel(model)
    combobox.show()

    sys.exit(app.exec_())
