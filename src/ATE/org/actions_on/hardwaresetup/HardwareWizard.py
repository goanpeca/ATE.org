# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 09:52:27 2020

@author: hoeren
"""

import os
import re

from ATE.org.validation import valid_pcb_name_regex
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import qtawesome as qta


PR = 'PR'
FT = 'FT'


class HardwareWizard(QtWidgets.QDialog):
    """ this wizard will create the definition as follows:
        hardware_definition = {
            'hardware': 'HW0',
            'PCB': {},
            'tester': 'SCT',
            'instruments': {},
            'actuators': {}}
    """

    def __init__(self, project_info, definition={}):
        super().__init__()
        self.project_info = project_info
        self._site = None
        self._pattern_type = None
        self._pattern = {}
        self._available_pattern = {}
        self._available_definiton = None
        self._selected_available_item = ''
        self.is_active = True

        self._load_ui()
        self._setup(definition)
        self._connect_event_handler()
        self._verify()

    def _load_ui(self):
        ui = '.'.join(os.path.realpath(__file__).split('.')[:-1]) + '.ui'
        uic.loadUi(ui, self)

    def _setup(self, definition={}):
        self.setWindowTitle(' '.join(re.findall('.[^A-Z]*', os.path.basename(__file__).replace('.py', ''))))
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)
        self.setFixedSize(self.size())

    # hardware
        if definition == {}:
            self.hardware.setText(self.project_info.get_next_hardware())
        else:
            self.hardware.setText(definition['hardware'])
        self.hardware.setEnabled(False)

        self.probecardLink.setDisabled(True)
    # PCBs
        rxPCBName = QtCore.QRegExp(valid_pcb_name_regex)
        PCBName_validator = QtGui.QRegExpValidator(rxPCBName, self)

        if definition == {}:
            self.singlesiteLoadboard.setText('')
            self.singlesiteProbecard.setText('')
            self.singlesiteDIB.setText('')
            self.singleSiteDIBisCable.setChecked(False)
            self.multisiteLoadboard.setText('')
            self.multisiteProbecard.setText('')
            self.multisiteDIB.setText('')
            self.multiSiteDIBisCable.setChecked(False)
            self.maxParallelism.setCurrentText('1')
        else:
            print(definition)
            self.singlesiteLoadboard.setText(definition['PCB']['SingleSiteLoadboard'])
            self.singlesiteProbecard.setText(definition['PCB']['SingleSiteProbecard'])
            self.singlesiteDIB.setText(definition['PCB']['SingleSiteDIB'])
            self.singleSiteDIBisCable.setChecked(definition['PCB']['SingleSiteDIBisCable'])
            self.multisiteLoadboard.setText(definition['PCB']['MultiSiteLoadboard'])
            self.multisiteProbecard.setText(definition['PCB']['MultiSiteProbecard'])
            self.multisiteDIB.setText(definition['PCB']['MultiSiteDIB'])
            self.multiSiteDIBisCable.setChecked(definition['PCB']['MultiSiteDIBisCable'])
            self.maxParallelism.setCurrentText(str(definition['PCB']['MaxParallelism']))

        self.singlesiteLoadboard.setValidator(PCBName_validator)
        self.multisiteLoadboard.setValidator(PCBName_validator)
        self.singlesiteProbecard.setValidator(PCBName_validator)
        self.multisiteProbecard.setValidator(PCBName_validator)
        self.singlesiteDIB.setValidator(PCBName_validator)
        self.multisiteDIB.setValidator(PCBName_validator)

        self.singlesiteLoadboard.setEnabled(True)
        self.multisiteLoadboard.setDisabled(True)
        self.singlesiteProbecard.setEnabled(True)
        self.multisiteProbecard.setDisabled(True)
        self.singlesiteDIB.setEnabled(True)
        self.multisiteDIB.setDisabled(True)

    # Instruments
        self.tester.clear()
        self.tester.addItems([''] + self.project_info.get_available_testers())
        if definition == {}:
            self.tester.setCurrentText('')
        else:
            if definition['tester'] in self.project_info.get_available_testers():
                self.tester.setCurrentText(definition['tester'])
            else:
                self.tester.setCurrentText('')
# until here the 'edit' is implemented, after this point I don't see things anymore ...

        # ... rest of instruments

    # Parallelism
        self.finaltestConfiguration.setColumnCount(self._max_parallelism_value)
        self.finaltestConfiguration.setRowCount(self._max_parallelism_value)
        self.finaltestSites.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self._set_list_visible_items(self.finaltestSites.count())
        self._init_table()
        # TODO: find a better solution
        self.finaltestConfiguration.setFixedSize(626, 374)

        self.right_button.setEnabled(False)
        self.probing_button.setChecked(True)
        self._pattern_type = PR

    # general
        self.feedback.setText('')
        self.feedback.setStyleSheet('color: orange')

        self.tabLayout.setCurrentIndex(0)

        self._set_icons()

        self.OKButton.setEnabled(False)
        self.CancelButton.setEnabled(True)

    def _set_icons(self):
        self.right_button.setIcon(qta.icon('mdi.arrow-right-bold', color='orange'))
        self.left_button.setIcon(qta.icon('mdi.arrow-left-bold', color='orange'))
        # self.availableInstruments.clear()
        # self.availableInstruments.addItems([''])
        # self.parent.project_info.get_available_instruments())
        # TODO: move from list to tree for this widget!
        self.collapse.setIcon(qta.icon('mdi.unfold-less-horizontal', color='orange'))
        self.expand.setIcon(qta.icon('mdi.unfold-more-horizontal', color='orange'))
        self.addInstrument.setIcon(qta.icon('mdi.arrow-right-bold', color='orange'))
        self.removeInstrument.setIcon(qta.icon('mdi.arrow-left-bold', color='orange'))
        # self.usedInstruments.clear()
        # TODO: move from list to tree for this widget!

    # Actuator
        # TODO: initialize this section
        self.addActuator.setIcon(qta.icon('mdi.arrow-right-bold', color='orange'))
        self.removeActuator.setIcon(qta.icon('mdi.arrow-left-bold', color='orange'))
        self.probecardLink.setIcon(qta.icon('mdi.link', color='orange'))

    def _connect_event_handler(self):
        # Parallelism
        self.finaltestConfiguration.cellClicked.connect(self._table_cell_clicked)
        self.finaltestConfiguration.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.finaltestConfiguration.customContextMenuRequested.connect(self._clear_cell)
        self.probecardLink.clicked.connect(self._link_probecard)
        self.probing_button.clicked.connect(self._on_probing_toggeled)
        self.final_test_button.clicked.connect(self._on_final_test_toggeled)
        self.finaltestSites.clicked.connect(self._final_test_list_clicked)
        self.reset_button.clicked.connect(self._init_table)
        self.right_button.clicked.connect(self._right_button_clicked)
        self.left_button.clicked.connect(self._left_button_clicked)
        self.finaltestAvailableConfigurations.clicked.connect(self._edit_pattern)

        # PCBs
        self.singlesiteLoadboard.textChanged.connect(self._verify)
        self.singlesiteDIB.textChanged.connect(self._verify)
        self.singlesiteProbecard.textChanged.connect(self._verify)
        self.multisiteLoadboard.textChanged.connect(self._verify)
        self.multisiteProbecard.textChanged.connect(self._verify)
        self.multisiteDIB.textChanged.connect(self._verify)
        self.maxParallelism.currentTextChanged.connect(self._max_parallelism_value_changed)

        # Instruments
        self.tester.currentTextChanged.connect(self.testerChanged)
        self.collapse.clicked.connect(self.collapseAvailableInstruments)
        self.expand.clicked.connect(self.expandAvailableInstruments)
        self.addInstrument.clicked.connect(self.addingInstrument)
        self.removeInstrument.clicked.connect(self.removingInstrument)
        self.checkInstruments.clicked.connect(self.checkInstrumentUsage)
        self.availableInstruments.itemSelectionChanged.connect(self.availableInstrumentsSelectionChanged)
        self.usedInstruments.itemSelectionChanged.connect(self.usedInstrumentsSelectionChanged)

        # Actuator
        self.addActuator.clicked.connect(self.addingActuator)
        self.removeActuator.clicked.connect(self.removingActuator)
        self.checkActuators.clicked.connect(self.checkActuatorUsage)
        self.availableActuators.itemSelectionChanged.connect(self.availableActuatorSelectionChanged)
        self.usedActuators.itemSelectionChanged.connect(self.usedActuatorSelectionChanged)

        # general
        self.CancelButton.clicked.connect(self.CancelButtonPressed)
        self.OKButton.clicked.connect(self.OKButtonPressed)

    def _edit_pattern(self, index):
        item = self.finaltestAvailableConfigurations.itemFromIndex(index)
        pattern = self._available_pattern[item.text()]
        self._selected_available_item = item.text()

        self.finaltestConfiguration.setColumnCount(len(pattern[0]))
        self.finaltestConfiguration.setRowCount(len(pattern))
        self._set_list_visible_items(len(pattern))
        self._init_table()
        self.maxParallelism.setCurrentText(str(len(pattern)))

        for row in range(self.finaltestConfiguration.rowCount()):
            for col in range(self.finaltestConfiguration.columnCount()):
                element = pattern[row][col]
                if element == 0:
                    element = ''

                item = self.finaltestConfiguration.item(row, col)
                item.setText(str(element))

        self._set_final_test_sites(False)

    def _deselect_list_item(self):
        self._selected_available_item = ''
        for item in self.finaltestAvailableConfigurations.selectedItems():
            item.setSelected(False)

    def _set_final_test_sites(self, visible):
        for index in range(self.finaltestSites.count()):
            item = self.finaltestSites.item(index)
            if not visible:
                item.setFlags(QtCore.Qt.NoItemFlags)
            else:
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

    def _does_name_already_exist(self, name):
        for index in range(self.finaltestAvailableConfigurations.count()):
            item = self.finaltestAvailableConfigurations.item(index)
            if item.text() == name:
                return True

        return False

    def _right_button_clicked(self):
        if not self._does_name_already_exist(self.name):
            self.finaltestAvailableConfigurations.addItem(self.name)

        self._available_pattern.update(self._pattern)
        self._pattern.clear()
        self.name = ''
        self.right_button.setEnabled(False)
        self._init_table()
        self._selected_available_item = ''

    def _left_button_clicked(self):
        self.finaltestAvailableConfigurations.clearFocus()
        item = self.finaltestAvailableConfigurations.currentItem()
        if not item:
            return

        for index in range(self.finaltestAvailableConfigurations.count()):
            element = self.finaltestAvailableConfigurations.item(index)
            if element.text() == item.text():
                self.finaltestAvailableConfigurations.takeItem(index)

        for key, _ in self._available_pattern.items():
            if key == item.text():
                self._available_pattern.pop(key)
                return

    def _init_table(self):
        for row in range(self.finaltestConfiguration.rowCount()):
            for col in range(self.finaltestConfiguration.columnCount()):
                item = self.finaltestConfiguration.item(row, col)
                if not item:
                    item = QtWidgets.QTableWidgetItem('')
                    self.finaltestConfiguration.setItem(row, col, item)

                if item.text():
                    self._update_final_test_item(item.text())

                item.setText('')
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

    def _clear_cell(self, point):
        item = self.finaltestConfiguration.itemAt(point)
        if not item:
            return

        item_content = item.text()
        if not item_content:
            return

        self._update_final_test_item(item_content)
        self.right_button.setEnabled(False)
        item.setText('')

    def _on_probing_toggeled(self):
        self.finaltestConfiguration.setColumnCount(self._max_parallelism_value)
        self.finaltestConfiguration.setRowCount(self._max_parallelism_value)
        self._init_table()
        self._pattern_type = PR

    def _on_final_test_toggeled(self):
        self.finaltestConfiguration.setColumnCount(self._max_parallelism_value)
        self._init_table()
        self.finaltestConfiguration.setRowCount(1)
        self._pattern_type = FT

    def _set_list_visible_items(self, count):
        for index in range(count):
            item = self.finaltestSites.item(index)
            if index < self._max_parallelism_value:
                item.setHidden(False)
                continue

            item.setHidden(True)

    def _final_test_list_clicked(self, index):
        self._site = None
        item = self.finaltestSites.itemFromIndex(index)
        if not self._is_site_selectable(item):
            return

        self._site = item

    def _table_cell_clicked(self, row, column):
        if not self._site:
            return

        if not self._site.text():
            return

        item = self.finaltestConfiguration.item(row, column)
        if not self._is_site_selectable(self._site):
            return

        # we should update site list when we override an already set cell
        if item.text():
            self._update_final_test_item(item.text())

        item.setText(self._site.text())
        self._site.setFlags(QtCore.Qt.NoItemFlags)
        if not self._are_all_sites_used():
            return

        self._verify_table()

    def _is_site_selectable(self, site):
        flag = site.flags()
        if not bool(flag & QtCore.Qt.ItemIsSelectable):
            return False

        return True

    def _update_final_test_item(self, name):
        for index in range(self._max_parallelism_value):
            item = self.finaltestSites.item(index)
            if item.text() == name:
                item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)

    def _are_all_sites_used(self):
        for index in range(self._max_parallelism_value):
            item = self.finaltestSites.item(index)
            if self._is_site_selectable(item):
                self.right_button.setEnabled(False)
                return False

        return True

# PCBs
    def _max_parallelism_value_changed(self, selected_parallelism):
        if not self.maxParallelism.isEnabled():
            return

        if self._max_parallelism_value == 1:
            self.multisiteLoadboard.setEnabled(False)
            self.multisiteDIB.setEnabled(False)
            self.multisiteProbecard.setEnabled(False)

            self._multi_site_loadboard_value = ''
            self._multi_site_probecard_value = ''
            self._multi_site_dib_value = ''

            self.probecardLink.setDisabled(True)
            self.finaltestConfiguration.setColumnCount(1)
            self.finaltestConfiguration.setRowCount(1)
        else:
            self.multisiteLoadboard.setEnabled(True)
            self.multisiteDIB.setEnabled(True)
            self.multisiteProbecard.setEnabled(True)
            self.probecardLink.setDisabled(False)
            self.finaltestConfiguration.setColumnCount(self._max_parallelism_value)
            if self.probing_button.isChecked():
                self.finaltestConfiguration.setRowCount(self._max_parallelism_value)
            else:
                self.finaltestConfiguration.setRowCount(1)

            self._deselect_list_item()

        self._init_table()
        self._set_list_visible_items(self.finaltestSites.count())
        self._set_final_test_sites(True)
        self._verify()

    def _link_probecard(self):
        if not self._single_site_probecard_value:
            return

        self._multi_site_probecard_value = self._single_site_probecard_value

    def _verify(self):
        if self.hardware.text() == 'HW0':
            # when HW0 is set everything is allowed we do not need to check our entries
            self.OKButton.setEnabled(True)
            self.tabLayout.setTabEnabled(1, False)
            self.tabLayout.setTabEnabled(2, False)
            return

        self.feedback.setText('')
        self.OKButton.setEnabled(False)

        if self._max_parallelism_value == 1:
            if not self._single_site_loadboard_value:
                self.feedback.setText("no singlesite_loadboard is specified")

        else:
            if self._single_site_dib_value and not self._multi_site_dib_value:
                self.feedback.setText("no multisite_dib is specified")

            if not self._single_site_dib_value and self._multi_site_dib_value:
                self.feedback.setText("no singlesite_dib is specified ")

            if self._single_site_probecard_value and not self._multi_site_probecard_value:
                self.feedback.setText("no multisite_Probecard is specified ")

            if not self._single_site_probecard_value and self._multi_site_probecard_value:
                self.feedback.setText("no singlesite_Probecard is specified ")

            if self._single_site_loadboard_value == self._multi_site_loadboard_value:
                self.feedback.setText("single- and multisiteloadboad could not habe same name")

            if not self._multi_site_loadboard_value:
                self.feedback.setText("no multisite_loadboard is specified")

            if not self._single_site_loadboard_value:
                self.feedback.setText("no singlesite_loadboard is specified")

            # TODO: do we need to check this case
            # if self._single_site_dib_value == self._single_site_dib_value:
            #     self.feedback.setText("no singlesite_loadboard is specified")

        if self.feedback.text() == '':
            self.OKButton.setEnabled(True)

    def _verify_table(self):
        pattern = self._get_pattern()
        name = self._pattern_type + str(len(pattern))
        if self._does_pattern_exist(name, pattern):
            self.feedback.setText("pattern exists already")
            self.feedback.setStyleSheet('color: orange')
            self.right_button.setEnabled(False)
            return

        self.feedback.setText("")
        if not self._selected_available_item:
            names = []
            for index in range(self.finaltestAvailableConfigurations.count()):
                item = self.finaltestAvailableConfigurations.item(index)
                if name not in item.text():
                    continue

                names.append(item.text())

            if len(names) == 0:
                name += 'A'
            else:
                name = names[-1]
                new_char = chr(ord(name[-1]) + 1)
                name = name[:-1]
                name += new_char
        else:
            name = self._selected_available_item

        self.name = name
        self._pattern[name] = pattern
        self.right_button.setEnabled(True)

    def _get_pattern(self):
        pattern = []
        for row in range(self.finaltestConfiguration.rowCount()):
            row_elements = []
            for column in range(self.finaltestConfiguration.columnCount()):
                item_content = self.finaltestConfiguration.item(row, column).text()
                if item_content:
                    row_elements.append(int(item_content))
                else:
                    row_elements.append(0)

            pattern.append(tuple(row_elements))

        return pattern

    def _does_pattern_exist(self, name, pattern):
        if self._available_definiton:
            # hardware exists already, edit case
            pass

        for key, value in self._available_pattern.items():
            if name in key:
                if value == pattern:
                    return True

        return False

    @property
    def _max_parallelism_value(self):
        return int(self.maxParallelism.currentText())

    @property
    def _single_site_loadboard_value(self):
        return self.singlesiteLoadboard.text()

    @property
    def _multi_site_loadboard_value(self):
        return self.multisiteLoadboard.text()

    @_multi_site_loadboard_value.setter
    def _multi_site_loadboard_value(self, value):
        self.multisiteLoadboard.setText(value)

    @property
    def _single_site_probecard_value(self):
        return self.singlesiteProbecard.text()

    @property
    def _multi_site_probecard_value(self):
        return self.multisiteProbecard.text()

    @_multi_site_probecard_value.setter
    def _multi_site_probecard_value(self, value):
        self.multisiteProbecard.setText(value)

    @property
    def _single_site_dib_value(self):
        return self.singlesiteDIB.text()

    @property
    def _multi_site_dib_value(self):
        return self.multisiteDIB.text()

    @_multi_site_dib_value.setter
    def _multi_site_dib_value(self, value):
        self.multisiteDIB.setText(value)

    def _get_current_configuration(self):
        return {'SingleSiteLoadboard': self.singlesiteLoadboard.text(),
                'SingleSiteDIB': self.singlesiteDIB.text(),
                'SignleSiteProbeCard': self.singlesiteProbecard.text(),
                'MultiSiteLoadboard': self.multisiteLoadboard.text(),
                'MultiSiteDIB': self.multisiteDIB.text(),
                'MultiSiteProbeCard': self.multisiteProbecard.text(),
                'MaxParallelism': int(self.maxParallelism.currentText()),
                'Actuator': {},
                'Instruments': {},
                'Parallelism': self._available_pattern}

# instruments
    def testerChanged(self, new_tester):
        print(f"testerChanged to '{new_tester}'")

    def availableInstrumentsSelectionChanged(self):
        print("available Instruments selection changed")

    def addingInstrument(self):
        print("adding instrument")

    def removingInstrument(self):
        print("removing instrument")

    def checkInstrumentUsage(self):
        print("check Instrument Usage")

    def usedInstrumentsSelectionChanged(self):
        print("used instruments selection changed")

# Actuator
    def availableActuatorSelectionChanged(self):
        print("available Actuator selection changed")

    def collapseAvailableInstruments(self):
        print("collapse available Instruments")

    def expandAvailableInstruments(self):
        print("exapnding available Instruments")

    def addingActuator(self):
        print("adding Actuator")

    def removingActuator(self):
        print("removing Actuator")

    def checkActuatorUsage(self):
        print("check Actuator Usage")

    def usedActuatorSelectionChanged(self):
        print("used Actuator selection changed")

# Parallelism
# General
    def CancelButtonPressed(self):
        self.reject()

    def OKButtonPressed(self):
        self.accept()


def new_hardwaresetup_dialog(project_info):
    """This function does the following:

        1. calls the wizard
        2. collects the defininition
        3. calls the navigator method 'add_hardware'
    """
    hd = {}
    nhw = HardwareWizard(project_info)
    if nhw.exec_():  # OK button pressed
        hd['hardware'] = nhw.hardware.text()
        hd['PCB'] = {
            'SingleSiteLoadboard': nhw.singlesiteLoadboard.text(),
            'SingleSiteProbecard': nhw.singlesiteProbecard.text(),
            'SingleSiteDIB': nhw.singlesiteDIB.text(),
            'SingleSiteDIBisCable': nhw.singleSiteDIBisCable.isChecked(),
            'MaxParallelism': int(nhw.maxParallelism.currentText()),
            'MultiSiteLoadboard': nhw.multisiteLoadboard.text(),
            'MultiSiteProbecard': nhw.multisiteProbecard.text(),
            'MultiSiteDIB': nhw.multisiteDIB.text(),
            'MultiSiteDIBisCable': nhw.multiSiteDIBisCable.isChecked()}
        hd['tester'] = nhw.tester.currentText()
        # TODO: Instruments
        # TODO: Actuators
        # TODO: Parallelism
    else:  # Cancel button pressed --> returns an empty dictionary.
        pass
    nhw.project_info.add_hardware(hd)
    del(nhw)


def edit_hardwaresetup_dialog(project_info, hardware_name):
    hd = project_info.get_hardware_definition(hardware_name)
    print(f"edit hardware : {hd}")
    ehw = HardwareWizard(project_info, hd)
    if ehw.exec_():  # OK button pressed
        # hd['hardware'] = ehw.hardware.text() hardware name is not editable !
        hd['PCB'] = {
            'SingleSiteLoadboard': ehw.singlesiteLoadboard.text(),
            'SingleSiteProbecard': ehw.singlesiteProbecard.text(),
            'SingleSiteDIB': ehw.singlesiteDIB.text(),
            'SingleSiteDIBisCable': ehw.singleSiteDIBisCable.isChecked(),
            'MaxParallelism': int(ehw.maxParallelism.currentText()),
            'MultiSiteLoadboard': ehw.multisiteLoadboard.text(),
            'MultiSiteProbecard': ehw.multisiteProbecard.text(),
            'MultiSiteDIB': ehw.multisiteDIB.text(),
            'MultiSiteDIBisCable': ehw.multiSiteDIBisCable.isChecked()}
        hd['tester'] = ehw.tester.currentText()
        # TODO: Instruments
        # TODO: Actuators
        # TODO: Parallelism
    else:  # Cancel button pressed --> returns an empty dictionary.
        pass
    ehw.project_info.update_hardware(hd)
    del(ehw)


if __name__ == '__main__':
    from ATE.org.navigation import ProjectNavigation, run_dummy_main
    project_info = ProjectNavigation(r'C:\Users\hoeren\__spyder_workspace__\CTCA')
    run_dummy_main(project_info, HardwareWizard)
