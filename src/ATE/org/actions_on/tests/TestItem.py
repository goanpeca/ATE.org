from ATE.org.actions_on.model.BaseItem import BaseItem
from ATE.org.actions_on.model.Constants import MenuActionTypes
from ATE.org.actions_on.tests.NewStandardTestWizard import new_standard_test_dialog
from ATE.org.actions_on.tests.TestWizard import new_test_dialog
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
        active_hardware = self.project_info.activeHardware
        active_base = self.project_info.activeBase
        if not active_base or not active_hardware:
            return

        test_list, path = self._get_available_tests(active_hardware, active_base)
        for test_entry in test_list:
            self.add_file_item(test_entry, path)

        self.observer = TestsObserver(path, self)
        self.observer.start_observer()

    def add_file_item(self, name, path):
        child = TestItemChild(os.path.splitext(name)[0], path, self)
        self.appendRow(child)

    def new_item(self):
        new_test_dialog(self.project_info)

    def import_item(self):
        pass

    def update(self):
        active_hardware = self.project_info.activeHardware
        active_base = self.project_info.activeBase
        # TODO: remove this after update toolbar class
        # problem here is that the toolbar does not emit the actual
        # hardware status when the application starts
        if not active_hardware:
            return

        if not active_base:
            self.set_children_hidden(True)
            if self.observer is not None:
                self.observer.stop_observer()
            return
        else:
            self.set_children_hidden(False)

        super().update()

    def _get_available_tests(self, active_hardware, active_base):
        from os import walk, path

        test_directory = path.join(self.project_info.project_directory, 'src',
                                   'tests', active_hardware, active_base)

        files = []
        for _, _, filenames in walk(test_directory):
            files.extend([path.splitext(x)[0] for x in filenames if not x == '__init__.py' and path.splitext(x)[1] == '.py'])
            break

        return files, test_directory

    def add_standard_test_item(self):
        new_standard_test_dialog(self.project_info)

    def _get_menu_items(self):
        return [MenuActionTypes.Add(),
                MenuActionTypes.AddStandardTest(),
                MenuActionTypes.Import()]


class TestItemChild(BaseItem):
    def __init__(self, name, path, parent, project_info=None):
        super().__init__(project_info, name, parent)
        self.path = os.path.join(path, name + '.py')
        self.file_system_operator = FileSystemOperator(self.path)

    def update_item(self, path):
        name = os.path.basename(os.path.splitext(path)[0])
        self.path = path
        self.setText(name)
        self.file_system_operator = FileSystemOperator(self.path)

    def edit_item(self):
        self.model().edit_file.emit(self.path)

    def delete_item(self):
        self.file_system_operator.delete_file()
        self.model().delete_file.emit(self.path)

    def _get_menu_items(self):
        return [MenuActionTypes.Edit(),
                None,
                MenuActionTypes.Delete()]
