from ATE.org.actions_on.hardwaresetup.NewHardwaresetupWizard import new_hardwaresetup_dialog
from ATE.org.actions_on.hardwaresetup.EditHardwaresetupWizard import edit_hardwaresetup_dialog
from ATE.org.actions_on.hardwaresetup.ViewHardwaresetupSettings import display_hardware_settings_dialog

from ATE.org.actions_on.model.Constants import MenuActionTypes
from ATE.org.actions_on.model.BaseItem import BaseItem


class HardwaresetupItem(BaseItem):
    def __init__(self, project_info, name, parent=None):
        super().__init__(project_info, name, parent=parent)
        self.child_set = self._get_children_names()

        self.hidden_children = []
        self._is_hidden = False

    def _get_children_names(self):
        return self.project_info.get_hardwares()

    def _create_child(self, name, parent):
        return HardwaresetupItemChild(self.project_info, name, parent)

    def _append_children(self):
        children = self._get_children_names()
        for child in children:
            child_item = self._create_child(child, self)
            self.appendRow(child_item)

    def new_item(self):
        new_hardwaresetup_dialog(self.project_info)

    def _get_menu_items(self):
        return [MenuActionTypes.Add()]


class HardwaresetupItemChild(BaseItem):
    def __init__(self, project_info, name, parent=None):
        super().__init__(project_info, name, parent=parent)

    def edit_item(self):
        edit_hardwaresetup_dialog(self.project_info, self.text())

    def display_item(self):
        configuration = self.project_info.get_hardware_definition(self.text())
        display_hardware_settings_dialog(configuration, self.text())

    def delete_item(self):
        # TODO: implement this
        # self.parent.removeRow(self.row())
        # self.emitDataChanged()
        pass

    def _get_menu_items(self):
        return [MenuActionTypes.Edit(),
                MenuActionTypes.View(),
                None,
                MenuActionTypes.Delete()]
