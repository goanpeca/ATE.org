# -*- coding: utf-8 -*-

from ATE.org.actions_on.flow.qualificationwizardbase import wizardbase
from ATE.org.actions_on.flow.qualificationwizardbase import intparam
from ATE.org.actions_on.flow.qualificationwizardbase import writeoncetextparam
from PyQt5 import QtCore, QtGui, QtWidgets, uic



quali_pc_flow_name = "qualification_PC_flow"

class PCWizard(wizardbase.wizardbase):
    # This function shall return a list of parameters, that
    # is usable by the wizard.
    def _get_wizard_parameters(self) -> list:
        return [writeoncetextparam.WriteOnceTextParam("name"),
                intparam.IntParam("MSL", 0, 0, 10000),
                intparam.IntParam("Bake Time (hours)", 0, 0, 500),
                intparam.IntParam("Bake Temperature (°C)", 0, 0, 500),
                intparam.IntParam("Soak Time (hours)", 0, 0, 500),
                intparam.IntParam("Soak Temperature (°C)", 12, 0, 500),
                intparam.IntParam("Soak relative humidity (%)", 0, 0, 100),
                intparam.IntParam("Num Reflows", 0, 0, 500),
                intparam.IntParam("Reflow Temperature (°C)", 12, 0, 500)]
    
    # This function shall return a list of testprogram slots
    # Note: We expect a list of TextBoxParams here
    def _get_wizard_testprogram_slots(self) -> list:
        return []

    def _get_data_type(self) -> str:
        return  quali_pc_flow_name


def new_pc_wizard(storage, product: str):
    dialog = PCWizard({"product": product}, storage)
    dialog.exec_()
    del(dialog)


def edit_pc_wizard(storage, data):
    dialog = PCWizard(data, storage)
    dialog.exec_()
    del(dialog)


def view_pc_wizard(storage, data):
    dialog = PCWizard(data, storage)
    dialog.set_view_only()
    dialog.exec_()
    del(dialog)

if __name__ == '__main__':
    import sys, qdarkstyle

    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    dialog = PCWizard(dict(), None)
    dialog.show()
    sys.exit(app.exec_())
