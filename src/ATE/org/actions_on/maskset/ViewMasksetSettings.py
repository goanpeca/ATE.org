from PyQt5 import QtCore, QtWidgets, uic
from enum import Enum

from ATE.org.actions_on.maskset.constants import *


class ErrorMessage(Enum):
    NoValidConfiguration = "no valid configuration"
    InvalidConfigurationElements = "configuration does not match the template inside constants.py"

    def __call__(self):
        return self.value


class ViewMasksetSettings(QtWidgets.QDialog):
    def __init__(self, maskset_configuration, maskset_name):
        self.maskset_configuration = maskset_configuration
        self.maskset_name = maskset_name

    def __call__(self):
        super().__init__()
        self._load_ui()
        self._setup(self.maskset_name)
        self._connect_event_handler()
        ViewMasksetSettings._setup_dialog_fields(self, self.maskset_configuration, self.maskset_name)

    def _load_ui(self):
        import os
        my_ui = f"{os.path.dirname(os.path.realpath(__file__))}\{UI_FILE}"
        uic.loadUi(my_ui, self)

    def _connect_event_handler(self):
        self.OKButton.clicked.connect(self.accept)
        self.CancelButton.clicked.connect(self.accept)

    def _setup(self, maskset_name):
        self.setWindowTitle("Maskset Setting")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)

        self.masksetName.setText(maskset_name)
        self.masksetName.setEnabled(False)
        self.bondpads.setEnabled(False)
        self.waferDiameter.setEnabled(False)
        self.dieSizeX.setEnabled(False)
        self.dieSizeY.setEnabled(False)
        self.scribeX.setEnabled(False)
        self.scribeY.setEnabled(False)
        self.dieRefY.setEnabled(False)
        self.dieRefX.setEnabled(False)
        self.xOffset.setEnabled(False)
        self.yOffset.setEnabled(False)
        self.flat.setEnabled(False)
        self.Type.setEnabled(False)

        self.bondpadTable.setRowCount(len(self.maskset_configuration["BondpadTable"]))
        row = self.bondpadTable.rowCount()
        column = self.bondpadTable.columnCount()
        for r in range(row):
            for c in range(column):
                item = QtWidgets.QTableWidgetItem('')
                self.bondpadTable.setItem(r, c, item)
                item.setFlags(QtCore.Qt.NoItemFlags)

        # resize cell columns
        for c in range(self.bondpadTable.columnCount()):
            if c == PAD_NAME_COLUMN:
                self.bondpadTable.setColumnWidth(c, NAME_COL_SIZE)

            elif c in (PAD_POS_X_COLUMN, PAD_POS_Y_COLUMN, PAD_SIZE_X_COLUMN, PAD_SIZE_Y_COLUMN, PAD_TYPE_COLUMN):
                self.bondpadTable.setColumnWidth(c, REF_COL_SIZE)

            elif c == PAD_DIRECTION_COLUMN:
                self.bondpadTable.setColumnWidth(c, DIR_COL_SIZE)

        self.bondpadTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.bondpadTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)

    @staticmethod
    def is_valid_configuration(maskset_configuration):
        if not maskset_configuration.keys() == DEFINITION.keys():
            return False

        return True

    @staticmethod
    def _setup_dialog_fields(dialog, maskset_configuration, maskset_name):
        if not ViewMasksetSettings.is_valid_configuration(maskset_configuration):
            dialog.feedback.setText(ErrorMessage.InvalidConfigurationElements())
            dialog.feedback.setStyleSheet('color: red')
            return

        dialog.feedback.setText('')
        dialog.feedback.setStyleSheet('')

        index = dialog.waferDiameter.findText(str(maskset_configuration["WaferDiameter"]), QtCore.Qt.MatchFixedString)
        if index >= 0:
            dialog.waferDiameter.setCurrentIndex(index)

        dialog.masksetName.setText(maskset_name)
        dialog.masksetName.setEnabled(False)

        dialog.bondpads.setValue((maskset_configuration["Bondpads"]))

        dialog.dieSizeX.setText(str(maskset_configuration["DieSize"][0])) # tuple
        dialog.dieSizeY.setText(str(maskset_configuration["DieSize"][1]))

        dialog.dieRefX.setText(str(maskset_configuration["DieRef"][0])) # tuple
        dialog.dieRefY.setText(str(maskset_configuration["DieRef"][1]))

        dialog.scribeX.setText(str(maskset_configuration["Scribe"][0])) # tuple
        dialog.scribeY.setText(str(maskset_configuration["Scribe"][1]))

        dialog.xOffset.setText(str(maskset_configuration["Offset"][0])) # tuple
        dialog.yOffset.setText(str(maskset_configuration["Offset"][1]))

        dialog.flat.setText(str(maskset_configuration["Flat"]))

        table_infos = maskset_configuration["BondpadTable"]
        dialog.bondpadTable.setRowCount(len(table_infos))
        row = dialog.bondpadTable.rowCount()
        column = dialog.bondpadTable.columnCount()

        for r in range(row):
            for c in range(column):
                dialog.bondpadTable.item(r, c).setText(str(table_infos[r + 1][c]))


def display_maskset_settings_dialog(maskset_configuration, maskset_name):
    maskset_wizard = ViewMasksetSettings(maskset_configuration, maskset_name)
    maskset_wizard()  # provoke __call__ function
    maskset_wizard.exec_()
    del(maskset_wizard)
