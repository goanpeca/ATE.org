from PyQt5 import QtWidgets, QtCore, uic
import os


class ItemTrace(QtWidgets.QDialog):
    def __init__(self, dependency_list, name, message=''):
        super().__init__()
        self.dependency_list = dependency_list
        self.name = name
        self.message = message
        self._load_ui()
        self._setup()
        self._show()

    def _load_ui(self):
        ui_file = '.'.join(os.path.realpath(__file__).split('.')[:-1]) + '.ui'
        uic.loadUi(ui_file, self)

    def _setup(self):
        self.setWindowTitle(self.name)
        self.setFixedSize(self.size())
        self.ok_button.clicked.connect(self.accept)
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, on=False)
        self.feedback.setText(self.message)
        self.feedback.setStyleSheet('color: orange')
        self.tree_view.setHeaderHidden(True)
        for key, elements in self.dependency_list.items():
            parent = QtWidgets.QTreeWidgetItem(self.tree_view)
            parent.setExpanded(True)
            parent.setText(0, key)
            for element in elements:
                child = QtWidgets.QTreeWidgetItem()
                child.setText(0, element)
                parent.addChild(child)

    def _show(self):
        self.exec_()
