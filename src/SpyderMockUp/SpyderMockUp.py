'''
Created on Nov 18, 2019

@author: hoeren (horen.tom@micronas.com)


https://www.google.com

file://./documentation/STDF_V4.pdf

'''
show_workspace = False

import importlib
import os
import re
import shutil
import sys

from PyQt5 import QtCore, QtGui, QtWidgets, uic

import qdarkstyle
import qtawesome as qta

from ATE.org.navigation import project_navigator
from ATE.org.validation import is_ATE_project
from SCT.utils.finders import SCT_finder

import ATE.org.actions_on.flow.UIElements.QualiFlowItem
import ATE.org.actions_on.flow.UIElements.TreeItemWithData

homedir = os.path.expanduser("~")
workspace_path = os.path.join(homedir, "__spyder_workspace__")

if not os.path.exists(workspace_path):
    os.mkdir(workspace_path)

class screenCast(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()
    rightClicked = QtCore.pyqtSignal()

    def __init(self, parent):
        super().__init__(parent)

    def mousePressEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            self.rightClicked.emit()
        else:
            self.clicked.emit()

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, app):
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
        #self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle(' '.join(re.findall('.[^A-Z]*', os.path.basename(__file__).replace('.py', ''))))

    # Check if OpenCV is available (without loading it !)
        spec = importlib.util.find_spec('cv2')
        self.open_cv_available = spec is not None

    # setup initial paths
        self.workspace_path = workspace_path
        if not os.path.exists(self.workspace_path):
            os.makedirs(self.workspace_path)

        self.tester_finder = SCT_finder()
        self.tester_list = self.tester_finder.list_testers()
        self.active_tester = self.tester_list[0] # start with the first in the list
        print("active_tester =", self.active_tester)

        self.active_project = ''
        self.active_project_path = ''
        self.project_info = None # the project navigator
        self.active_hardware = ''

    # connect the File/New/Project menu
        self.action_quit.triggered.connect(self.quit_event)
        self.action_new_project_2.triggered.connect(self.new_project)
        self.action_open_project.triggered.connect(self.open_project)

    # setup the project explorer
        self.tree.clear()
        self.tree.setHeaderHidden(True)
        self.tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.context_menu_manager)
        self.tree.itemDoubleClicked.connect(self.edit_test)

    # setup the screencaster
        self.screencast = screenCast()
        self.screencast.setPixmap(qta.icon('mdi.video', color='orange').pixmap(16,16))
        self.screencast_state = 'idle'
        self.screencast.clicked.connect(self.screencast_start_stop)
        self.screencast.rightClicked.connect(self.screencast_settings)

        self.statusBar().addPermanentWidget(self.screencast)

    # setup the toolbar
        self.toolbar = self.create_toolbar() # sets active_tester, active_project, hwr (and base if necessary)
        self.update_toolbar()
        self.update_testers()

    # TODO: not needed after refactoring .ui file
        self.editorTabs.clear()
        self.editorTabs.addTab(QtWidgets.QTextEdit(), 'Tab')
        self.editorTabs.setTabsClosable(True)
        self.editorTabs.tabCloseRequested.connect(self.close_tab)

        self.load_last_project()
        self.show()

    def load_last_project(self):
        if os.path.exists(".lastproject"):
            f = open(".lastproject", "r")
            last_project = f.read()
            self.open_project_impl(last_project)

    def quit_event(self, status):
        #TODO: implement correctly (not as below)
        # if isinstance(status, int):
        #     sys.exit(status)
        # else:
        #     sys.exit()
        pass
    
    # def closeEvent(self, event=None):
    #     self.close()

    def create_toolbar(self):
        '''
        This method will create the toolbar (once, like etention of __init__)
        '''
        toolbar = self.addToolBar('toolbar')
        toolbar.setMovable(False)

        tester_label = QtWidgets.QLabel("Tester:")
        tester_label.setStyleSheet("background-color: rgba(0,0,0,0%)")
        toolbar.addWidget(tester_label)

        self.tester_combo = QtWidgets.QComboBox()
        self.tester_combo.clear()
        toolbar.addWidget(self.tester_combo)

        refreshTesters = QtWidgets.QAction(qta.icon('mdi.refresh', color='orange'), "Refresh Testers", self)
        refreshTesters.setStatusTip("Refresh the tester list")
        refreshTesters.triggered.connect(self.update_testers)
        refreshTesters.setCheckable(False)
        toolbar.addAction(refreshTesters)

        run_action = QtWidgets.QAction(qta.icon('mdi.play-circle-outline', color='orange'), "Run", self)
        run_action.setStatusTip("Run active module")
        run_action.triggered.connect(self.onRun)
        run_action.setCheckable(False)
        toolbar.addAction(run_action)

        hw_label = QtWidgets.QLabel("Hardware:")
        hw_label.setStyleSheet("background-color: rgba(0,0,0,0%)")
        toolbar.addWidget(hw_label)

        self.hw_combo = QtWidgets.QComboBox()
        self.hw_combo.blockSignals(True)
        self.hw_combo.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.hw_combo.currentTextChanged.connect(self.hardwareChanged)
        self.hw_combo.clear()
        self.hw_combo.setEnabled(False)
        self.hw_combo.blockSignals(False)
        
        toolbar.addWidget(self.hw_combo)

        base_label = QtWidgets.QLabel("Base:")
        base_label.setStyleSheet("background-color: rgba(0,0,0,0%)")
        toolbar.addWidget(base_label)

        self.base_combo = QtWidgets.QComboBox()
        self.base_combo.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.base_combo.blockSignals(True)
        self.base_combo.clear()
        self.base_combo.addItems(['', 'PR', 'FT'])
        self.base_combo.setCurrentIndex(0)        
        self.base_combo.currentIndexChanged.connect(self.baseChanged)
        self.base_combo.setEnabled(False)
        self.base_combo.blockSignals(False)
        toolbar.addWidget(self.base_combo)

        self.target_label = QtWidgets.QLabel("Target:")
        self.target_label.setStyleSheet("background-color: rgba(0,0,0,0%)")
        toolbar.addWidget(self.target_label)
        
        self.target_combo = QtWidgets.QComboBox()
        self.target_combo.blockSignals(True)
        self.target_combo.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.target_combo.currentIndexChanged.connect(self.targetChanged)
        self.target_combo.setEnabled(False)
        self.target_combo.clear()
        self.target_combo.blockSignals(False)
        toolbar.addWidget(self.target_combo)


        info_action = QtWidgets.QAction(qta.icon('mdi.information-outline', color='orange'), "Information", self)
        info_action.setStatusTip("print current information")
        info_action.triggered.connect(self.printInfo)
        info_action.setCheckable(False)
        toolbar.addAction(info_action)

        settings_action = QtWidgets.QAction(qta.icon('mdi.wrench', color='orange'), "Settings", self)
        settings_action.setStatusTip("Settings")
        settings_action.triggered.connect(self.onSettings)
        settings_action.setCheckable(False)
        toolbar.addAction(settings_action)

        return toolbar

    def update_testers(self):
        new_tester_list = list(self.tester_finder.list_testers())
        old_tester_list = [self.tester_combo.itemText(i) for i in range(self.tester_combo.count())]
        if set(new_tester_list) != set(old_tester_list):
            self.tester_combo.blockSignals(True)
            self.tester_combo.clear()
            self.tester_combo.addItems(new_tester_list)
            if self.active_tester in new_tester_list:
                self.tester_combo.setCurrentIndex(self.tester_list.index(self.active_tester))
            else:
                self.tester_combo.setCurrentIndex(0)
            self.active_tester = self.tester_combo.currentText()
            self.tester_combo.blockSignals(False)

    # def update_projects(self):
        
    #     all_projects = self.ALL_project_finder.list_Spyder_projects()
    #     ATE_projects = self.ATE_project_finder.list_ATE_projects()
    #     old_projects = [self.project_combo.itemText(i) for i in range(self.project_combo.count())]

    #     if len(ATE_projects) == 0:
    #         ATE_projects.append('')
    #         all_projects.append('')
    #         self.active_project = ''

    #     if self.active_project not in ATE_projects:
    #         self.active_project = ATE_projects[0]

    #     # if set(all_projects) != set(old_projects):
    #     #     self.project_combo.blockSignals(True)
    #     #     self.project_combo.clear()
    #     #     for index, project in enumerate(all_projects):
    #     #         self.project_combo.addItem(project)
    #     #         if project not in ATE_projects:
    #     #             self.project_combo.model().item(index).setEnabled(False)
    #     #         if project == self.active_project:
    #     #             self.project_combo.setCurrentIndex(index)
    #     #     self.project_combo.blockSignals(False)

    #     self.active_project_path = os.path.join(self.workspace_path, self.active_project)
    #     self.update_hardware()

    def update_menu(self):
        if self.active_project == None: # no active project
            self.active_project_path = None
        else: # we have an active project
            self.active_project_path = os.path.join(self.workspace_path, self.active_project)

    def update_hardware(self):
        '''
        This mentod will update the hardware list in the toolbar's combo box
        '''
        if self.active_project != '':
            hw_list = self.project_info.get_hardwares()
            old_hw_list = [self.hw_combo.itemText(i) for i in range(self.hw_combo.count())]

            if len(hw_list) == 0:
                hw_list.append('')
                self.active_hardware = ''

            if self.active_hardware not in hw_list:
                self.active_hardware = hw_list[0]

            if set(hw_list) != set(old_hw_list):
                self.hw_combo.blockSignals(True)
                self.hw_combo.clear()
                for index, hw in enumerate(hw_list):
                    self.hw_combo.addItem(str(hw))
                    if hw == self.active_hardware:
                        self.hw_combo.setCurrentIndex(index)
                self.hw_combo.blockSignals(False)


        # if self.active_project != '':
        #     hw_list = self.project_info.get_hardwares()
        #     old_hw_list = [self.hw_combo.itemText(i) for i in range(self.hw_combo.count())]

        #     if len(hw_list) == 0:
        #         hw_list.append('')
        #         self.active_hardware = ''

        #     if self.active_hardware not in hw_list:
        #         self.active_hardware = hw_list[0]

        #     if set(hw_list) != set(old_hw_list):
        #         self.hw_combo.blockSignals(True)
        #         self.hw_combo.clear()
        #         for index, hw in enumerate(hw_list):
        #             self.hw_combo.addItem(str(hw))
        #             if hw == self.active_hardware:
        #                 self.hw_combo.setCurrentIndex(index)
        #         self.hw_combo.blockSignals(False)

    def update_base(self):
        if self.project_info is None:
            self.base_combo.blockSignals(True)
            self.base_combo.setEnabled(False)
            self.base_combo.setCurrentIndex(0) #empty string
            self.base_combo.blockSignals(False)
            return

        if self.hw_combo.isEnabled():
            self.base_combo.setEnabled(True)
            if self.base_combo.currentText() == 'FT':
                self.target_label.setText('Product:')
            elif self.base_combo.currentText() == 'PR':
                self.target_label.setText('Die:')
            else:
                self.target_label.setText('Target:')
        else:
            self.base_combo.setEnabled(False)
    
    def update_target(self):
        if self.project_info is None:
            self.target_label.setText('Targets:')
            self.target_combo.blockSignals(True)
            self.target_combo.clear()
            self.target_combo.setEnabled(False)            
            return

        saved_target = self.target_combo.currentText()
        if self.base_combo.isEnabled():
            if self.target_label.text() == 'FT':
                targets = [''] 
                targets += self.project_info.get_products_for_hardware(self.active_hardware)
            elif self.target_label.text() == 'PR':
                targets = [''] 
                targets += self.project_info.get_dies_for_hardware(self.active_hardware)
            else: 
                targets = [''] 
                targets += self.project_info.get_dies_for_hardware(self.active_hardware)
                targets += self.project_info.get_products_for_hardware(self.active_hardware)
            self.target_combo.blockSignals(True)
            self.target_combo.clear()
            self.target_combo.addItems(targets)
            if saved_target in targets:
                self.target_combo.setCurrentIndex(self.target_combo.findText(saved_target))
            else:
                self.target_combo.setCurrentIndex(0)
            self.target_combo.setEnabled(True)
            self.target_combo.blockSignals(False)
        else:
            self.target_combo.blockSignals(True)
            self.target_combo.clear()
            self.target_combo.setEnabled(False)
            self.target_combo.blockSignals(False)

    def update_toolbar(self):
        '''
        This method will update the toolbar.
        '''
        self.update_hardware()
        self.update_base()
        self.update_target()

    def set_tree(self):
        if self.project_info is None:
            return

        self.tree.setHeaderHidden(True)

        self.project = QtWidgets.QTreeWidgetItem(self.tree)
        self.project.setText(0, self.active_project)
        self.project.setText(1, 'project')
        self.project.setText(2, 'project')
        font = self.project.font(0)
        font.setWeight(QtGui.QFont.Bold)
        self.project.setFont(0, font)
        self.project.setForeground(0, QtGui.QBrush(QtGui.QColor("#FFFF00")))

        # documentation
        self.documentation = QtWidgets.QTreeWidgetItem(self.project)
        self.documentation.setText(0, 'documentation')
        self.documentation.setText(1, 'documentation')
        doc_root = os.path.join(self.active_project_path, 'doc')

        self.standards_documentation = QtWidgets.QTreeWidgetItem(self.documentation, None)
        self.standards_documentation.setText(0, 'standards')
        self.standards_documentation.setText(1, 'standards_dir')

        tmp = os.listdir(os.path.join(doc_root, 'standards'))
        std_docs = [f for f in tmp if os.path.isfile(os.path.join(doc_root, 'standards', f))]
        previous = None
        for doc_name in std_docs:
            doc =  QtWidgets.QTreeWidgetItem(self.standards_documentation, previous)
            doc.setText(0, doc_name)
            doc.setText(1, 'standards_doc')
            previous = doc

        #TODO: doc structure should follow the directory structure

        # sources
        self.sources = QtWidgets.QTreeWidgetItem(self.project, self.documentation)
        self.sources.setText(0, 'sources')
        self.sources.setText(1, 'sources')

        # sources/definitions
        self.definitions = QtWidgets.QTreeWidgetItem(self.sources)
        self.definitions.setText(0, 'definitions')
        self.definitions.setText(1, 'definitions')

        self.hardwaresetups = None
        self.masksets = None
        self.dies = None
        self.packages = None
        self.devices = None
        self.products = None

        def set_tree_element(element, node, sub_node, node_elements, is_disabled):
            element = QtWidgets.QTreeWidgetItem()
            element.setText(0, node)
            element.setText(1, node)
            self.definitions.insertChild(0, element)
            element.setDisabled(is_disabled)
            previous = None
            if len(node_elements) == 0:
                return True

            for name in node_elements:
                sub_element = QtWidgets.QTreeWidgetItem(element, previous)
                sub_element.setText(0, str(name))
                sub_element.setText(1, sub_node)
                previous = sub_element

            return False

        is_disabled = False
        # sources/definitions/hardwaresetup
        is_disabled = set_tree_element(self.hardwaresetups, 'hardwaresetups', 'hardwaresetup', self.project_info.get_hardwares(), is_disabled)
        # sources/definitions/masksets
        is_disabled = set_tree_element(self.masksets, 'masksets', 'maskset', self.project_info.get_masksets(), is_disabled)
        # sources/definitions/dies
        is_disabled = set_tree_element(self.dies, 'dies', 'die', self.project_info.get_dies(), is_disabled)
        # sources/definitions/packages
        is_disabled = set_tree_element(self.packages, 'packages', 'package', self.project_info.packages_get(), is_disabled)
        # sources/definitions/devices
        is_disabled = set_tree_element(self.devices, 'devices', 'device', self.project_info.get_devices(), is_disabled)
        # sources/definitions/products
        is_disabled = set_tree_element(self.products, 'products', 'product', self.project_info.get_products(), is_disabled)

        # sources/registermaps
        self.registermaps = QtWidgets.QTreeWidgetItem(self.sources, self.definitions)
        self.registermaps.setText(0, 'register maps')
        self.registermaps.setText(1, 'registermaps')
        #TODO: cycle through the directory and add the registermaps

        # souces/protocols
        self.protocols = QtWidgets.QTreeWidgetItem(self.sources, self.registermaps)
        self.protocols.setText(0, 'protocols')
        self.protocols.setText(1, 'protocols')
        #TODO: cycle through the directory and add the protocols

        # sources/patterns
        self.patterns = QtWidgets.QTreeWidgetItem(self.sources, self.protocols)
        self.patterns.setText(0, 'patterns')
        self.patterns.setText(1, 'patterns')
        #TODO: insert the appropriate patterns from /sources/patterns, based on HWR and Base

        # sources/states
        self.states = QtWidgets.QTreeWidgetItem(self.sources, self.patterns)
        self.states.setText(0, 'states')
        self.states.setText(1, 'states')
        # #TODO: cycle through the states and add the states

        # sources/flows
        self.flows = QtWidgets.QTreeWidgetItem(self.sources, self.states)
        self.flows.setText(0, 'flows')
        self.flows.setText(1, 'flows')
        self.flows.setDisabled(True)
        self.set_flow_state(self.flows)
        self.flows.setChildIndicatorPolicy(QtWidgets.QTreeWidgetItem.DontShowIndicator)

        # sources/tests
        self.tests = QtWidgets.QTreeWidgetItem(self.sources, self.flows)
        self.tests.setText(0, 'tests')
        self.tests.setText(1, 'tests')
        self.tests.setDisabled(True)
        self.tests.setChildIndicatorPolicy(QtWidgets.QTreeWidgetItem.DontShowIndicator)

    def update_tree(self):
        '''
        this method will update the 'project explorer'
        '''
        current_item = None
        if self.tree.currentItem() is None:
            return
        
        if self.project_info is None:
            return

        current_item = self.tree.currentItem()
        get_info_from_type = {"hardwaresetups": self.project_info.get_hardwares(),
                              "masksets": self.project_info.get_masksets(),
                              "dies": self.project_info.get_dies(),
        					  "packages": self.project_info.packages_get(),
                              "devices": self.project_info.get_devices(),
                              "products": self.project_info.get_products()}

        sub_type = {"hardwaresetups": "hardwaresetup",
                    "masksets": "maskset",
                    "dies": "die",
                    "packages": "package",
                    "devices": "device",
                    "products": "product"}

        changed_type = current_item.text(1)
        if changed_type in get_info_from_type:
            elem_list = get_info_from_type[changed_type]
            if current_item.childCount() == len(elem_list):
                # in this case, we do not need to update, no change occurres
                return

            current_item.takeChildren()

            for name in elem_list:
                child = QtWidgets.QTreeWidgetItem()
                child.setText(0, name)
                child.setText(1, sub_type[changed_type])
                current_item.insertChild(current_item.childCount(), child)
                self.tree.itemAbove(current_item).setDisabled(False)

    def context_menu_manager(self, point):
        #https://riverbankcomputing.com/pipermail/pyqt/2009-April/022668.html
        #https://doc.qt.io/qt-5/qtreewidget-members.html
        #https://www.qtcentre.org/threads/18929-QTreeWidgetItem-have-contextMenu
        #https://cdn.materialdesignicons.com/4.9.95/

        index = self.tree.indexAt(point)

        if not index.isValid():
            return

        item = self.tree.itemAt(point)
        if item.isDisabled():
            return

        self.node_name = item.text(0)
        self.node_type = item.text(1)
        self.node_data = item.text(2)

        print("name = '%s' type = '%s', data = '%s'" % (self.node_name, self.node_type, self.node_data))

        if self.node_type == 'project':
            menu = QtWidgets.QMenu(self)
            audit = menu.addAction(qta.icon("mdi.incognito", color='orange') ,"audit")
            audit.triggered.connect(self.placeholder)
            pack = menu.addAction(qta.icon("mdi.gift-outline", color='orange'), "pack")
            menu.exec_(QtGui.QCursor.pos())
        elif self.node_type == 'docs_root' :
            menu = QtWidgets.QMenu(self)
            new_folder = menu.addAction(qta.icon("mdi.folder-plus-outline", color='orange'), "New Folder")
            new_folder.triggered.connect(self.new_folder)
            rename_folder = menu.addAction(qta.icon("mdi.folder-edit-outline", color='orange'), "Rename Folder")
            import_document = menu.addAction(qta.icon("mdi.folder-download-outline", color='orange'), "Import Document")
            menu.exec_(QtGui.QCursor.pos())
        elif self.node_type == 'docs':
            menu = QtWidgets.QMenu(self)
            new_folder = menu.addAction(qta.icon("mdi.folder-plus-outline", color='orange'), "New Folder")
            rename_folder = menu.addAction(qta.icon("mdi.folder-edit-outline", color='orange'), "Rename Folder")
            import_document = menu.addAction(qta.icon("mdi.folder-download-outline", color='orange'), "Import Document")
            menu.addSeparator()
            delete_folder = menu.addAction(qta.icon("mdi.folder-remove-outline", color='orange'), "Delete Folder")
            menu.exec_(QtGui.QCursor.pos())
        elif self.node_type == 'doc':
            menu = QtWidgets.QMenu(self)
            open_file = menu.addAction(qta.icon("mdi.file-edit-outline", color='orange'), "Open")
            rename_file = menu.addAction(qta.icon("mdi.lead-pencil", color='orange'), "Rename")
            menu.addSeparator()
            delete_file = menu.addAction(qta.icon("mdi.eraser", color='orange'), "Delete")
            menu.exec_(QtGui.QCursor.pos())
        elif self.node_type == 'hardwaresetups':
            menu = QtWidgets.QMenu(self)
            new_hardwaresetup = menu.addAction(qta.icon('mdi.plus', color='orange'), "Add")
            new_hardwaresetup.triggered.connect(self.new_hardwaresetup)
            menu.exec_(QtGui.QCursor.pos())
        elif self.node_type == 'hardwaresetup':
            menu = QtWidgets.QMenu(self)
            activate_hardwaresetup = menu.addAction(qta.icon('mdi.check', color='orange'), "Activate")
            activate_hardwaresetup.triggered.connect(self.activate_hardwaresetup)
            show_hardwaresetup = menu.addAction(qta.icon('mdi.eye-outline', color='orange'), "View")
            show_hardwaresetup.triggered.connect(self.display_hardwaresetup)
            edit_hardwaresetup = menu.addAction(qta.icon('mdi.lead-pencil', color='orange'), "Edit")
            edit_hardwaresetup.triggered.connect(self.edit_hardwaresetup)
            delete_hardwaresetup = menu.addAction(qta.icon('mdi.minus', color='orange'), "Delete")
            menu.exec_(QtGui.QCursor.pos())
        elif self.node_type == 'masksets':
            menu = QtWidgets.QMenu(self)
            add_maskset = menu.addAction(qta.icon('mdi.plus', color='orange'), "Add")
            add_maskset.triggered.connect(self.new_maskset)
            menu.exec_(QtGui.QCursor.pos())
        elif self.node_type == 'maskset':
            menu = QtWidgets.QMenu(self)
            view_maskset = menu.addAction(qta.icon('mdi.eye-outline', color='orange'), "View")
            view_maskset.triggered.connect(self.display_maskset)
            edit_maskset = menu.addAction(qta.icon('mdi.lead-pencil', color='orange'), "Edit")
            edit_maskset.triggered.connect(self.edit_maskset)
            delete_maskset = menu.addAction(qta.icon('mdi.minus', color='orange'), "Delete")
            # delete_maskset.triggered.connect
            menu.exec_(QtGui.QCursor.pos())
        elif self.node_type == 'dies':
            menu = QtWidgets.QMenu(self)
            add_die = menu.addAction(qta.icon('mdi.plus', color='orange'), "Add")
            add_die.triggered.connect(self.new_die)
            menu.exec_(QtGui.QCursor.pos())
        elif self.node_type == 'die':
            menu = QtWidgets.QMenu(self)
            edit_die = menu.addAction(qta.icon('mdi.lead-pencil', color='orange'), "Edit")
            # edit_die.triggered.connect
            delete_die = menu.addAction(qta.icon('mdi.minus', color='orange'), "Delete")
            # delete_die.triggered.connect
            menu.exec_(QtGui.QCursor.pos())
        elif self.node_type == 'packages':
            menu = QtWidgets.QMenu(self)
            add_package = menu.addAction(qta.icon('mdi.plus', color='orange'), "Add")
            add_package.triggered.connect(self.new_package)
            menu.exec_(QtGui.QCursor.pos())
        elif self.node_type == 'package':
            menu = QtWidgets.QMenu(self)
            edit_package = menu.addAction(qta.icon('mdi.lead-pencil', color='orange'), "Edit")
            # edit_package.triggered.connect
            delete_package = menu.addAction(qta.icon('mdi.minus', color='orange'), "Delete")
            # delete_package.triggered.connect
            menu.exec_(QtGui.QCursor.pos())
        elif self.node_type == 'patterns':
            menu = QtWidgets.QMenu(self)
            add_pattern = menu.addAction(qta.icon('mdi.plus', color='orange'), "Add")
            #add_pattern.triggered.connect ...
            import_pattern = menu.addAction(qta.icon('mdi.application-import', color='orange'), "Import")
            #import_pattern.triggered.connect ...
            menu.exec_(QtGui.QCursor.pos())
        elif self.node_type == 'pattern':
            menu = QtWidgets.QMenu(self)
            edit_pattern = menu.addAction(qta.icon('mdi.lead-pencil', color='orange'), "Edit")      
            # edit_pattern.triggered.connect ...
            delete_pattern = menu.addAction(qta.icon('mdi.minus', color='orange'), "Delete")
            # delete_pattern.triggered.connect ...
            menu.exec_(QtGui.QCursor.pos())
        elif self.node_type == 'protocols':
            menu = QtWidgets.QMenu(self)
            add_protocol = menu.addAction(qta.icon('mdi.plus', color='orange'), "Add")      
            # add_protocol.triggered.connect ...
            menu.exec_(QtGui.QCursor.pos())        
        elif self.node_type == 'protocol':
            menu = QtWidgets.QMenu(self)
            edit_protocol = menu.addAction(qta.icon('mdi.lead-pencil', color='orange'), "Edit")      
            # edit_protocol.triggered.connect ...
            delete_protocol = menu.addAction(qta.icon('mdi.minus', color='orange'), "Delete")
            # delete_protocol.triggered.connect ...
            menu.exec_(QtGui.QCursor.pos())
        elif self.node_type == 'devices':
            menu = QtWidgets.QMenu(self)
            add_device = menu.addAction(qta.icon('mdi.plus', color='orange'), "Add")
            add_device.triggered.connect(self.new_device)
            menu.exec_(QtGui.QCursor.pos())
            #TODO: update the base filter to 'FT' if needed !

        elif self.node_type == 'device':
            menu = QtWidgets.QMenu(self)
            edit_device = menu.addAction(qta.icon('mdi.lead-pencil', color='orange'), "Edit")
            # edit_device.triggered.connect
            delete_device = menu.addAction(qta.icon('mdi.minus', color='orange'), "Delete")
            # delete_device.triggered.connect
            menu.exec_(QtGui.QCursor.pos())
        elif self.node_type == 'products':
            menu = QtWidgets.QMenu(self)
            add_product = menu.addAction(qta.icon('mdi.plus', color='orange'), "Add")
            add_product.triggered.connect(self.new_product)
            menu.exec_(QtGui.QCursor.pos())
        elif self.node_type == 'product':
            menu = QtWidgets.QMenu(self)
            edit_product = menu.addAction(qta.icon('mdi.lead-pencil', color='orange'), "Edit")
            # edit_product.triggered.connect
            delete_product = menu.addAction(qta.icon('mdi.minus', color='orange'), "Delete")
            # delete_product.triggered.connect
            menu.exec_(QtGui.QCursor.pos())
        elif self.node_type == 'flows':
            menu = QtWidgets.QMenu(self)
            add_flow = menu.addAction(qta.icon('mdi.plus', color='orange'), "Add")
            # add_flow.triggered.connect
            menu.exec_(QtGui.QCursor.pos())
        elif self.node_type == 'flow':
            menu = QtWidgets.QMenu(self)
            edit_flow = menu.addAction(qta.icon('mdi.lead-pencil', color='orange'), "Edit")
            # edit_flow.triggered.connect
            delete_flow = menu.addAction(qta.icon('mdi.minus', color='orange'), "Delete")
            # delete_flow.triggered.connect
            menu.exec_(QtGui.QCursor.pos())
        elif self.node_type == 'production_flow':
            menu = QtWidgets.QMenu(self)
            add_program = menu.addAction(qta.icon('mdi.plus', color='orange'), "Add")
            add_program.triggered.connect(self.new_testprogram)
            menu.exec_(QtGui.QCursor.pos())

        elif self.node_type == 'registermaps':
            menu = QtWidgets.QMenu(self)
            add_registermap = menu.addAction(qta.icon('mdi.plus', color='orange'), "Add")
            #add_registermap.triggered.connect
            import_registermap = menu.addAction(qta.icon('mdi.application-import', color='orange'), "Import")
            # import_registermap.triggered.connect
            menu.exec_(QtGui.QCursor.pos())
        elif self.node_type == 'registermap':
            menu = QtWidgets.QMenu(self)
            edit_registermap = menu.addAction(qta.icon('mdi.lead-pencil', color='orange'), "Edit")
            # edit_registermap.triggered.connect
            delete_registermap = menu.addAction(qta.icon('mdi.minus', color='orange'), "Delete")
            # delete_registermap.triggered.connect
            menu.exec_(QtGui.QCursor.pos())
        elif self.node_type == 'states':
            menu = QtWidgets.QMenu(self)
            add_state = menu.addAction(qta.icon('mdi.plus', color='orange'), "Add")
            #add_state.triggered.connect
            menu.exec_(QtGui.QCursor.pos())
        elif self.node_type == 'state':
            menu = QtWidgets.QMenu(self)
            view_state = menu.addAction(qta.icon('mdi.eye-outline', color='orange'), "View")
            # view_state.triggered.connect
            edit_state = menu.addAction(qta.icon('mdi.lead-pencil', color='orange'), "Edit")
            # edit_state.triggered.connect
            delete_state = menu.addAction(qta.icon('mdi.minus', color='orange'), "Delete")
            # delete_state.triggered.connect
            menu.exec_(QtGui.QCursor.pos())
        elif self.node_type == 'tests':
            menu = QtWidgets.QMenu(self)
            add_test = menu.addAction(qta.icon('mdi.plus', color='orange'), "Add Test")
            add_test.triggered.connect(self.add_test)
            add_standard_test = menu.addAction(qta.icon('mdi.plus-box-outline', color='orange'), "Add Standard Test")
            add_standard_test.triggered.connect(self.add_standard_test)
            clone_from_test = menu.addAction(qta.icon('mdi.application-import', color='orange'), "Clone from ...")
            clone_from_test.triggered.connect(self.clone_from_test)
            menu.exec_(QtGui.QCursor.pos())
        elif self.node_type == 'test':
            menu = QtWidgets.QMenu(self)
            edit_test = menu.addAction(qta.icon('mdi.lead-pencil', color='orange'), "Edit")
            edit_test.triggered.connect(self.edit_test)
            clone_to_test = menu.addAction(qta.icon('mdi.application-export', color='orange'), "Clone to ...")
            # clone_to_test.triggered.connect
            trace_test = menu.addAction(qta.icon('mdi.share-variant', color='orange'), "Trace usage")
            # trace_test.triggered.connect
            delete_test = menu.addAction(qta.icon('mdi.minus', color='orange'), "Delete")
            # delete_test.triggered.connect
            menu.exec_(QtGui.QCursor.pos())

        elif isinstance(item, ATE.org.actions_on.flow.UIElements.QualiFlowItem.MultiInstanceQualiFlowItem):
            item.exec_context_menu(self, self.project_info, self.target_combo.currentText())
            self.update_flow_state()
        elif isinstance(item, ATE.org.actions_on.flow.UIElements.QualiFlowItem.SingleInstanceQualiFlowItem):
            item.exec_context_menu(self, self.project_info, self.target_combo.currentText())
        elif isinstance(item, ATE.org.actions_on.flow.UIElements.TreeItemWithData.TreeItemWithData):
            item.exec_context_menu(self, self.project_info)
        elif isinstance(item, ATE.org.actions_on.flow.UIElements.QualiFlowItem.SimpleFlowItem):
            item.exec_context_menu(self, self.project_info, self.target_combo.currentText())


    def testerChanged(self):
        self.active_tester = self.tester_combo.currentText()

    def hardwareChanged(self):
        self.active_hardware = self.hw_combo.currentText()
        self.update_base()
        self.update_target()
        self.update_tests()
        self.update_tree()

    def update_tests(self):
        if self.base_combo.currentText() == '':
            self.tests.setDisabled(True)
            self.tests.setChildIndicatorPolicy(QtWidgets.QTreeWidgetItem.DontShowIndicator)
            return

        self.tests.setDisabled(False)
        self.tests.setChildIndicatorPolicy(QtWidgets.QTreeWidgetItem.ShowIndicator)

        test_list = self._get_available_tests()
        if len(test_list) == 0:
            self.tests.setChildIndicatorPolicy(QtWidgets.QTreeWidgetItem.DontShowIndicator)

        self.tests.takeChildren()
        for test_entry in test_list:
            test = QtWidgets.QTreeWidgetItem()
            test.setText(0, test_entry)
            test.setText(1, 'test')
            self.tests.insertChild(self.tests.childCount(), test)

    def _get_available_tests(self):
        from os import walk, path

        self.tests_directory = path.join(self.workspace_path, self.active_project, 'src',
                                    'tests', self.active_hardware, self.base_combo.currentText())

        files = []
        for _, _, filenames in walk(self.tests_directory):
            files.extend([path.splitext(x)[0] for x in filenames if not x == '__init__.py'])
            break

        return files

    def set_flow_state(self, parent):
        # sources/flows/production
        self.production_flow = self.make_simple_flow(parent, None, "production", "production_flow")

        self.production_flow.setFlags(QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled)

        # HALT vs HASS --> https://www.intertek.com/performance-testing/halt-and-hass/
        # sources/flows/qualification
        self.qualification_flows = QtWidgets.QTreeWidgetItem(parent, self.production_flow)
        self.qualification_flows.setText(0, 'qualification')
        self.qualification_flows.setText(1, 'qualification_flows')

        # sources/flows/qualification/ZHM
        self.qualification_ZHM_flows = self.make_simple_flow(self.qualification_flows, None, "ZHM", "Zero Hour Measurements")

        # sources/flows/qualification/HTOL
        self.qualification_HTOL_flows = self.make_multi_instance_quali_flow(self.qualification_ZHM_flows, "ATE.org.actions_on.flow.HTOL.htolwizard")

        # sources/flows/qualification/HAST
        self.qualification_HAST_flows = self.make_single_instance_quali_flow(self.qualification_HTOL_flows, "ATE.org.actions_on.flow.HAST.hastwizard")

        # sources/flows/qualification/ESD
        self.qualification_ESD_flows = QtWidgets.QTreeWidgetItem(self.qualification_flows, self.qualification_HAST_flows)
        self.qualification_ESD_flows.setToolTip(0, 'Electro Static Discharge')
        self.qualification_ESD_flows.setText(0, 'ESD')
        self.qualification_ESD_flows.setText(1, 'qualification_ESD_flows')

        # sources/flows/qualification/HTSL
        self.qualification_HTSL_flows = self.make_multi_instance_quali_flow(self.qualification_ESD_flows, "ATE.org.actions_on.flow.HTSL.htslwizard")

        # sources/flows/qualification/DR
        self.qualification_DR_flows = self.make_multi_instance_quali_flow(self.qualification_HTSL_flows, "ATE.org.actions_on.flow.DR.drwizard")

        # sources/flows/qualification/EC
        self.qualification_EC_flows = QtWidgets.QTreeWidgetItem(self.qualification_flows, self.qualification_DR_flows)
        self.qualification_EC_flows.setToolTip(0, 'Endurance Cycling')
        self.qualification_EC_flows.setText(0, 'EC')
        self.qualification_EC_flows.setText(1, 'qualification_EC_flows')

        # sources/flows/qualification/ABSMAX
        self.qualification_ABSMAX_flows = QtWidgets.QTreeWidgetItem(self.qualification_flows, self.qualification_EC_flows)
        self.qualification_ABSMAX_flows.setToolTip(0, 'Absolute Maximum Ratings')
        self.qualification_ABSMAX_flows.setText(0, 'ABSMAX')
        self.qualification_ABSMAX_flows.setText(1, 'qualification_ABSMAX_flows')

        # sources/flows/qualification/XRAY
        self.qualification_XRAY_flows = QtWidgets.QTreeWidgetItem(self.qualification_flows, self.qualification_ABSMAX_flows)
        # self.qualification_XRAY_flows.setToolTip(0, 'X-Ray')
        self.qualification_XRAY_flows.setText(0, 'XRAY')
        self.qualification_XRAY_flows.setText(1, 'qualification_XRAY_flows')

        # sources/flows/qualification/LI
        self.qualification_LI_flows = QtWidgets.QTreeWidgetItem(self.qualification_flows, self.qualification_XRAY_flows)
        self.qualification_LI_flows.setToolTip(0, 'Lead Integrity')
        self.qualification_LI_flows.setText(0, 'LI')
        self.qualification_LI_flows.setText(1, 'qualification_LI_flows')

        # sources/flows/qualification/ELFR
        self.qualification_ELFR_flows = self.make_single_instance_quali_flow(self.qualification_LI_flows, "ATE.org.actions_on.flow.ELFR.elfrwizard")

        # sources/flows/qualification/RSH
        self.qualification_RSH_flows = self.make_multi_instance_quali_flow(self.qualification_ELFR_flows, "ATE.org.actions_on.flow.RSH.rshwizard")

        # sources/flows/qualification/SA
        self.qualification_SA_flows = QtWidgets.QTreeWidgetItem(self.qualification_flows, self.qualification_RSH_flows)
        self.qualification_SA_flows.setToolTip(0, 'SolderAbility')
        self.qualification_SA_flows.setText(0, 'SA')
        self.qualification_SA_flows.setText(1, 'qualification_SA_flows')

        # sources/flows/qualification/LU
        self.qualification_LU_flows = self.make_single_instance_quali_flow(self.qualification_SA_flows, "ATE.org.actions_on.flow.LU.luwizard")

        # sources/flows/qualification/AC
        self.qualification_AC_flows = self.make_multi_instance_quali_flow(self.qualification_LU_flows, "ATE.org.actions_on.flow.AC.acwizard")

        # sources/flows/qualification/TC
        self.qualification_TC_flows = self.make_single_instance_quali_flow(self.qualification_AC_flows, "ATE.org.actions_on.flow.TC.tcwizard")
        
        # sources/flows/qualification/THB
        self.qualification_THB_flows = self.make_single_instance_quali_flow(self.qualification_TC_flows, "ATE.org.actions_on.flow.THB.thbwizard")

        # sources/flows/characterisation
        self.characterisation_flows = self.make_simple_flow(parent, self.qualification_flows, "characterisation", "characterisation_flow")

        # sources/flows/validation
        self.validation_flow = self.make_simple_flow(parent, self.characterisation_flows, "validation", "validation_flow")

        # sources/flows/engineering
        self.engineering_flow = self.make_simple_flow(parent, self.validation_flow, "engineering", "engineering_flow")


    def update_flow_state(self):
        if self.target_combo.currentText() == '':
            self.flows.setDisabled(True)
            self.flows.setChildIndicatorPolicy(QtWidgets.QTreeWidgetItem.DontShowIndicator)
            return

        self.flows.setDisabled(False)
        self.flows.setChildIndicatorPolicy(QtWidgets.QTreeWidgetItem.ShowIndicator)

        self.populateQualificationFlow(self.qualification_HTOL_flows, "ATE.org.actions_on.flow.HTOL.htolwizard")
        self.populateQualificationFlow(self.qualification_HTSL_flows, "ATE.org.actions_on.flow.HTSL.htslwizard")
        self.populateQualificationFlow(self.qualification_AC_flows, "ATE.org.actions_on.flow.AC.acwizard")
        self.populateQualificationFlow(self.qualification_DR_flows, "ATE.org.actions_on.flow.DR.drwizard")
        


    def populateQualificationFlow(self, item: QtWidgets.QWidget, moduleName: str):
        item.takeChildren()
        for subflow in self.project_info.get_data_for_qualification_flow(item.text(1), self.target_combo.currentText()):
            flows = ATE.org.actions_on.flow.UIElements.TreeItemWithData.TreeItemWithData(item, moduleName, self.delete_qualification_flow_instance)
            flows.setText(0, subflow[0])
            flows.setText(1, f"{item.text(1)}_instance")
            flows.set_item_data(subflow)

    def make_single_instance_quali_flow(self, firstsibling: QtWidgets.QTreeWidgetItem, modulename: str):
        return ATE.org.actions_on.flow.UIElements.QualiFlowItem.SingleInstanceQualiFlowItem(self.qualification_flows, firstsibling, modulename)

    def make_multi_instance_quali_flow(self, firstsibling: QtWidgets.QTreeWidgetItem, modulename: str):
        return ATE.org.actions_on.flow.UIElements.QualiFlowItem.MultiInstanceQualiFlowItem(self.qualification_flows, firstsibling, modulename)

    def make_simple_flow(self, parent, firstsibling: QtWidgets.QTreeWidgetItem, name: str, tooltip):
        return ATE.org.actions_on.flow.UIElements.QualiFlowItem.SimpleFlowItem(parent, firstsibling, name, tooltip)


    def baseChanged(self):
        self.update_target()
        self.update_flow_state()
        self.update_tests()

    def targetChanged(self):
        self.update_flow_state()
        self.update_tests()

    def active_project_changed(self):
        self.active_project = self.comboBox.currentText()
        self.active_project_path = os.path.join(self.workspace_path, self.active_project)
        self.setWindowTitle("Spyder MockUp (%s)" % self.active_project_path)

    def workspace_setup(self):
        self.workspace_path = workspace_path
        if not os.path.exists(self.workspace_path):
            os.makedirs(self.workspace_path)
        for project in self.list_projects_in_workspace():
            print(project)

    # def list_projects_in_workspace(self):
    #     retval = []
    #     for possible_project_dir in os.listdir(self.workspace_path):
    #         if os.path.isdir(possible_project_dir):
    #             retval.append(possible_project_dir)
    #             #TODO: look in the directories
    #     return retval

    def get_tree_state(self):
        '''
        this method will traverse the tree, and record the state (isExpanded)
        for each item, and saves it.
        
        --> need to work model based !!!
        '''
        state = {}
        it = QtWidgets.QTreeWidgetItemIterator(self.tree)
        while it.value():
            itemIndex = self.tree.indexFromItem(it.value(), 0)
            itemState = self.tree.isExpanded(itemIndex)
            state.update({itemIndex: itemState})
            it += 1
        return state
    
    def set_tree_state(self, state):
        '''
        this method will apply the supplied state to the tree (setExpanded)
        if a state can not be applied (item gone), it will be ignored.
        
        --> need to work model based !!!
        '''
        it = QtWidgets.QTreeWidgetItemIterator(self.tree)
        while it.value():
            toExpand = [i for i in state if i == self.tree.indexFromItem(it.value(),0)]
            shouldExpand = state.get(toExpand[0])
            if shouldExpand:
                if not self.tree.isItemExpanded(it.value()):
                    self.tree.expandItem(it.value())
            it += 1

    def add_test(self):
        from ATE.org.actions_on.tests.NewTestWizard import new_test_dialog
        new_test_dialog(self)
        self.update_tests()

    def add_standard_test(self):
        from ATE.org.actions_on.tests.NewStandardTestWizard import new_standard_test_dialog
        new_standard_test_dialog(self)
        self.update_tests()
    
    def clone_from_test(self):
        pass
        
        


    def new_testprogram(self):
        from ATE.org.actions_on.program.NewProgramWizard import new_program_dialog
        new_program_dialog(self)
        self.update_tree()

    def new_product(self):
        from ATE.org.actions_on.product.NewProductWizard import new_product_dialog
        new_product_dialog(self)
        self.update_tree()

    def new_device(self):
        from ATE.org.actions_on.device.NewDeviceWizard import new_device_dialog
        new_device_dialog(self)
        self.update_tree()

    def new_package(self):
        from ATE.org.actions_on.package.NewPackageWizard import new_package_dialog
        new_package_dialog(self)
        self.update_tree()

    def new_die(self):
        from ATE.org.actions_on.die.NewDieWizard import new_die_dialog
        new_die_dialog(self)
        self.update_tree()

    def new_maskset(self):
        from ATE.org.actions_on.maskset.NewMasksetWizard import new_maskset_dialog
        new_maskset_dialog(self.project_info)
        self.update_tree()

    def new_hardwaresetup(self):
        from ATE.org.actions_on.hardwaresetup.NewHardwaresetupWizard import new_hardwaresetup_dialog
        new_hardwaresetup_dialog(self.project_info)
        self.active_hardware = self.project_info.get_latest_hardware_name()
        self.update_hardware()
        self.update_tree()

    def new_flow(self):
        print("new_flow")

    def new_protocol(self):
        print("new_protocol")

    def new_registermap(self):
        print("new_registermap")

    def new_project(self):
        from ATE.org.actions_on.project.NewProjectWizard import new_project_dialog
        new_project_dialog(self)
        self.tree.clear()

        self.project_info = project_navigator(self.active_project_path)
        self.project_info.create_project_structure()
        self.project_info.create_sql_connection()
        self.project_info.create_project_database()

        self.set_tree()

    def delete_qualification_flow_instance(self, data: dict):
        self.project_info.delete_qualifiaction_flow_instance(data)
        self.update_flow_state()

    def open_project(self):
        selected_directory = os.path.normpath(
            str(QtWidgets.QFileDialog.getExistingDirectory(self, 
                                                           "Select Directory",
                                                           workspace_path,
                                                           QtWidgets.QFileDialog.ShowDirsOnly
                                                           | QtWidgets.QFileDialog.DontResolveSymlinks)
                )
            )
        self.open_project_impl(selected_directory)
    
    def open_project_impl(self, projectpath):
        if is_ATE_project(projectpath):      
            # Store this as the last project
            f= open(".lastproject","w")
            f.write(projectpath)
            f.close()
            self.tree.clear()
            self.active_project_path = projectpath
            self.active_project = os.path.split(self.active_project_path)[-1]            
            self.project_info = project_navigator(self, self.active_project_path)

            if not os.path.exists(self.project_info.db_file):
                self.create_project_database()

            available_hardwares =  self.project_info.get_hardwares()
            print(f"{available_hardwares}")
            available_hardwares.sort()
            print(f"{available_hardwares}")
            if len(available_hardwares) > 0:
                self.active_hardware = available_hardwares[-1]
                
                self.hw_combo.blockSignals(True)
                self.hw_combo.clear()
                self.hw_combo.addItems(available_hardwares)
                self.hw_combo.setCurrentIndex(len(available_hardwares)-1)
                self.hw_combo.setEnabled(True)
                self.hw_combo.blockSignals(False)
                
                
                self.base_combo.setCurrentIndex(0) # = nothing selected
                self.base_combo.setEnabled(True)
                
                targets = [''] 
                targets += self.project_info.get_dies_for_hardware(self.active_hardware)
                targets += self.project_info.get_products_for_hardware(self.active_hardware)
                self.target_combo.blockSignals(True)
                self.target_combo.clear()
                self.target_combo.addItems(targets)
                self.target_combo.setCurrentIndex(0) # = nothing
                self.target_combo.setEnabled(True)
                self.target_combo.blockSignals(False)
            else:
                self.active_hardware = ''

            self.update_hardware()

            # set tree once and use "update_tree" function to update if needed
            self.set_tree()


    def clone_test(self):
        print("clone_test")

    def clone_testprogram(self):
        print("clone_testprogram")

    def clone_flow(self):
        print("clone_flow")

    def clone_protocol(self):
        print("clone_protocol")

    def clone_registermap(self):
        print("clone_registermap")

    def clone_product(self):
        print("clone_product")

    def clone_device(self):
        print("clone_device")

    def clone_package(self):
        print("clone_package")

    def clone_die(self):
        print("clone_die")

    def clone_maskset(self):
        print("clone_maskset")



    def import_registermap(self):
        print("import_registermap")

    def import_product(self):
        print("import_product")

    def import_package(self):
        print("import_package")

    def import_maskset(self):
        print("import_maskset")



    def edit_testprogram(self):
        print("edit_testprogram")

    def edit_flow(self):
        print("edit_flow")

    def edit_protocol(self):
        print("edit_protocol")

    def edit_registermap(self):
        print("edit_registermap")

    def edit_product(self):
        print("edit_product")

    def edit_device(self):
        print("edit_device")

    def edit_package(self):
        print("edit_package")

    def edit_die(self):
        print("edit_die")


    def rename_test(self):
        print("rename_test")

    def rename_maskset(self):
        print("rename_maskset")

    def rename_device(self):
        print("rename_device")

    def rename_die(self):
        print("rename_die")

    def rename_product(self):
        print("rename_product")

    def rename_package(self):
        print("rename_package")



    def display_tests(self):
        print("display_tests")

    def display_testprograms(self):
        print("display_testprograms")

    def display_flows(self):
        print("display_flows")

    def display_protocols(self):
        print("display_protocols")

    def display_registermaps(self):
        print("display_registermaps")

    def display_products(self):
        print("display_products")

    def display_devices(self):
        print("display_devices")

    def display_packages(self):
        print("display_packages")

    def display_dies(self):
        print("display_dies")


    def delete_test(self):
        print("delete_test")

    def delete_testprogram(self):
        print("delete_testprogram")

    def delete_flow(self):
        print("delete_flow")

    def delete_protocol(self):
        print("delete_protocol")

    def delete_registermap(self):
        print("delete_registermap")

    def delete_product(self):
        print("delete_product")

    def delete_device(self):
        print("delete_device")

    def delete_package(self):
        print("delete_package")

    def delete_die(self):
        print("delete_die")

    def delete_hardwaresetup(self):
        print("delete_hardwaresetup")

    def delete_project(self):
        print("delete_project", end='')
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        directory_to_delete = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory", workspace_path, options=options))
        print(" : %s" % directory_to_delete, end='')
        shutil.rmtree(directory_to_delete)
        print(" Done.")


    def onRun(self):
        print("run")

    def onSettings(self):
        print("settings")
        print(f"\tself.tree.Width = {self.tree.width()}")
        print(f"\tself.editorTabs.Width = {self.editorTabs.width()}")
        print(f"\tself.infoTabs.Width = {self.infoTabs.width()}")

    def screencast_settings(self):
        print("start screencast settings")
        from ScreenCastSettings import ScreenCastSettings
        screenCastSettings = ScreenCastSettings(self)
        screenCastSettings.exec_()
        del(screenCastSettings)
        print("end screencast settings")

    def screencast_start_stop(self):
        if self.screencast_state == 'recording':

            print("recording stopped")
            self.screencast_state = 'idle'
            self.screencast.setPixmap(qta.icon('mdi.video', color='orange').pixmap(16,16))
        else:

            print("recording started")
            self.screencast_state = 'recording'
            self.screencast.setPixmap(qta.icon('mdi.video', 'fa5s.ban', options=[{'color' : 'orange'},{'color' : 'red'}]).pixmap(16,16))

    def printInfo(self):
        print("info")

    def placeholder(self, event):
        print(type(event))
        print(event)

    def activate_hardwaresetup(self):
        available_hardwares =  self.project_info.get_hardwares()
        index = available_hardwares.index(self.tree.currentItem().text(0))
        self.hw_combo.setCurrentIndex(index)

    def edit_hardwaresetup(self):
        from ATE.org.actions_on.hardwaresetup.EditHardwaresetupWizard import edit_hardwaresetup_dialog

        hw_name = self.tree.currentItem().text(0)
        edit_hardwaresetup_dialog(self.project_info, hw_name)

    def display_hardwaresetup(self):
        from ATE.org.actions_on.hardwaresetup.ViewHardwaresetupSettings import display_hardware_settings_dialog

        hw_name = self.tree.currentItem().text(0)
        configuration = self.project_info.get_hardware_definition(hw_name)
        display_hardware_settings_dialog(configuration, hw_name)

    def edit_maskset(self):
        from ATE.org.actions_on.maskset.EditMasksetWizard import edit_maskset_dialog

        maskset_name = self.tree.currentItem().text(0)
        edit_maskset_dialog(self.project_info, maskset_name)

    def display_maskset(self):
        from ATE.org.actions_on.maskset.ViewMasksetSettings import display_maskset_settings_dialog

        maskset_name = self.tree.currentItem().text(0)
        configuration = self.project_info.get_maskset_definition(maskset_name)
        display_maskset_settings_dialog(configuration, maskset_name)

    def delete_maskset(self):
        self.project_info.delete_hardwaresetup()
		
    def edit_test(self, item=None):
        if isinstance(item, QtWidgets.QTreeWidgetItem):
            if not item.text(1) == 'test':
                return

        tabs = self.editorTabs.count()

        if self.editorTabs.tabText(0) == 'Tab':
            self.editorTabs.removeTab(0)

        selected_file = self.tree.currentItem().text(0)
        for index in range(tabs):
            if selected_file == self.editorTabs.tabText(index):
                self.editorTabs.setCurrentIndex(index)
                return

        file_path = os.path.join(self.tests_directory, selected_file + '.py')
        with open(file_path) as f:
            content = f.read()

        text_editor = QtWidgets.QTextEdit('')
        text_editor.insertPlainText(content)
        self.editorTabs.addTab(text_editor, selected_file)
        self.editorTabs.setCurrentIndex(self.editorTabs.count() - 1)

    def close_tab(self, tab_index):
        self.editorTabs.removeTab(tab_index)

        if self.editorTabs.count() == 0:
            text_editor = QtWidgets.QTextEdit('')
            self.editorTabs.addTab(text_editor, 'Tab')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window = MainWindow(app)
    window.show()
    sys.exit(app.exec_())

