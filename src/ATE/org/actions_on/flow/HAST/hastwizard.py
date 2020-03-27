# -*- coding: utf-8 -*-

from ATE.org.actions_on.flow.qualificationwizardbase import wizardbase
from ATE.org.actions_on.flow.qualificationwizardbase import intparam
from ATE.org.actions_on.flow.qualificationwizardbase import textboxparam
from PyQt5 import QtCore, QtGui, QtWidgets, uic


quali_hast_flow_name = "qualification_hast_flow"


class HASTWizard(wizardbase.wizardbase):
    # This function shall return a list of parameters, that
    # is usable by the wizard.
    def _get_wizard_parameters(self) -> list:
        return [intparam.IntParam("Testwindow (hours)", 0, 0, 10000),
                intparam.IntParam("Duration (hours)", 0, 0, 100),
                intparam.IntParam("Temperature (°C)", 0, 0, 100),
                intparam.IntParam("Rel. Humidity (%)", 0, 0, 100)]
    
    # This function shall return a list of testprogram slots
    # Note: We expect a list of TextBoxParams here
    def _get_wizard_testprogram_slots(self) -> list:
        return []

    def _get_data_type(self) -> str:
        return quali_hast_flow_name


def edit_hast_wizard(storage, product: str):
    hastdata = storage.get_unique_data_for_qualifcation_flow(quali_hast_flow_name, product)
    dialog = HASTWizard(hastdata, storage)
    dialog.exec_()
    del(dialog)


if __name__ == '__main__':
    import sys, qdarkstyle

    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    dialog = HASTWizard(dict(), None)
    dialog.show()
    sys.exit(app.exec_())
