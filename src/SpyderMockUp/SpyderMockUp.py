# -*- coding: utf-8 -*-
"""
Created on Nov 18, 2019

@author: hoeren (horen.tom@micronas.com)

References:
    - file://./documentation/STDF_V4.pdf

"""

import importlib
import os
import platform
import re
import sys

from PyQt5 import QtCore, QtWidgets, uic, QtGui

import qdarkstyle
import qtawesome as qta

from ATE.org.navigation import ProjectNavigation
from ATE.org.validation import is_ATE_project
from ScreenCasting.QtScreenCast import ScreenCastToolButton

show_workspace = False


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, app=None):
        super().__init__()
        self.app = app

        self.flow_is_set = False
    # get the appropriate .ui file and load it.
        my_ui = __file__.replace('.py', '.ui')
        if not os.path.exists(my_ui):
            raise Exception("'%s' doesn't exist" % my_ui)
        uic.loadUi(my_ui, self)

    # Initialize the main window
        # ToDo: Reenable this, if we figure that we *really* want SpyderMock to be in front of our debugger
        # all the time.
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle(' '.join(re.findall('.[^A-Z]*', os.path.basename(__file__).replace('.py', ''))))

    # Check if OpenCV is available (without loading it !)
        spec = importlib.util.find_spec('cv2')
        self.open_cv_available = spec is not None

    # setup initial paths
        self.homedir = os.path.expanduser("~")
        self.workspace_path = os.path.join(self.homedir, "__spyder_workspace__")
        if not os.path.exists(self.workspace_path):
            os.makedirs(self.workspace_path)
        self.project_info = ProjectNavigation('', self.workspace_path, self)

    # connect the File/New/Project menu
        self.action_quit.triggered.connect(self.quit_event)
        self.action_new_project_2.triggered.connect(self.new_project)
        self.action_open_project.triggered.connect(self.open_project)

    # setup the project explorer
        self.tree.setHeaderHidden(True)
        self.tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.context_menu_manager)

    # setup the screencaster
        self.screencast = ScreenCastToolButton(self)
        self.statusBar().addPermanentWidget(self.screencast)

    # setup the toolbar
        from ATE.org.toolbar import ToolBar
        self.toolbar = ToolBar(None, self)
        self.addToolBar(self.toolbar)

    # TODO: not needed after refactoring .ui file
        self.editorTabs.clear()
        self.editorTabs.addTab(QtWidgets.QTextEdit(), 'Tab')
        self.editorTabs.setTabsClosable(True)
        self.editorTabs.tabCloseRequested.connect(self.close_tab)

        self.load_last_project()

    def context_menu_manager(self, point):
        # https://riverbankcomputing.com/pipermail/pyqt/2009-April/022668.html
        # https://doc.qt.io/qt-5/qtreewidget-members.html
        # https://www.qtcentre.org/threads/18929-QTreeWidgetItem-have-contextMenu
        # https://cdn.materialdesignicons.com/4.9.95/
        indexes = self.tree.selectedIndexes()
        if indexes is None:
            return

        model_index = self.tree.indexAt(point)
        item = self.model.itemFromIndex(model_index)
        if item is None:
            return

        item.exec_context_menu()

    def load_last_project(self):
        if os.path.exists(".lastproject"):
            f = open(".lastproject", "r")
            last_project = f.read()
            self.open_project_impl(last_project)

    def quit_event(self, status):
        # TODO: implement correctly (not as below)
        # if isinstance(status, int):
        #     sys.exit(status)
        # else:
        #     sys.exit()
        pass

    def set_tree(self):
        from ATE.org.actions_on.model.TreeModel import TreeModel
        self.model = TreeModel(self.project_info, parent=self)
        self.model.edit_file.connect(self.edit_test)
        self.model.delete_file.connect(self.delete_test)
        self.tree.setModel(self.model)
        self.tree.doubleClicked.connect(self.item_double_clicked)

    def new_project(self):
        from ATE.org.actions_on.project.ProjectWizard import NewProjectDialog

        new_project_name, new_project_quality = NewProjectDialog(self, self.project_info)
        if not new_project_name:
            return

        self.toolbar(self.project_info)
        self.set_tree()

        with open(".lastproject", "w") as f:
            f.write(os.path.join(self.project_info.workspace_path, new_project_name))

    def open_project(self):
        dir_name = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                              "Select Directory",
                                                              self.workspace_path,
                                                              QtWidgets.QFileDialog.ShowDirsOnly | QtWidgets.QFileDialog.DontResolveSymlinks)
        selected_directory = os.path.normpath(dir_name)
        self.open_project_impl(selected_directory)

    def open_project_impl(self, projectpath):
        if is_ATE_project(projectpath):
            # Store this as the last project
            with open(".lastproject", "w") as f:
                f.write(projectpath)

            self.active_project_path = projectpath
            self.project_info = ProjectNavigation(self.active_project_path, self.workspace_path, self)
            self.active_project = os.path.split(self.active_project_path)[-1]
            self.toolbar(self.project_info)

            self.set_tree()

    def screencast_settings(self):
        pass

    def screencast_start_stop(self):
        if self.screencast_state == 'recording':

            print("recording stopped")
            self.screencast_state = 'idle'
        else:

            print("recording started")
            self.screencast_state = 'recording'

    def edit_test(self, path):
        selected_file = os.path.basename(path)
        index = self._get_tab_index(selected_file)
        if not index == -1:
            self.editorTabs.setCurrentIndex(index)
            return

        with open(path) as f:
            content = f.read()

        text_editor = QtWidgets.QTextEdit('')
        text_editor.setFontFamily('Courier')
        text_editor.setFontPointSize(8)
        text_editor.insertPlainText(content)
        self.editorTabs.addTab(text_editor, selected_file)
        self.editorTabs.setCurrentIndex(self.editorTabs.count() - 1)

    def close_tab(self, tab_index):
        self.editorTabs.removeTab(tab_index)

        if self.editorTabs.count() == 0:
            text_editor = QtWidgets.QTextEdit('')
            self.editorTabs.addTab(text_editor, 'Tab')

    def delete_test(self, path):
        selected_file = os.path.basename(path)
        index = self._get_tab_index(selected_file)
        if index == -1:
            return

        self.close_tab(index)

    def _get_tab_index(self, selected_file):
        tabs = self.editorTabs.count()

        if self.editorTabs.tabText(0) == 'Tab':
            self.editorTabs.removeTab(0)

        for index in range(tabs):
            if selected_file == self.editorTabs.tabText(index):
                return index

        return -1

    def item_double_clicked(self, index):
        try:
            item = self.tree.selectedIndexes()[0]
        except Exception:
            return

        model_item = item.model().itemFromIndex(index)
        from ATE.org.actions_on.tests.TestItem import TestItemChild
        if isinstance(model_item, TestItemChild):
            self.edit_test(model_item.path)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window = MainWindow(app)
    window.show()
    res = app.exec_()
    # TODO: there have to be another way to do this mybe move this inside the tree model itself, ?
    if hasattr(window, 'model'):
        window.model.doc_observer.stop_observer()

    sys.exit(res)
