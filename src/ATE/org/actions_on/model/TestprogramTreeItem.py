from PyQt5 import QtCore, QtGui, QtWidgets, uic
import qtawesome as qta

# ToDo, SPYD11: Fix this to conform with model based tree!
class TestprogramTreeItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent, implmodule, delfunc):
        super(QtWidgets.QTreeWidgetItem, self).__init__(parent, None)

    def exec_context_menu(self, window, project_info):
        menu = QtWidgets.QMenu(window)
        edit_flow = menu.addAction(qta.icon('mdi.lead-pencil', color='orange'), "Edit")
        #edit_flow.triggered.connect(lambda: self.editfunc(project_info, self.get_item_data()[3]))

        view_flow = menu.addAction(qta.icon('mdi.eye-outline', color='orange'), "View")
        #view_flow.triggered.connect(lambda: self.viewfunc(project_info, self.get_item_data()[3]))

        delete_flow = menu.addAction(qta.icon('mdi.minus', color='orange'), "Delete")
        #delete_flow.triggered.connect(lambda: self.deletefunc(self.get_item_data()[3]))

        menu.exec_(QtGui.QCursor.pos())
