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

    # get the appropriate .ui file and load it.
        my_ui = __file__.replace('.py', '.ui')
        if not os.path.exists(my_ui):
            raise Exception("'%s' doesn't exist" % my_ui)
        uic.loadUi(my_ui, self)

    # Initialize the main window
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
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
        self.active_hw = ''

    # connect the File/New/Project menu
        self.action_quit.triggered.connect(self.quit_event)
        self.action_new_project_2.triggered.connect(self.new_project)
        self.action_open_project.triggered.connect(self.open_project)

    # setup the project explorer
        self.tree.clear()
        self.tree.setHeaderHidden(True)
        self.tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.context_menu_manager)

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

        self.show()

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
                self.active_hw = ''

            if self.active_hw not in hw_list:
                self.active_hw = hw_list[0]

            if set(hw_list) != set(old_hw_list):
                self.hw_combo.blockSignals(True)
                self.hw_combo.clear()
                for index, hw in enumerate(hw_list):
                    self.hw_combo.addItem(str(hw))
                    if hw == self.active_hw:
                        self.hw_combo.setCurrentIndex(index)
                self.hw_combo.blockSignals(False)


        # if self.active_project != '':
        #     hw_list = self.project_info.get_hardwares()
        #     old_hw_list = [self.hw_combo.itemText(i) for i in range(self.hw_combo.count())]

        #     if len(hw_list) == 0:
        #         hw_list.append('')
        #         self.active_hw = ''

        #     if self.active_hw not in hw_list:
        #         self.active_hw = hw_list[0]

        #     if set(hw_list) != set(old_hw_list):
        #         self.hw_combo.blockSignals(True)
        #         self.hw_combo.clear()
        #         for index, hw in enumerate(hw_list):
        #             self.hw_combo.addItem(str(hw))
        #             if hw == self.active_hw:
        #                 self.hw_combo.setCurrentIndex(index)
        #         self.hw_combo.blockSignals(False)

    def update_base(self):
        if self.project_info == None:
            self.base_combo.blockSignals(True)
            self.base_combo.setEnabled(False)
            self.base_combo.setCurrentIndex(0) #empty string
            self.base_combo.blockSignals(False)
        else:            
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
        if self.project_info == None:
            self.target_label.setText('Targets:')
            self.target_combo.blockSignals(True)
            self.target_combo.clear()
            self.target_combo.setEnabled(False)            
        else:
            saved_target = self.target_combo.currentText()
            if self.base_combo.isEnabled():
                if self.target_label.text() == 'FT':
                    targets = [''] 
                    targets += self.project_info.get_products_for_hardware(self.active_hw)
                elif self.target_label.text() == 'PR':
                    targets = [''] 
                    targets += self.project_info.get_dies_for_hardware(self.active_hw)
                else: 
                    targets = [''] 
                    targets += self.project_info.get_dies_for_hardware(self.active_hw)
                    targets += self.project_info.get_products_for_hardware(self.active_hw)
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
        if self.project_info != None:
            self.tree.clear()
            self.tree.setHeaderHidden(True)

            project = QtWidgets.QTreeWidgetItem(self.tree)
            project.setText(0, self.active_project)
            project.setText(1, 'project')
            project.setText(2, 'project')
            font = project.font(0)
            font.setWeight(QtGui.QFont.Bold)
            project.setFont(0, font)
            project.setForeground(0, QtGui.QBrush(QtGui.QColor("#FFFF00")))

        # documentation
            documentation = QtWidgets.QTreeWidgetItem(project)
            documentation.setText(0, 'documentation')
            documentation.setText(1, 'documentation')
            doc_root = os.path.join(self.active_project_path, 'doc')

            standards_documentation = QtWidgets.QTreeWidgetItem(documentation, None)
            standards_documentation.setText(0, 'standards')
            standards_documentation.setText(1, 'standards_dir')

            tmp = os.listdir(os.path.join(doc_root, 'standards'))
            print(tmp)
            std_docs = [f for f in tmp if os.path.isfile(os.path.join(doc_root, 'standards', f))]
            previous = None
            for doc_name in std_docs:
                doc =  QtWidgets.QTreeWidgetItem(standards_documentation, previous)
                doc.setText(0, doc_name)
                doc.setText(1, 'standards_doc')
                previous = doc

            #TODO: doc structure should follow the directory structure

        # sources
            sources = QtWidgets.QTreeWidgetItem(project, documentation)
            sources.setText(0, 'sources')
            sources.setText(1, 'sources')

        # sources/definitions
            definitions = QtWidgets.QTreeWidgetItem(sources)
            definitions.setText(0, 'definitions')
            definitions.setText(1, 'definitions')

        # sources/definitions/products
            products = QtWidgets.QTreeWidgetItem(definitions, None)
            products.setText(0, 'products')
            products.setText(1, 'products')
            previous = None
            for product_name in self.project_info.get_products():
                product = QtWidgets.QTreeWidgetItem(products, previous)
                product.setText(0, product_name)
                print(product_name)
                product.setText(1, 'product')
                previous = product

        # sources/definitions/devices
            devices = QtWidgets.QTreeWidgetItem(definitions, products)
            devices.setText(0, 'devices')
            devices.setText(1, 'devices')
            previous = None
            for device_name in self.project_info.get_devices():
                device = QtWidgets.QTreeWidgetItem(devices, previous)
                device.setText(0, device_name)
                device.setText(1, 'device')
                previous = device

        # sources/definitions/packages
            packages = QtWidgets.QTreeWidgetItem(definitions, devices)
            packages.setText(0, 'packages')
            packages.setText(1, 'packages')
            previous = None
            for name in self.project_info.get_packages():
                package = QtWidgets.QTreeWidgetItem(packages, previous)
                package.setText(0, name)
                package.setText(1, 'package')
                previous = package

        # sources/definitions/dies
            dies = QtWidgets.QTreeWidgetItem(definitions, packages)
            dies.setText(0, 'dies')
            dies.setText(1, 'dies')
            previous = None
            for name in self.project_info.get_dies():
                die = QtWidgets.QTreeWidgetItem(dies, previous)
                die.setText(0, name)
                die.setText(1, 'die')
                previous = die

        # sources/definitions/masksets
            masksets = QtWidgets.QTreeWidgetItem(definitions, dies)
            masksets.setText(0, 'masksets')
            masksets.setText(1, 'masksets')
            previous = None
            for name in self.project_info.get_masksets():
                maskset = QtWidgets.QTreeWidgetItem(masksets, previous)
                maskset.setText(0, name)
                maskset.setText(1, 'maskset')
                previous = maskset

        # sources/definitions/hardware
            hardwaresetups = QtWidgets.QTreeWidgetItem(definitions, masksets)
            hardwaresetups.setText(0, 'hardwaresetups')
            hardwaresetups.setText(1, 'hardwaresetups')
            previous = None
            for name in self.project_info.get_hardwares():
                hardwaresetup = QtWidgets.QTreeWidgetItem(hardwaresetups, previous)
                hardwaresetup.setText(0, str(name))
                hardwaresetup.setText(1, 'hardwaresetup')
                previous = hardwaresetup

        # sources/registermaps
            registermaps = QtWidgets.QTreeWidgetItem(sources, definitions)
            registermaps.setText(0, 'register maps')
            registermaps.setText(1, 'registermaps')
            #TODO: cycle through the directory and add the registermaps

        # souces/protocols
            protocols = QtWidgets.QTreeWidgetItem(sources, registermaps)
            protocols.setText(0, 'protocols')
            protocols.setText(1, 'protocols')
            #TODO: cycle through the directory and add the protocols

        # sources/patterns
            patterns = QtWidgets.QTreeWidgetItem(sources, protocols)
            patterns.setText(0, 'patterns')
            patterns.setText(1, 'patterns')
            #TODO: insert the appropriate patterns from /sources/patterns, based on HWR and Base

        # sources/states
            states = QtWidgets.QTreeWidgetItem(sources, patterns)
            states.setText(0, 'states')
            states.setText(1, 'states')
            # #TODO: cycle through the states and add the states

        # sources/flows
            flows = QtWidgets.QTreeWidgetItem(sources, states)
            flows.setText(0, 'flows')
            flows.setText(1, 'flows')
            flows.setDisabled(True)

        # sources/tests
            tests = QtWidgets.QTreeWidgetItem(sources, flows)
            tests.setText(0, 'tests')
            tests.setText(1, 'tests')
            tests.setDisabled(True)

    def update_tree(self):
        '''
        this method will update the 'project explorer'
        '''
        current_item = None
        if not self.tree.currentItem() is None:
            current_item = self.tree.currentItem()

        if self.project_info is not None:
            get_info_from_type = {"hardwaresetups": self.project_info.get_hardwares(),
                                  "masksets": self.project_info.get_masksets(),
                                  "dies": self.project_info.get_masksets(),
                                  "packages": self.project_info.get_packages(),
                                  "devices": self.project_info.get_devices(),
                                  "products": self.project_info.get_products()}

            sub_type = {"hardwaresetups": "hardware",
                        "masksets": "maskset",
                        "dies": "die",
                        "packages": "package",
                        "devices": "device",
                        "products": "product"}

            changed = current_item
            changed_type = current_item.text(1)
            if changed_type not in get_info_from_type:
                return
            children= []
            for child in range(changed.childCount()):
                children.append(changed.child(child).text(0))

            diff = list(set(get_info_from_type[changed_type]) - set(children))
            for name in diff:
                child = QtWidgets.QTreeWidgetItem()
                child.setText(0, name)
                child.setText(1, sub_type[changed_type])
                changed.insertChild(changed.childCount(), child)
                return

    def context_menu_manager(self, point):
        #https://riverbankcomputing.com/pipermail/pyqt/2009-April/022668.html
        #https://doc.qt.io/qt-5/qtreewidget-members.html
        #https://www.qtcentre.org/threads/18929-QTreeWidgetItem-have-contextMenu
        #https://cdn.materialdesignicons.com/4.9.95/
        index = self.tree.indexAt(point)
        if not index.isValid():
            print("what the fuck")
            return
        item = self.tree.itemAt(point)
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
            #activate_hardwaresetup.triggered.connect
            show_hardwaresetup = menu.addAction(qta.icon('mdi.eye-outline', color='orange'), "View")
            edit_hardwaresetup = menu.addAction(qta.icon('mdi.lead-pencil', color='orange'), "Edit")
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
            # view_maskset.triggered.connect
            edit_maskset = menu.addAction(qta.icon('mdi.lead-pencil', color='orange'), "Edit")
            # edit_maskset.triggered.connect
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
            add_test = menu.addAction(qta.icon('mdi.plus', color='orange'), "Add")
            #add_test.triggered.connect
            clone_from_test = menu.addAction(qta.icon('mdi.application-import', color='orange'), "Clone from ...")
            menu.exec_(QtGui.QCursor.pos())
        elif self.node_type == 'test':
            menu = QtWidgets.QMenu(self)
            edit_test = menu.addAction(qta.icon('mdi.lead-pencil', color='orange'), "Edit")
            # edit_test.triggered.connect
            clone_to_test = menu.addAction(qta.icon('mdi.application-export', color='orange'), "Clone to ...")
            # clone_to_test.triggered.connect
            trace_test = menu.addAction(qta.icon('mdi.share-variant', color='orange'), "Trace usage")
            # trace_test.triggered.connect
            delete_test = menu.addAction(qta.icon('mdi.minus', color='orange'), "Delete")
            # delete_test.triggered.connect
            menu.exec_(QtGui.QCursor.pos())

    def testerChanged(self):
        self.active_tester = self.tester_combo.currentText()

    def hardwareChanged(self):
        self.active_hw = self.hw_combo.currentText()
        self.update_base()
        self.update_target()
        # self.update_tree()

    def update_tests(self):
        it = QtWidgets.QTreeWidgetItemIterator(self.tree)
        # nasty way to update flows
        while it.value():
            if it.value().text(1) == "tests":
                if self.base_combo.currentText() == '':
                    it.value().setDisabled(True)
                    # remove all children from node: "flows"
                    it.value().takeChildren()
                else: # build the sub-tree with self.base_combo
                    it.value().setDisabled(False)
                    test_list = self.project_info.get_tests_from_db(self.hw_combo.currentText(), 
                                                                    self.base_combo.currentText())
                    print(test_list)
                    for test_entry in test_list:
                        test = QtWidgets.QTreeWidgetItem()
                        test.setText(0, test_entry)
                        test.setText(1, 'test')
                        test.setText(2, test_list[test_entry])
                        it.value().insertChild(it.value().childCount(), test)
                    
                    it.value().sortChildren(0, QtCore.Qt.AscendingOrder)
                    return

            it += 1

    def update_flow_state(self):
        it = QtWidgets.QTreeWidgetItemIterator(self.tree)
        while it.value():
            if it.value().text(1) == "flows":
                # remove all children from node: "flows"
                it.value().takeChildren()
                if self.target_combo.currentText() == '':
                    it.value().setDisabled(True)
                else:
                    it.value().setDisabled(False)

            # sources/flows/production
                    flows = it.value()
                    production_flow = QtWidgets.QTreeWidgetItem(flows, None)
                    production_flow.setText(0, 'production')
                    production_flow.setText(1, 'production_flow')

                    production_flow.setFlags(QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled)

            # HALT vs HASS --> https://www.intertek.com/performance-testing/halt-and-hass/
            # sources/flows/qualification
                    qualification_flows = QtWidgets.QTreeWidgetItem(flows, production_flow)
                    qualification_flows.setText(0, 'qualification')
                    qualification_flows.setText(1, 'qualification_flows')

            # sources/flows/qualification/ZHM
                    qualification_ZHM_flows = QtWidgets.QTreeWidgetItem(qualification_flows, None)
                    qualification_ZHM_flows.setToolTip(0, 'Zero Hour Measurements')
                    qualification_ZHM_flows.setText(0, 'ZHM')
                    qualification_ZHM_flows.setText(1, 'qualification_ZHM_flows')

            # sources/flows/qualification/HTOL
                    qualification_HTOL_flows = QtWidgets.QTreeWidgetItem(qualification_flows, qualification_ZHM_flows)
                    qualification_HTOL_flows.setToolTip(0, 'High Temperature Operating Life')
                    qualification_HTOL_flows.setText(0, 'HTOL')
                    qualification_HTOL_flows.setText(1, 'qualification_HTOL_flow')

            # sources/flows/qualification/HAST
                    qualification_HAST_flows = QtWidgets.QTreeWidgetItem(qualification_flows, qualification_HTOL_flows)
                    qualification_HAST_flows.setToolTip(0, 'Highley Accelerated Stress Test')
                    qualification_HAST_flows.setText(0, 'HAST')
                    qualification_HAST_flows.setText(1, 'qualification_HAST_flows')
            # sources/flows/qualification/ESD
                    qualification_ESD_flows = QtWidgets.QTreeWidgetItem(qualification_flows, qualification_HAST_flows)
                    qualification_ESD_flows.setToolTip(0, 'Electro Static Discharge')
                    qualification_ESD_flows.setText(0, 'ESD')
                    qualification_ESD_flows.setText(1, 'qualification_ESD_flows')

            # sources/flows/qualification/HTSL
                    qualification_HTSL_flows = QtWidgets.QTreeWidgetItem(qualification_flows, qualification_ESD_flows)
                    qualification_HTSL_flows.setToolTip(0, 'High Temperature Storage Life')
                    qualification_HTSL_flows.setText(0, 'HTSL')
                    qualification_HTSL_flows.setText(1, 'qualification_HTSL_flows')

            # sources/flows/qualification/DR
                    qualification_DR_flows = QtWidgets.QTreeWidgetItem(qualification_flows, qualification_HTSL_flows)
                    qualification_DR_flows.setToolTip(0, 'Data Retention')
                    qualification_DR_flows.setText(0, 'DR')
                    qualification_DR_flows.setText(1, 'qualification_DR_flows')

            # sources/flows/qualification/EC
                    qualification_EC_flows = QtWidgets.QTreeWidgetItem(qualification_flows, qualification_DR_flows)
                    qualification_EC_flows.setToolTip(0, 'Endurance Cycling')
                    qualification_EC_flows.setText(0, 'EC')
                    qualification_EC_flows.setText(1, 'qualification_EC_flows')

            # sources/flows/qualification/ABSMAX
                    qualification_ABSMAX_flows = QtWidgets.QTreeWidgetItem(qualification_flows, qualification_EC_flows)
                    qualification_ABSMAX_flows.setToolTip(0, 'Absolute Maximum Ratings')
                    qualification_ABSMAX_flows.setText(0, 'ABSMAX')
                    qualification_ABSMAX_flows.setText(1, 'qualification_ABSMAX_flows')

            # sources/flows/qualification/XRAY
                    qualification_XRAY_flows = QtWidgets.QTreeWidgetItem(qualification_flows, qualification_ABSMAX_flows)
                    # qualification_XRAY_flows.setToolTip(0, 'X-Ray')
                    qualification_XRAY_flows.setText(0, 'XRAY')
                    qualification_XRAY_flows.setText(1, 'qualification_XRAY_flows')

            # sources/flows/qualification/LI
                    qualification_LI_flows = QtWidgets.QTreeWidgetItem(qualification_flows, qualification_XRAY_flows)
                    qualification_LI_flows.setToolTip(0, 'Lead Integrity')
                    qualification_LI_flows.setText(0, 'LI')
                    qualification_LI_flows.setText(1, 'qualification_LI_flows')

            # sources/flows/qualification/ELFR
                    qualification_ELFR_flows = QtWidgets.QTreeWidgetItem(qualification_flows, qualification_LI_flows)
                    qualification_ELFR_flows.setToolTip(0, 'Early Life Failure Rate (aka: BurnIn)')
                    qualification_ELFR_flows.setText(0, 'ELFR')
                    qualification_ELFR_flows.setText(1, 'qualification_ELFR_flows')

            # sources/flows/qualification/RSH
                    qualification_RSH_flows = QtWidgets.QTreeWidgetItem(qualification_flows, qualification_ELFR_flows)
                    qualification_RSH_flows.setToolTip(0, 'Resistance to Solder Heat')
                    qualification_RSH_flows.setText(0, 'RSH')
                    qualification_RSH_flows.setText(1, 'qualification_RSH_flows')

            # sources/flows/qualification/SA
                    qualification_SA_flows = QtWidgets.QTreeWidgetItem(qualification_flows, qualification_RSH_flows)
                    qualification_SA_flows.setToolTip(0, 'SolderAbility')
                    qualification_SA_flows.setText(0, 'SA')
                    qualification_SA_flows.setText(1, 'qualification_SA_flows')

            # sources/flows/qualification/LU
                    qualification_LU_flows = QtWidgets.QTreeWidgetItem(qualification_flows, qualification_SA_flows)
                    qualification_LU_flows.setToolTip(0, 'Latch-up')
                    qualification_LU_flows.setText(0, 'LU')
                    qualification_LU_flows.setText(1, 'qualification_LU_flows')

            # sources/flows/characterisation
                    characterisation_flows = QtWidgets.QTreeWidgetItem(flows, qualification_flows)
                    characterisation_flows.setText(0, 'characterisation')
                    characterisation_flows.setText(1, 'characterisation_flow')

            # sources/flows/validation
                    validation_flow = QtWidgets.QTreeWidgetItem(flows, characterisation_flows)
                    validation_flow.setText(0, 'validation')
                    validation_flow.setText(1, 'validation_flow')

            # sources/flows/engineering
                    engineering_flow = QtWidgets.QTreeWidgetItem(flows, validation_flow)
                    engineering_flow.setText(0, 'engineering')
                    engineering_flow.setText(1, 'engineering_flow')             

                    flows.sortChildren(0, QtCore.Qt.AscendingOrder)
                    # stop iteration when done
                    return

            it += 1

    def baseChanged(self):
        self.update_target()
        self.update_flow_state()
        self.update_tests()
        # self.update_tree()

    def targetChanged(self):
        self.update_flow_state()
        self.update_tests()
        # self.update_tree()
        pass

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
            itemState = self.tree.isExpanded(it.value())
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

    def new_test(self):
        from ATE.org.actions.new.test.NewTestWizard import new_test_dialog
        new_test_dialog(self)

    def new_testprogram(self):
        from ATE.org.actions.new.program.NewProgramWizard import new_program_dialog
        new_program_dialog(self)

    def new_flow(self):
        print("new_flow")

    def new_protocol(self):
        print("new_protocol")

    def new_registermap(self):
        print("new_registermap")

    def new_product(self):
        from ATE.org.actions.new.product.NewProductWizard import new_product_dialog
        new_product_dialog(self)

    def new_device(self):
        from ATE.org.actions.new.device.NewDeviceWizard import new_device_dialog
        new_device_dialog(self)

    def new_package(self):
        from ATE.org.actions.new.package.NewPackageWizard import new_package_dialog
        new_package_dialog(self)

    def new_die(self):
        from ATE.org.actions.new.die.NewDieWizard import new_die_dialog
        new_die_dialog(self)

    def new_maskset(self):
        from ATE.org.actions.new.maskset.NewMasksetWizard import new_maskset_dialog
        new_maskset_dialog(self)

    def new_hardwaresetup(self):
        from ATE.org.actions.new.hardwaresetup.NewHardwaresetupWizard import new_hardwaresetup_dialog
        new_hardwaresetup_dialog(self)
        self.update_hardware()

    def new_project(self):
        from ATE.org.actions.new.project.NewProjectWizard import new_project_dialog
        new_project_dialog(self)

    def open_project(self):
        selected_directory = os.path.normpath(
            str(QtWidgets.QFileDialog.getExistingDirectory(self, 
                                                           "Select Directory",
                                                           workspace_path,
                                                           QtWidgets.QFileDialog.ShowDirsOnly
                                                           | QtWidgets.QFileDialog.DontResolveSymlinks)
                )
            )
        if is_ATE_project(selected_directory):         
            self.active_project_path = selected_directory
            self.active_project = os.path.split(self.active_project_path)[-1]            
            self.project_info = project_navigator(self.active_project_path)
            available_hardwares =  self.project_info.get_hardwares()
            print(f"{available_hardwares}")
            available_hardwares.sort()
            print(f"{available_hardwares}")
            if len(available_hardwares)>0:
                self.active_hw = available_hardwares[-1]
                
                self.hw_combo.blockSignals(True)
                self.hw_combo.clear()
                self.hw_combo.addItems(available_hardwares)
                self.hw_combo.setCurrentIndex(len(available_hardwares)-1)
                self.hw_combo.setEnabled(True)
                self.hw_combo.blockSignals(False)
                
                
                self.base_combo.setCurrentIndex(0) # = nothing selected
                self.base_combo.setEnabled(True)
                
                targets = [''] 
                targets += self.project_info.get_dies_for_hardware(self.active_hw)
                targets += self.project_info.get_products_for_hardware(self.active_hw)
                self.target_combo.blockSignals(True)
                self.target_combo.clear()
                self.target_combo.addItems(targets)
                self.target_combo.setCurrentIndex(0) # = nothing
                self.target_combo.setEnabled(True)
                self.target_combo.blockSignals(False)
            else:
                self.active_hw = ''

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



    def edit_test(self):
        print("edit_test")

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

    def edit_maskset(self):
        print("edit_maskset")

    def edit_hardwaresetup(self):
        print("actionhardware_setup")



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

    def display_masksets(self):
        print("display_masksets")



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

    def delete_maskset(self):
        print("delete_maskset")

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
        print(self.get_tree_state())

    def placeholder(self, event):
        print(type(event))
        print(event)





if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window = MainWindow(app)
    window.show()
    sys.exit(app.exec_())

