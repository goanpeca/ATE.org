from PyQt5 import QtCore, QtGui, QtWidgets, uic
import qtawesome as qta


class TreeItemWithData(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent, implmodule, delfunc):
        super(QtWidgets.QTreeWidgetItem, self).__init__(parent, None)
        import importlib
        mod = importlib.import_module(implmodule)
        self.viewfunc = getattr(mod, "view_item")
        self.editfunc = getattr(mod, "edit_item")
        self.deletefunc = delfunc

    def set_item_data(self, data):
        self.data = data
    
    def get_item_data(self):
        return self.data

    def exec_context_menu(self, window, project_info):
        menu = QtWidgets.QMenu(window)
        edit_flow = menu.addAction(qta.icon('mdi.lead-pencil', color='orange'), "Edit")
        edit_flow.triggered.connect(lambda: self.editfunc(project_info, self.get_item_data()[3]))

        view_flow = menu.addAction(qta.icon('mdi.eye-outline', color='orange'), "View")
        view_flow.triggered.connect(lambda: self.viewfunc(project_info, self.get_item_data()[3]))

        delete_flow = menu.addAction(qta.icon('mdi.minus', color='orange'), "Delete")
        delete_flow.triggered.connect(lambda: self.deletefunc(self.get_item_data()[3]))

        from ATE.org.actions_on.program.NewProgramWizard import new_program_dialog
        add_test_prog = menu.addAction(qta.icon('mdi.plus', color='orange'), "Add Testprogram")
        add_test_prog.triggered.connect(lambda: new_program_dialog(self))
        

        menu.exec_(QtGui.QCursor.pos())
