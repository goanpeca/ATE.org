# -*- coding: utf-8 -*-

from ATE.org.actions_on.flow.qualificationwizardbase import wizardbase
from ATE.org.actions_on.flow.qualificationwizardbase import intparam
from ATE.org.actions_on.flow.qualificationwizardbase import writeoncetextparam
from PyQt5 import QtCore, QtGui, QtWidgets, uic


quali_flow_name = "qualification_HTOL_flow"
quali_flow_listentry_name = "HTOL"
quali_flow_tooltip = "High Temperature Operating Life"


class HTOLWizard(wizardbase.wizardbase):
    # This function shall return a list of parameters, that
    # is usable by the wizard.
    def _get_wizard_parameters(self) -> list:
        return [writeoncetextparam.WriteOnceTextParam("name"),
                intparam.IntParam("Length (hours)", 0, 0, 10000),
                intparam.IntParam("Testwindow (hours)", 0, 0, 500),
                intparam.IntParam("Vdd (V)", 12, 0, 240)]
    
    # This function shall return a list of testprogram slots
    # Note: We expect a list of TextBoxParams here
    def _get_wizard_testprogram_slots(self) -> list:
        return []

    def _get_data_type(self) -> str:
        return quali_flow_name


def new_item(storage, product: str):
    dialog = HTOLWizard({"product": product}, storage)
    dialog.exec_()
    del(dialog)


def edit_item(storage, data):
    dialog = HTOLWizard(data, storage)
    dialog.exec_()
    del(dialog)


def view_item(storage, data):
    dialog = HTOLWizard(data, storage)
    dialog.set_view_only()
    dialog.exec_()
    del(dialog)

if __name__ == '__main__':
    import sys, qdarkstyle

    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    dialog = HTOLWizard(dict(), None)
    dialog.show()
    sys.exit(app.exec_())
