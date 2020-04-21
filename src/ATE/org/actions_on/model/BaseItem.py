from PyQt5 import QtCore, QtGui, QtWidgets


class BaseItem(QtGui.QStandardItem):
    def __init__(self, project_info, name, parent=None):
        super().__init__(name)
        self.parent = parent
        self.project_info = project_info

        self.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.setToolTip(self._get_tooltip())

        self.hidden_children = []
        self._is_hidden = False

        self.menu = QtWidgets.QMenu()
        self._init_menu()

        self._append_children()

    def _init_menu(self):
        from ATE.org.actions_on.model.Actions import ACTIONS

        for action_type in self._get_menu_items():
            if not action_type:
                self.menu.addSeparator()
                continue

            action = ACTIONS[action_type]
            action = self.menu.addAction(action[0], action[1])
            action.triggered.connect(getattr(self, action_type))

    # TODO: at some point we are not going to need parameters any more, remove them
    def exec_context_menu(self, active_hardware, active_base, active_target):
        # dirty hack
        self.active_hardware = active_hardware
        self.base = active_base
        self.target = active_target

        if self.is_hidden():
            return

        self.menu.exec_(QtGui.QCursor.pos())

    def update(self):
        self.removeRows(0, self.rowCount())
        self._append_children()

    def row_count(self):
        return self.rowCount()

    def new_item(self):
        pass

    def edit_item(self):
        pass

    def delete_item(self):
        pass

    def display_item(self):
        pass

    def import_item(self):
        pass

    def clone_from_item(self):
        pass

    def clone_to_item(self):
        pass

    def tace_usage_item(self):
        pass

    def add_standard_test_item(self):
        pass

    def _append_children(self):
        pass

    def _get_tooltip(self):
        return ''

    def _get_menu_items(self):
        return []

    def _get_children_names(self):
        return []

    def set_children_hidden(self, hide: bool):
        self._is_hidden = hide
        if hide:
            self._hide_children()
        else:
            self._show_children()

    def _hide_children(self):
        for index in range(self.rowCount()):
            self.hidden_children.append(self.takeChild(index))

        while self.rowCount():
            self.removeRow(0)

        self.setFlags(QtCore.Qt.NoItemFlags)

    def _show_children(self):
        for index, item in enumerate(self.hidden_children):
            self.insertRow(index, item)

        self.hidden_children = []
        self.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

    def has_children(self):
        return self.rowCount() > 0

    def is_hidden(self):
        return self._is_hidden

    def get_child(self, name):
        for index in range(self.rowCount()):
            item = self.child(index)
            if item.text() == name:
                return item

        return None

    def remove_child(self, name):
        child_item = self.get_child(name)
        self.removeRow(child_item.row())
