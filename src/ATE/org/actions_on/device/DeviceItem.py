from ATE.org.actions_on.device.NewDeviceWizard import new_device_dialog

from ATE.org.actions_on.model.Constants import MenuActionTypes
from ATE.org.actions_on.model.BaseItem import BaseItem


class DeviceItem(BaseItem):
    def __init__(self, project_info, name, parent=None):
        super().__init__(project_info, name, parent=parent)
        self.child_set = self._get_children_names()

    def _get_children_names(self):
        return self.project_info.get_devices()

    def _create_child(self, name, parent):
        return DeviceItemChild(self.project_info, name, parent)

    def _append_children(self):
        children = self._get_children_names()
        for child in children:
            child_item = self._create_child(child, self)
            self.appendRow(child_item)

    def _get_menu_items(self):
        return [MenuActionTypes.Add()] 

    def new_item(self):
        new_device_dialog(self.project_info, self.active_hardware)


class DeviceItemChild(BaseItem):
    def __init__(self, project_info, name, parent=None):
        super().__init__(project_info, name, parent=parent)

    def edit_item(self):
        pass

    def display_item(self):
        pass

    def delete_item(self):
        pass

    def _get_menu_items(self):
        return [MenuActionTypes.Edit(),
                MenuActionTypes.View(),
                None,
                MenuActionTypes.Delete()]
