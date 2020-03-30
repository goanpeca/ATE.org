from PyQt5 import QtCore, QtGui, QtWidgets, uic

class TreeItemWithData(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent):
        super(QtWidgets.QTreeWidgetItem, self).__init__(parent, None)

    def set_item_data(self, data):
        self.data = data
    
    def get_item_data(self):
        return self.data