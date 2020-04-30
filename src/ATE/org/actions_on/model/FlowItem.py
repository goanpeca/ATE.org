from ATE.org.actions_on.model.BaseItem import BaseItem as BaseItem
from ATE.org.actions_on.model.Constants import MenuActionTypes


def generate_item_name(item):
    # construct a unique name for this item. Since SimpleItems
    # exist in multiple versions with the same basic name, we construct
    # the name based on
    # - the given name
    # - the active target
    # - the active base
    if None in [item.project_info.active_target, item.project_info.active_base]:
        return None

    owner_name = item.text() + item.project_info.active_target + item.project_info.active_base
    return owner_name


def append_test_program_nodes(item):
    owner_name = generate_item_name(item)

    for tp in item.project_info.get_programs_for_owner(owner_name):
        item.appendRow(TestprogramTreeItem(item.project_info, tp, owner_name))


def add_test_program(item):
    import ATE.org.actions_on.program.NewProgramWizard as np
    result = np.new_program_dialog(None)
    if result is not None:
        itemname = generate_item_name(item)
        item.project_info.insert_program_owner(result, itemname)


class FlowItem(BaseItem):
    def __init__(self, project_info, name, parent=None):
        super().__init__(project_info, name, parent)

    def update(self):
        if self.project_info.active_target == '' or self.project_info.active_target is None:
            self.set_children_hidden(True)
            return
        else:
            self.set_children_hidden(False)

        for c in range(int(0), self.row_count()):
            item = self.child(c)
            item.update()


class SimpleFlowItem(FlowItem):
    '''
        The simple flow item is any flow item which
        only has flow instances (i.e. testprograms!)
        as children.
    '''
    def __init__(self, project_info, name, tooltip=""):
        super().__init__(project_info, name, None)
        self.setToolTip(tooltip)

    def update(self):
        super().update()
        self.removeRows(0, self.row_count())
        append_test_program_nodes(self)

    def new_item(self):
        add_test_program(self)

    def _get_menu_items(self):
        return [MenuActionTypes.Add()]


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
                MenuActionTypes.View(),
                MenuActionTypes.Add()]

    def edit_item(self):
        edit_func = getattr(self.mod, "edit_item")
        edit_func(self.project_info, self.project_info.active_target)

    def view_item(self):
        edit_func = getattr(self.mod, "view_item")
        edit_func(self.project_info, self.project_info.active_target)

    def new_item(self):
        add_test_program(self)

    def _generate_sub_items(self):
        append_test_program_nodes(self)


class MultiInstanceQualiFlowItem(QualiFlowItemBase):
    def __init__(self, project_info, name, implmodule, parent=None):
        super().__init__(project_info, name, implmodule, parent)

    def update(self):
        super().update()
        self.removeRows(0, self.row_count())
        self._generate_sub_items()

    def _generate_sub_items(self):
        for subflow in self.project_info.get_data_for_qualification_flow(self.flowname, self.project_info.active_target):
            self.appendRow(QualiFlowSubitemInstance(self.project_info, subflow[0], self.project_info.active_target, subflow[3], self.modname, self))

    def _get_menu_items(self):
        return [MenuActionTypes.Add()]

    def new_item(self):
        new_func = getattr(self.mod, "new_item")
        new_func(self.project_info, self.project_info.active_target)


class QualiFlowSubitemInstance(BaseItem):
    def __init__(self, project_info, name, product, data, implmodule, parent):
        super().__init__(project_info, name, parent)
        import importlib
        self.mod = importlib.import_module(implmodule)
        self.product = product
        self.data = data
        self._generate_sub_items()

    def _get_menu_items(self):
        return [MenuActionTypes.Edit(),
                MenuActionTypes.View(),
                MenuActionTypes.Delete(),
                None,
                MenuActionTypes.Add()]

    def edit_item(self):
        edit_func = getattr(self.mod, "edit_item")
        edit_func(self.project_info, self.data)

    def display_item(self):
        edit_func = getattr(self.mod, "view_item")
        edit_func(self.project_info, self.data)

    def delete_item(self):
        self.project_info.delete_qualifiaction_flow_instance(self.data)

    def new_item(self):
        add_test_program(self)

    def _generate_sub_items(self):
        append_test_program_nodes(self)


class TestprogramTreeItem(BaseItem):
    def __init__(self, project_info, name, owner):
        super().__init__(project_info, name, None)
        self.owner = owner

    def _get_menu_items(self):
        return [MenuActionTypes.Edit(),
                MenuActionTypes.View(),
                MenuActionTypes.Delete()]

    def edit_item(self):
        pass

    def display_item(self):
        pass

    def delete_item(self):
        self.project_info.delete_program_owner(self.text(), self.owner)
