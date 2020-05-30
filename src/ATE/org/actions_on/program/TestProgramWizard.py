from PyQt5 import QtGui, QtCore, QtWidgets, uic
import sys
import os
import re
from enum import Enum


class Action(Enum):
    Up = 'Up'
    Down = 'Down'
    Left = 'Left'
    Right = 'Right'

    def __call__(self):
        return self.value


class Sequencer(Enum):
    Static = 'Fixed Temperature'  # 'Static'
    Dynamic = 'Variable Temperature'  # 'Dynamic'

    def __call__(self):
        return self.value


class ErrorMessage(Enum):
    NotSelected = 'no test is selected'
    InvalidInput = 'invalid input'
    InvalidTemperature = 'invalid temperature value(s)'
    OutOfRange = 'value out of range'
    TargetMissed = 'target is missing'
    UsertextMissed = 'usertext is missing'
    TemperatureMissed = 'temperature is missing'
    NoTestSelected = 'no test was selected'
    MultipleTestSelection = 'multiple tests are selected'
    EmtpyTestList = 'no test was choosen'
    TestProgramExists = 'test program name exists already'

    def __call__(self):
        return self.value


DEFAULT_TEMPERATURE = '25'


class TestProgramWizard(QtWidgets.QDialog):
    def __init__(self, project_info, owner, parent=None, read_only=False, edit_on=True):
        super().__init__(parent)
        self.project_info = project_info
        self.owner = owner

        self.available_tests = []
        self.selected_tests = []
        self.read_only = read_only
        self.edit_on = edit_on

        self.current_selected_test = None
        self.result = None

        self._load_ui()
        self._setup()
        self._view()
        self._connect_event_handler()

    def _load_ui(self):
        ui = __file__.replace('.py', '.ui')
        uic.loadUi(ui, self)

    def _setup(self):
        # windows setup
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)

        self.setWindowTitle(' '.join(re.findall('.[^A-Z]*', os.path.basename(__file__).replace('.py', ''))))
        self.setWindowTitle("Test Program Configuration")

        # TODO: do we need tool tips
        # self.RightButton.setToolTip("select")

        self._set_icon(self.testAdd, 'arrow-right')
        self._set_icon(self.testRemove, 'arrow-left')
        self._set_icon(self.moveTestDown, 'arrow-down')
        self._set_icon(self.moveTestUp, 'arrow-up')

        self._resize_table(self.parametersInput, 50)
        self._resize_table(self.parametersOutput, 50)

        from ATE.org.validation import valid_float_regex
        regx = QtCore.QRegExp(valid_float_regex)
        self.positive_float_validator = QtGui.QRegExpValidator(regx, self)

        self.existing_programs = self.project_info.get_programs_for_owner(self.owner)

    def _connect_event_handler(self):
        self.availableTests.itemClicked.connect(self._available_test_selected)
        self.selectedTests.itemClicked.connect(self._test_selected)

        self.parametersInput.itemDoubleClicked.connect(self._double_click_handler_input_param)
        self.parametersOutput.itemDoubleClicked.connect(self._double_click_handler_output_param)

        self.testAdd.clicked.connect(lambda: self._move_test(Action.Right()))
        self.moveTestDown.clicked.connect(lambda: self._move_test(Action.Down()))
        self.moveTestUp.clicked.connect(lambda: self._move_test(Action.Up()))
        self.testRemove.clicked.connect(lambda: self._move_test(Action.Left()))

        self.hardware.currentIndexChanged.connect(self._hardware_changed)
        self.base.currentIndexChanged.connect(self._base_changed)
        self.usertext.textChanged.connect(self._usertext_changed)

        self.sequencerType.currentIndexChanged.connect(self._sequencer_type_changed)
        self.temperature.textChanged.connect(self._verify_temperature)
        from ATE.org.validation import valid_user_text_name_regex
        user_text_reg_ex = QtCore.QRegExp(valid_user_text_name_regex)
        user_text_name_validator = QtGui.QRegExpValidator(user_text_reg_ex, self)
        self.usertext.setValidator(user_text_name_validator)

        self.OKButton.clicked.connect(self._save_configuration)
        self.CancelButton.clicked.connect(self._cancel)

    def _set_icon(self, button, icon_type):
        from ATE.org.actions_on.program.Actions import ACTIONS
        icon = QtGui.QIcon(ACTIONS[icon_type][0])
        button.setIcon(icon)
        button.setText("")

    def _resize_table(self, table, col_size):
        # resize cell columns
        for c in range(table.columnCount()):
            table.setColumnWidth(c, col_size)

        table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)

    def _view(self):
        self.existing_hardwares = self.project_info.get_hardwares()
        self.hardware.addItems(self.existing_hardwares)
        current_hw_index = self.hardware.findText(self.project_info.active_hardware, QtCore.Qt.MatchExactly)
        self.hardware.setCurrentIndex(current_hw_index)

        current_base_index = self.base.findText(self.project_info.active_base, QtCore.Qt.MatchExactly)
        self.base.setCurrentIndex(current_base_index)

        self._update_target()

        self.sequencerType.addItems([Sequencer.Static(), Sequencer.Dynamic()])
        self.temperature.setText(DEFAULT_TEMPERATURE)

        self.availableTests.addItems(self._get_available_tests())
        self.Feedback.setText('')
        self.Feedback.setStyleSheet('color:orange')
        self.usertext_feedback.setStyleSheet('color:orange')
        self.temperature_feedback.setStyleSheet('color:orange')
        self.target_feedback.setStyleSheet('color:orange')
        self.usertext_feedback.setStyleSheet('color:orange')
        self._verify()

    def _update_target(self):
        self.target.clear()
        if self.base.currentText() == 'PR':
            existing_targets = self.project_info.get_dies_for_hardware(self.hardware.currentText())
        else:
            existing_targets = self.project_info.get_devices_for_hardware(self.hardware.currentText())

        self.target.addItems(existing_targets)
        self.target.setCurrentIndex(0)

    @QtCore.pyqtSlot(str)
    def _usertext_changed(self, text):
        self._verify()

    @QtCore.pyqtSlot()
    def _hardware_changed(self):
        self._update_target()
        self._verify()

    @QtCore.pyqtSlot()
    def _base_changed(self):
        self._update_target()
        self._verify()

    @QtCore.pyqtSlot(int)
    def _sequencer_type_changed(self, index):
        if self.sequencerType.itemText(index) == Sequencer.Static():
            self.temperature.setText(DEFAULT_TEMPERATURE)
            return

        self.temperature.setText(f'{DEFAULT_TEMPERATURE},')

    @QtCore.pyqtSlot(QtWidgets.QListWidgetItem)
    def _available_test_selected(self, item):
        self.parametersInput.setEnabled(False)
        self.parametersOutput.setEnabled(False)

        self._handle_selection(self.availableTests, self.selectedTests, item)

    @QtCore.pyqtSlot(QtWidgets.QListWidgetItem)
    def _test_selected(self, item):
        self.parametersInput.setEnabled(True)
        self.parametersOutput.setEnabled(True)

        self._handle_selection(self.selectedTests, self.availableTests, item)

    def _handle_selection(self, selected_list, second_list, item):
        for index in range(second_list.count()):
            second_list.item(index).setSelected(False)

        if len(selected_list.selectedItems()) > 1:
            self.parametersInput.setRowCount(0)
            self.parametersOutput.setRowCount(0)
            self._update_feedback(ErrorMessage.MultipleTestSelection())
            return

        self._update_tables_parameters(item)

    def _update_tables_parameters(self, item):
        self.current_selected_test = item
        parameters = self.project_info.get_test_definiton(item.text())
        self.input_parameters = parameters['input_parameters']
        self.output_parameters = parameters['output_parameters']

        # update table content if content already changed
        if item.text() in self._selected_tests_list and \
           len(self.selectedTests.selectedItems()):
            test = self.selected_tests[self.selectedTests.currentRow()]
            input_params = list(test[item.text()]['input_parameters'].items())
            for param in input_params:
                self.input_parameters[param[0]]['Default'] = param[1]

            output_params = list(test[item.text()]['output_parameters'].items())
            for param in output_params:
                self.output_parameters[param[0]]['LTL'], self.output_parameters[param[0]]['UTL'] = \
                    test[item.text()]['output_parameters'][param[0]]['LTL'], \
                    test[item.text()]['output_parameters'][param[0]]['UTL']

        self._fill_input_parameter_table()
        self._fill_output_parameter_table()

    @QtCore.pyqtSlot(str)
    def _move_test(self, action):
        try:
            {Action.Up(): lambda: self._move_up(),
             Action.Down(): lambda: self._move_down(),
             Action.Left(): lambda: self._remove_from_testprogram(),
             Action.Right(): lambda: self._add_to_testprogram(),
             }[action]()
        except Exception:
            raise (f'action "{action}" not recognized')

    def _is_selected(self, test_list):
        selected_items = len(test_list.selectedItems())
        if not selected_items:
            return False
        return True

    @QtCore.pyqtSlot()
    def _move_up(self):
        if len(self.selectedTests.selectedItems()) > 1:
            return

        if not self._is_selected(self.selectedTests):
            self._update_feedback(ErrorMessage.NotSelected())
            return

        if self.selectedTests.currentRow() > 0:
            self._update_list_after_move(True)

    @QtCore.pyqtSlot()
    def _move_down(self):
        if len(self.selectedTests.selectedItems()) > 1:
            return

        if not self._is_selected(self.selectedTests):
            self._update_feedback(ErrorMessage.NotSelected())
            return

        if self.selectedTests.currentRow() < self.selectedTests.count() - 1:
            self._update_list_after_move(False)

    def _update_list_after_move(self, is_up):
        current_row = self.selectedTests.currentRow()
        current_row_item = self.selectedTests.currentItem()
        index = current_row - 1 if is_up else current_row + 1
        self.selectedTests.takeItem(current_row)
        self.selectedTests.insertItem(index, current_row_item)
        self.selectedTests.setCurrentItem(current_row_item)

    @QtCore.pyqtSlot()
    def _remove_from_testprogram(self):
        if not self._is_selected(self.selectedTests):
            self._update_feedback(ErrorMessage.NotSelected())
            return

        selected_items = len(self.selectedTests.selectedItems())
        for _ in range(selected_items):
            item = self.selectedTests.takeItem(self.selectedTests.currentRow())
            self.parametersInput.setRowCount(0)
            self.parametersOutput.setRowCount(0)
            self._remove_test(item)

        self._verify()

    @QtCore.pyqtSlot()
    def _add_to_testprogram(self):
        if not self._is_selected(self.availableTests):
            self._update_feedback(ErrorMessage.NotSelected())
            return

        for item in self.availableTests.selectedItems():
            self.selectedTests.addItem(f'{item.text()}')
            self.selected_tests.append(self._generate_test_struct(item.text()))

        self._verify()

    @QtCore.pyqtSlot(str)
    def _verify_temperature(self, text):
        if not text:
            self.temperature_feedback.setText(ErrorMessage.TemperatureMissed())
            return

        if self.sequencer_type == Sequencer.Static():
            if self._get_static_temp(text) is None:
                self.temperature_feedback.setText(ErrorMessage.InvalidTemperature())
                return

        if self.sequencer_type == Sequencer.Dynamic():
            if self._get_dynamic_temp(text) is None:
                self.temperature_feedback.setText(ErrorMessage.InvalidTemperature())
                return

        self.temperature_feedback.setText('')
        self.OKButton.setEnabled(True)

    def _get_static_temp(self, text):
        try:
            temp = int(text)

        except ValueError:
            self.temperature.setText(text[:-1])
            return None

        return [temp]

    # TODO: do we have to support other variant for dynamic temperature input
    # 25..100 ?
    def _get_dynamic_temp(self, text):
        temp_vars = []
        try:
            temps = text.split(',')
            if len(temps) == 0:
                return None

            for i in temps:
                if i != '':
                    temp_vars.append(int(i))

        except ValueError:
            self.temperature.setText(text[:-1])
            return None

        return temp_vars

    def _inset_selected_test(self, test=None):
        self.SelectedTests.addItem(f'{self.current_selected_test.text()}: {test}')

    def _get_available_tests(self):
        return self.project_info.get_tests_from_db(self.hardware.currentText(),
                                                   self.base.currentText(),
                                                   'custom')  # TODO: test type is missed, we use custon as default

    def _set_sample_visible_mode(self, is_visible):
        self.sample.setVisible(is_visible)
        self.sample_label.setVisible(is_visible)
        self.one_label.setVisible(is_visible)

    def _verify(self):
        success = True
        self.usertext_feedback.setText('')
        self.target_feedback.setText('')
        self.temperature_feedback.setText('')
        self._update_feedback('')

        if self.base.currentText() == 'PR':
            self._set_sample_visible_mode(False)
        else:
            self._set_sample_visible_mode(True)

        if not self.target.currentText():
            self.target_feedback.setText(ErrorMessage.TargetMissed())
            success = False

        if not self.temperature.text():
            self.temperature_feedback.setText(ErrorMessage.TemperatureMissed())
            success = False

        if not self.selectedTests.count():
            self._update_feedback(ErrorMessage.EmtpyTestList())
            success = False

        # TODO: implement when test-program name specified
        if self.edit_on and self.program_name in self.existing_programs:
            self._update_feedback(ErrorMessage.TestProgramExists())
            success = False

        if success:
            self.usertext_feedback.setText('')
            self.target_feedback.setText('')
            self.temperature_feedback.setText('')
            self._update_feedback('')
            self.OKButton.setEnabled(True)
        else:
            self.OKButton.setEnabled(False)

    @property
    def program_name(self):
        return f'Prog_{self.hardware.currentText()}_{self.base.currentText()}_{self.target.currentText()}_{self.usertext.text()}'

    @property
    def sequencer_type(self):
        return self.sequencerType.currentText()

    def _update_feedback(self, message):
        if not len(message) == 0:
            self.Feedback.setText(message)
            self.Feedback.setStyleSheet('color: orange')
            return

        self.Feedback.setStyleSheet('')
        self.Feedback.setText('')

    def _fill_input_parameter_table(self):
        self._clear_table_content(self.parametersInput)
        self.parametersInput.setRowCount(len(self.input_parameters))
        self.parametersInput.setColumnCount(6)
        fmt = '.0f'  # set format to zero as default
        row = 0
        for key, value in self.input_parameters.items():
            for col in range(self.parametersInput.columnCount()):
                parameter_name = self.parametersInput.item(row, 0)
                if parameter_name:
                    fmt = self.input_parameters[parameter_name.text()]['fmt']

                if col == 0:
                    name_item = QtWidgets.QTableWidgetItem(key)
                    name_item.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
                    name_item.setFlags(QtCore.Qt.NoItemFlags)
                    self.parametersInput.setItem(row, col, name_item)
                    continue
                elif col == 1:
                    item = QtWidgets.QTableWidgetItem(str(self._get_text(value['Min'], fmt)))
                elif col == 2:
                    item = self._generate_configurable_table_cell(value['Default'], fmt, 2)
                elif col == 3:
                    item = QtWidgets.QTableWidgetItem(str(self._get_text(value['Max'], fmt)))
                elif col == 4:
                    item = QtWidgets.QTableWidgetItem(value['Unit'])
                elif col == 5:
                    item = QtWidgets.QTableWidgetItem(value['fmt'])

                if col in (1, 3, 4, 5):
                    item.setFlags(QtCore.Qt.NoItemFlags)

                item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                self.parametersInput.setItem(row, col, item)

            row += 1

    def _get_text(self, value, fmt):
        return ('%' + fmt) % float(value)

    def _clear_table_content(self, table):
        for row in range(table.rowCount()):
            for col in range(table.columnCount()):
                table.removeCellWidget(row, col)

    def _fill_output_parameter_table(self):
        self._clear_table_content(self.parametersOutput)
        self.parametersOutput.setRowCount(len(self.output_parameters))
        self.parametersOutput.setColumnCount(7)
        row = 0
        header = self.parametersInput.horizontalHeader()
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        for key, value in self.output_parameters.items():
            for col in range(self.parametersOutput.columnCount()):
                parameter_name = self.parametersOutput.item(row, 0)
                if parameter_name:
                    fmt = self.output_parameters[parameter_name.text()]['fmt']

                if col == 0:
                    name_item = QtWidgets.QTableWidgetItem(key)
                    name_item.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
                    name_item.setFlags(QtCore.Qt.NoItemFlags)
                    self.parametersOutput.setItem(row, col, name_item)
                    continue
                elif col == 1:
                    item = QtWidgets.QTableWidgetItem(str(self._get_text(value['LSL'], fmt)))
                elif col == 2:
                    item = self._generate_configurable_table_cell(value['LTL'], fmt, 2)
                # TODO: should the nom be a part of the table
                # elif col == 3:
                #     item = QtWidgets.QTableWidgetItem(str(value['NOM']))
                elif col == 3:
                    item = self._generate_configurable_table_cell(value['UTL'], fmt, 3)
                elif col == 4:
                    item = QtWidgets.QTableWidgetItem(str(self._get_text(value['USL'], fmt)))
                elif col == 5:
                    item = QtWidgets.QTableWidgetItem(value['Unit'])
                elif col == 6:
                    item = QtWidgets.QTableWidgetItem(value['fmt'])

                if col in (1, 4, 5, 6):
                    item.setFlags(QtCore.Qt.NoItemFlags)

                item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                self.parametersOutput.setItem(row, col, item)

            row += 1

    def _generate_configurable_table_cell(self, value, fmt, cell):
        text = str(self._get_text(value, fmt))
        item = QtWidgets.QTableWidgetItem(text)
        # QFontMetrics used to get the pixel size of the text which is used
        # to resizing of the cell
        font = QtGui.QFont()
        metric = QtGui.QFontMetrics(font)
        text_size = metric.boundingRect(text).width()
        colum_size = self.parametersInput.columnWidth(cell)
        self.parametersOutput.setColumnWidth(cell, text_size + colum_size)

        if self.read_only:
            item.setFlags(QtCore.Qt.NoItemFlags)

        return item

    def _double_click_handler_input_param(self, item):
        self._create_checkable_cell(self.parametersInput, 'input', item)

    def _double_click_handler_output_param(self, item):
        self._create_checkable_cell(self.parametersOutput, 'output', item)

    def _create_checkable_cell(self, table, table_type, item):
        column = item.column()
        row = item.row()
        checkable_widget = QtWidgets.QLineEdit()
        checkable_widget.setText(item.text())

        checkable_widget.setValidator(self.positive_float_validator)

        table.setCellWidget(row, column, checkable_widget)
        checkable_widget.editingFinished.connect(lambda row=row, column=column,
                                                 checkable_widget=checkable_widget, table=table,
                                                 table_type=table_type:
                                                 self._edit_cell_done(table, table_type, checkable_widget, row, column))

    def _edit_cell_done(self, table, table_type, checkable_widget, row, column):
        param_type = table.item(row, 0).text()
        value = float(checkable_widget.text())

        if not len(self.selectedTests.selectedItems()):
            return

        test_name = self.selectedTests.selectedItems()[0].text()

        if table_type == 'input':
            self._validate_input_parameter(test_name, value, param_type)
        else:
            self._validate_output_parameter(test_name, value, param_type, column)

    def _validate_output_parameter(self, test_name, value, param_type, column):
        limits = (self.output_parameters[param_type]['LSL'], self.output_parameters[param_type]['USL'])
        limit = 'LTL'
        if column == 3:
            limit = 'UTL'

        if not self._is_valid_value(value, limits) or \
           not self._is_valid_output_value(value, param_type, limit):
            self._fill_output_parameter_table()
            self._update_feedback(ErrorMessage.OutOfRange())
            return

        self._verify()
        self.output_parameters[param_type][limit] = value
        self._update_selected_tests_parameters(test_name,
                                               'output_parameters',
                                               param_type,
                                               value,
                                               limit)
        self._fill_output_parameter_table()

    def _is_valid_output_value(self, value, param_type, limit):
        import numpy as np

        if str(self.output_parameters[param_type]['UTL']) == str(np.nan) and limit != 'UTL' or \
           str(self.output_parameters[param_type]['LTL']) == str(np.nan) and limut != 'LTL':
            return True

        if limit == 'LTL':
            return self.output_parameters[param_type]['UTL'] > value

        if limit == 'UTL':
            return self.output_parameters[param_type]['LTL'] < value

    def _validate_input_parameter(self, test_name, value, param_type):
        limits = (self.input_parameters[param_type]['Min'], self.input_parameters[param_type]['Max'])
        if not self._is_valid_value(value, limits):
            self._fill_input_parameter_table()
            self._update_feedback(ErrorMessage.OutOfRange())
            return

        self._verify()
        self.input_parameters[param_type]['Default'] = value
        self._update_selected_tests_parameters(test_name,
                                               'input_parameters',
                                               param_type,
                                               value)
        self._fill_input_parameter_table()

    def _is_valid_value(self, value, limits):
        left_limit = limits[0]
        right_limit = limits[1]
        if left_limit == '-inf' and right_limit == 'inf':
            return True

        if left_limit == '-inf':
            return value <= float(right_limit)

        if right_limit == 'inf':
            return value >= float(left_limit)

        return float(left_limit) <= value <= float(right_limit)

    @property
    def _selected_tests_list(self):
        selected_tests = []
        for index in range(self.selectedTests.count()):
            selected_tests.append(self.selectedTests.item(index).text())

        return selected_tests

    def _remove_test(self, item):
        index = self._get_test_index(item.text())
        if index == -1:
            return

        self.selected_tests.pop(index)

    def _generate_test_struct(self, test_name):
        sturct = {test_name: {'input_parameters': {'Value': None}, 'output_parameters': {'Out': {'UTL': '', 'LTL': ''}}}}
        parameters = self.project_info.get_test_definiton(test_name)
        inputs = {}
        outputs = {}
        for key, value in parameters['input_parameters'].items():
            inputs[key] = value['Default']

        for key, value in parameters['output_parameters'].items():
            outputs[key] = {'LTL': value['LTL'], 'UTL': value['UTL']}

        sturct[test_name].update({'input_parameters': inputs})
        sturct[test_name].update({'output_parameters': outputs})
        return sturct

    def _get_test_index(self, test_name):
        for index, test in enumerate(self.selected_tests):
            test_tuple = list(test.items())
            if test_tuple[0][0] == test_name:
                return index

        return -1

    def _update_selected_tests_parameters(self, test_name, type, parameter_name, value, limit=''):
        index = self.selectedTests.currentRow()
        if not limit:
            self.selected_tests[index][test_name][type][parameter_name] = value
        else:
            self.selected_tests[index][test_name][type][parameter_name][limit] = value

    def _get_configuration(self):
        configuration = {'name': f'Prog_{self.hardware.currentText()}_{self.base.currentText()}_{self.target.currentText()}_{self.usertext.text()}',
                         'hardware': self.hardware.currentText(),
                         'base': self.base.currentText(),
                         'target': self.target.currentText(),
                         'usertext': self.usertext.text(),
                         'sequencer_type': self.sequencer_type,
                         'temperature': self.temperature.text(),
                         'sample': self.sample.suffix()}

        definition = {'sequence': self.selected_tests}

        return configuration, definition

    def _save_configuration(self):
        configuration, definition = self._get_configuration()

        if configuration is None:
            return

        if not self.read_only and self.edit_on:
            self.project_info.insert_program(configuration['name'], configuration['hardware'], configuration['base'], configuration['target'],
                                             configuration['usertext'], configuration['sequencer_type'], configuration['temperature'],
                                             definition, self.owner, self.project_info.get_program_owner_element_count(self.owner))
        else:
            self.project_info.update_program(configuration['name'], configuration['hardware'], configuration['base'],
                                             configuration['target'], configuration['usertext'], configuration['sequencer_type'],
                                             configuration['temperature'], definition, self.owner)

        self.accept()

    def _cancel(self):
        self.reject()


def new_program_dialog(project_info, owner, parent):
    testProgramWizard = TestProgramWizard(project_info, owner, parent)
    testProgramWizard.exec_()
    del(testProgramWizard)


if __name__ == '__main__':
    import qdarkstyle
    app = QtWidgets.QApplication([])
    app.setStyleSheet(qdarkstyle.load_stylesheet_from_environment())

    with TestProgramWizard() as win:
        sys.exit(app.exec_())
