from ATE.org.actions_on.maskset.NewMasksetWizard import new_maskset_dialog
from ATE.org.actions_on.maskset.EditMasksetWizard import edit_maskset_dialog
from ATE.org.actions_on.maskset.ViewMasksetSettings import display_maskset_settings_dialog

from ATE.org.actions_on.model.Constants import MenuActionTypes
from ATE.org.actions_on.model.BaseItem import BaseItem


class MasksetItem(BaseItem):
    def __init__(self, project_info, name, parent=None):
        super().__init__(project_info, name, parent=parent)
        self.child_set = self._get_children_names()

    def _get_children_names(self):
        return self.project_info.get_masksets()

    def _create_child(self, name, parent):
        return MasksetItemChild(self.project_info, name, parent)

    def _append_children(self):
        children = self._get_children_names()
        for child in children:
            child_item = self._create_child(child, self)
            self.appendRow(child_item)

    def new_item(self):
        new_maskset_dialog(self.project_info)

    def _get_menu_items(self):
        return [MenuActionTypes.Add()]


class MasksetItemChild(BaseItem):
    def __init__(self, project_info, name, parent=None):
        super().__init__(project_info, name, parent=parent)

    def edit_item(self):
        edit_maskset_dialog(self.project_info, self.text())

    def display_item(self):
        configuration = self.project_info.get_maskset_definition(self.text())
        display_maskset_settings_dialog(configuration, self.text())

    def delete_item(self):
        pass

    def _get_menu_items(self):
        return [MenuActionTypes.Edit(),
                MenuActionTypes.View(),
                None,
                MenuActionTypes.Delete()]
