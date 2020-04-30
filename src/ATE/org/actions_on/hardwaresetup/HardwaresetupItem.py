from ATE.org.actions_on.hardwaresetup.HardwareWizard import new_hardwaresetup_dialog
from ATE.org.actions_on.hardwaresetup.EditHardwaresetupWizard import edit_hardwaresetup_dialog
from ATE.org.actions_on.hardwaresetup.ViewHardwaresetupSettings import display_hardware_settings_dialog

from ATE.org.actions_on.model.Constants import MenuActionTypes
from ATE.org.actions_on.model.BaseItem import BaseItem
from ATE.org.actions_on.utils.StateItem import StateItem


class HardwaresetupItem(BaseItem):
    def __init__(self, project_info, name, parent=None):
        super().__init__(project_info, name, parent=parent)
        self.child_set = self._get_children_names()

        self.hidden_children = []

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


class HardwaresetupItemChild(StateItem):
    def __init__(self, project_info, name, parent=None):
        super().__init__(project_info, name, parent=parent)
        self.definition = self._get_definition()

    def _get_dependant_objects(self):
        return self.project_info.get_dependant_objects_for_hardware(self.text())

    def activate_item(self):
        self.project_info.update_active_hardware(self.text())

    def edit_item(self):
        edit_hardwaresetup_dialog(self.project_info, self.text())

    def display_item(self):
        display_hardware_settings_dialog(self.text(), self.project_info)

    def trace_item(self):
        from ATE.org.actions_on.utils.ItemTrace import ItemTrace
        ItemTrace(self.dependency_list, self.text())

    def is_enabled(self):
        return self.project_info.get_hardware_state(self.text())

    def _get_definition(self):
        return self.project_info.get_hardware_definition(self.text())

    def _update_item_state(self, enabled):
        self.project_info.update_hardware_state(self.text(), enabled)
        return enabled

    def _enabled_item_menu(self):
        return [MenuActionTypes.Activate(),
                MenuActionTypes.Edit(),
                MenuActionTypes.View(),
                MenuActionTypes.Trace(),
                None,
                MenuActionTypes.Obsolete()]
