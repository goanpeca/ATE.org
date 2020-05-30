from ATE.org.actions_on.model.BaseItem import BaseItem
from ATE.org.actions_on.utils.StateItem import StateItem
from ATE.org.actions_on.model.Constants import MenuActionTypes
from ATE.org.actions_on.tests.NewStandardTestWizard import new_standard_test_dialog
from ATE.org.actions_on.tests.TestWizard import new_test_dialog
from ATE.org.actions_on.tests.TestWizard import edit_test_dialog
from ATE.org.actions_on.utils.FileSystemOperator import FileSystemOperator
from ATE.org.actions_on.tests.TestsObserver import TestsObserver

import os


class TestItem(BaseItem):
    def __init__(self, project_info, name, path, parent=None):
        super().__init__(project_info, name, parent)
        self.set_children_hidden(True)
        self.observer = None
        self.file_system_operator = FileSystemOperator(path)

    def _append_children(self):
        active_hardware = self.project_info.active_hardware
        active_base = self.project_info.active_base
        if not active_base or not active_hardware:
            return

        test_list, path = self._get_available_tests(active_hardware, active_base)
        for test_entry in test_list:
            self.add_file_item(test_entry, path)

        if self.observer is None:
            self.observer = TestsObserver(path, self)
            self.observer.start_observer()

    def add_file_item(self, name, path):
        child = TestItemChild(os.path.splitext(name)[0], path, self, self.project_info)
        self.appendRow(child)

    def new_item(self):
        new_test_dialog(self.project_info)

    def import_item(self):
        pass

    def update(self):
        active_hardware = self.project_info.active_hardware
        active_base = self.project_info.active_base

        if not active_hardware or \
           not active_base:
            self.set_children_hidden(True)
            if self.observer is not None:
                self.observer.stop_observer()
                self.observer = None
            return
        else:
            self.set_children_hidden(False)

        super().update()

    def _get_available_tests(self, active_hardware, active_base):
        from os import walk, path

        test_directory = path.join(self.project_info.project_directory, 'src',
                                   active_hardware, active_base)

        file_names = []
        for _, directories, _ in walk(test_directory):
            file_names = [x for x in directories if '_' not in x]
            break

        return file_names, test_directory

    def add_standard_test_item(self):
        new_standard_test_dialog(self.project_info)

    def _get_menu_items(self):
        return [MenuActionTypes.Add(),
                MenuActionTypes.AddStandardTest(),
                MenuActionTypes.Import()]


class TestItemChild(StateItem):
    def __init__(self, name, path, parent, project_info):
        super().__init__(project_info, name, parent)
        self.path = os.path.join(path, name, name + '.py')
        self.file_system_operator = FileSystemOperator(self.path)

    def update_item(self, path):
        name = os.path.basename(os.path.splitext(path)[0])
        self.path = path
        self.setText(name)
        self.file_system_operator = FileSystemOperator(self.path)

    def edit_item(self):
        definition = self.project_info.get_test_definition(self.text())
        edit_test_dialog(self.project_info, definition)

    def open_file_item(self):
        path = os.path.dirname(self.path)
        dirname, _ = os.path.splitext(os.path.basename(self.path))
        filename = os.path.basename(self.path)
        path = os.path.join(path, filename)

        self.model().edit_file.emit(path)

    def delete_item(self):
        from ATE.org.actions_on.utils.ItemTrace import ItemTrace
        if not ItemTrace(self.dependency_list, self.text(), message=f"Are you sure you want to delete ?").exec_():
            return

        # emit event to update tab view
        self.model().delete_file.emit(self.path)

        import shutil
        shutil.rmtree(os.path.dirname(self.path))
        self.project_info.remove_test(self.text())

    @property
    def dependency_list(self):
        return self.project_info.get_dependant_objects_for_test(self.text())

    def is_enabled(self):
        return self.project_info.get_test_state(self.text())

    def _update_db_state(self, enabled):
        self.project_info.update_test_state(self.text(), enabled)

    def _are_dependencies_fulfilled(self):
        dependency_list = {}

        hw = self.project_info.get_test_hardware(self.text())
        if not hw:
            return dependency_list

        hw_enabled = self.project_info.get_hardware_state(hw[0])

        if not hw_enabled:
            dependency_list.update({'hardwares': hw})

        return dependency_list

    def _enabled_item_menu(self):
        return [MenuActionTypes.OpenFile(),
                MenuActionTypes.Edit(),
                MenuActionTypes.Trace(),
                None,
                MenuActionTypes.Delete()]
