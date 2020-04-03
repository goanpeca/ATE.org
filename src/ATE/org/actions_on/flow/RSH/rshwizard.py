# -*- coding: utf-8 -*-

from ATE.org.actions_on.flow.qualificationwizardbase import wizardbase
from ATE.org.actions_on.flow.qualificationwizardbase import intparam
from ATE.org.actions_on.flow.qualificationwizardbase import writeoncetextparam
from ATE.org.actions_on.flow.qualificationwizardbase import optionparam
from PyQt5 import QtCore, QtGui, QtWidgets, uic


quali_flow_name = "qualification_RSH_flows"
quali_flow_listentry_name = "RSH"
quali_flow_tooltip = "Resistance to Solder Heat"


class RSHWizard(wizardbase.wizardbase):
    # This function shall return a list of parameters, that
    # is usable by the wizard.
    def _get_wizard_parameters(self) -> list:
        return [writeoncetextparam.WriteOnceTextParam("name"),
                optionparam.OptionParam("Type", ["Reflow", "Bodydip", "Iron Solder"])]
    
    # This function shall return a list of testprogram slots
    # Note: We expect a list of TextBoxParams here
    def _get_wizard_testprogram_slots(self) -> list:
        return []

    def _get_data_type(self) -> str:
        return quali_flow_name


def new_item(storage, product: str):
    dialog = RSHWizard({"product": product}, storage)
    dialog.exec_()
    del(dialog)


def edit_item(storage, data):
    dialog = RSHWizard(data, storage)
    dialog.exec_()
    del(dialog)


def view_item(storage, data):
    dialog = RSHWizard(data, storage)
    dialog.set_view_only()
    dialog.exec_()
    del(dialog)

if __name__ == '__main__':
    import sys, qdarkstyle

    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    dialog = RSHWizard(dict(), None)
    dialog.show()
    sys.exit(app.exec_())
