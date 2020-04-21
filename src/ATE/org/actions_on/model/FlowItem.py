from ATE.org.actions_on.model.BaseItem import BaseItem as BaseItem
from ATE.org.actions_on.model.Constants import MenuActionTypes

from PyQt5 import QtCore, QtGui, QtWidgets


class SimpleFlowItem(BaseItem):
    def __init__(self, main, name, tooltip, parent):
        super().__init__(main, name, parent)
        self.setToolTip(tooltip)
        # ToDo (SPYD11): These items need to be able to attach
        # Testprograms.

    def _generate_sub_items(self):
        pass

    def _get_menu_items(self):
        return []


class FlowItem(BaseItem):
    def __init__(self, project_info, name, parent=None):
        super().__init__(project_info, name, parent)

    def update(self):
        if self.project_info.activeProduct == '' or self.project_info.activeProduct is None:
            self.set_children_hidden(True)
            return
        else:
            self.set_children_hidden(False)

        for c in range(int(0), self.row_count()):
            item = self.child(c)
            item.update()


class QualiFlowItemBase(FlowItem):
    def __init__(self, project_info, name, implmodule, parent=None):
        super().__init__(project_info, name, parent)
        import importlib
        self.mod = importlib.import_module(implmodule)
        self.setToolTip(getattr(self.mod, "quali_flow_tooltip"))
        self.setText(getattr(self.mod, "quali_flow_listentry_name"))
        self.flowname = (getattr(self.mod, "quali_flow_name"))
        self.modname = implmodule
        self._generate_sub_items()

    def _generate_sub_items(self):
        pass

    def _get_menu_items(self):
        return [MenuActionTypes.Add()]


class SingleInstanceQualiFlowItem(QualiFlowItemBase):
    def _get_menu_items(self):
        return [MenuActionTypes.Edit(),
                MenuActionTypes.View()]

    def edit_item(self):
        edit_func = getattr(self.mod, "edit_item")
        edit_func(self.project_info, self.project_info.activeProduct)

    def view_item(self):
        edit_func = getattr(self.mod, "view_item")
        edit_func(self.project_info, self.project_info.activeProduct)

    def _generate_sub_items(self):
        # ToDo: Display all testprogramms associated with this flow here.
        pass


class MultiInstanceQualiFlowItem(QualiFlowItemBase):
    def __init__(self, project_info, name, implmodule, parent=None):
        super().__init__(project_info, name, implmodule, parent)

    def update(self):
        super().update()
        self.removeRows(0, self.row_count())
        self._generate_sub_items()

    def _generate_sub_items(self):
        for subflow in self.project_info.get_data_for_qualification_flow(self.flowname, self.project_info.activeProduct):
            self.appendRow(QualiFlowSubitemInstance(self.project_info, subflow[0], self.project_info.activeProduct, subflow[3], self.modname, self))

    def _get_menu_items(self):
        return [MenuActionTypes.Add()]

    def new_item(self):
        new_func = getattr(self.mod, "new_item")
        new_func(self.project_info, self.project_info.activeProduct)


class QualiFlowSubitemInstance(BaseItem):
    def __init__(self, project_info, name, product, data, implmodule, parent):
        super().__init__(project_info, name, parent)
        import importlib
        self.mod = importlib.import_module(implmodule)
        self.product = product
        self.data = data

    def _get_menu_items(self):
        return [MenuActionTypes.Edit(),
                MenuActionTypes.View(),
                MenuActionTypes.Delete()]

    def edit_item(self):
        edit_func = getattr(self.mod, "edit_item")
        edit_func(self.project_info, self.data)

    def display_item(self):
        edit_func = getattr(self.mod, "view_item")
        edit_func(self.project_info, self.data)

    def delete_item(self):
        self.project_info.delete_qualifiaction_flow_instance(self.data)
