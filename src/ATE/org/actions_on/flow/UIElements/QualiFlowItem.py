from PyQt5 import QtCore, QtGui, QtWidgets, uic
import qtawesome as qta


class QualiFlowItemBase(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent, firstsibling, implmodule):
        super(QtWidgets.QTreeWidgetItem, self).__init__(parent, firstsibling)
        import importlib
        mod = importlib.import_module(implmodule)
        self.setToolTip(0, getattr(mod, "quali_flow_tooltip"))
        self.setText(0, getattr(mod, "quali_flow_listentry_name"))
        self.setText(1, getattr(mod, "quali_flow_name"))

        if isinstance(self, MultiInstanceQualiFlowItem):
            self.newfunc = getattr(mod, "new_item")
        if isinstance(self, SingleInstanceQualiFlowItem):
            self.editfunc = getattr(mod, "edit_item")


class SimpleFlowItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent, firstsibling, name, tooltip):
        super(QtWidgets.QTreeWidgetItem, self).__init__(parent, firstsibling)
        self.setToolTip(0, tooltip)
        self.setText(0, name)

    def exec_context_menu(self, window, project_info, product):
        menu = QtWidgets.QMenu(window)
        from ATE.org.actions_on.program.NewProgramWizard import new_program_dialog
        add_test_prog = menu.addAction(qta.icon('mdi.plus', color='orange'), "Add Testprogram")
        add_test_prog.triggered.connect(lambda: new_program_dialog(self))
        menu.exec_(QtGui.QCursor.pos())


class SingleInstanceQualiFlowItem(QualiFlowItemBase):

    def exec_context_menu(self, window, project_info, product):
        menu = QtWidgets.QMenu(window)
        add_flow = menu.addAction(qta.icon('mdi.lead-pencil', color='orange'), "Edit")
        add_flow.triggered.connect(lambda: self.editfunc(project_info, product))

        from ATE.org.actions_on.program.NewProgramWizard import new_program_dialog
        add_test_prog = menu.addAction(qta.icon('mdi.plus', color='orange'), "Add Testprogram")
        add_test_prog.triggered.connect(lambda: new_program_dialog(self))
        
        menu.exec_(QtGui.QCursor.pos())


class MultiInstanceQualiFlowItem(QualiFlowItemBase):
    def exec_context_menu(self, window, project_info, product):
        menu = QtWidgets.QMenu(window)
        add_flow = menu.addAction(qta.icon('mdi.plus', color='orange'), "Add")
        add_flow.triggered.connect(lambda: self.newfunc(project_info, product))
        menu.exec_(QtGui.QCursor.pos())
