from PyQt5 import QtCore, QtGui

from ATE.org.actions_on.model.BaseItem import BaseItem

from ATE.org.actions_on.hardwaresetup.HardwaresetupItem import HardwaresetupItem
from ATE.org.actions_on.maskset.MasksetItem import MasksetItem
from ATE.org.actions_on.die.DieItem import DieItem
from ATE.org.actions_on.package.PackageItem import PackageItem
from ATE.org.actions_on.device.DeviceItem import DeviceItem
from ATE.org.actions_on.product.ProductItem import ProductItem

from ATE.org.actions_on.model import FlowItem as FlowItem

from ATE.org.actions_on.tests.TestItem import TestItem

from ATE.org.actions_on.documentation.DocumentationObserver import DocumentationObserver
from ATE.org.actions_on.documentation.DocumentationItem import DocumentationItem
from ATE.org.constants import TableIds


class TreeModel(QtGui.QStandardItemModel):
    edit_file = QtCore.pyqtSignal(["QString"])
    delete_file = QtCore.pyqtSignal(["QString"])

    def __init__(self, project_info, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setHorizontalHeaderLabels([self.tr("Project")])
        self.project_info = project_info
        self.hardware = ''
        self.base = ''
        self.target = ''
        import os
        self.doc_path = os.path.join(self.project_info.project_directory, "doc")
        self.tests_path = os.path.join(self.project_info.project_directory, "src", "tests")
        self._setup()
        self._connect_action_handler()
        self.update(self.hardware, self.base, self.target)

    def on_db_change(self, table_id):
        if table_id == TableIds.Flow():
            self.flows.update()

        # Note: This will basically rebuild the complete "definitions"
        # subtree. We might get performance problems here, if we ever
        # encounter a project with *lots* of definition items. If
        # this ever happens we can split updating the trees into
        # individual subtrees using the table_id and calling update
        # only on the matching subtree node.
        if table_id in [TableIds.Definition(), TableIds.Hardware(),
                        TableIds.Maskset(), TableIds.Device(),
                        TableIds.Die(), TableIds.Package(),
                        TableIds.Product()]:
            self._update_definitions()
            self.update(self.hardware, self.base, self.target)

    def _connect_action_handler(self):
        self.itemChanged.connect(lambda item: self._update(item, self.hardware, self.base, self.target))
        self.project_info.database_changed.connect(self.on_db_change)
        self.project_info.active_product_changed.connect(self.apply_toolbar_change)
        self.project_info.active_base_changed.connect(self.apply_toolbar_change)
        self.project_info.active_hardware_changed.connect(self.apply_toolbar_change)

    def apply_toolbar_change(self):
        self.base = self.project_info.activeBase
        self.target = self.project_info.activeProduct
        self.hardware = self.project_info.activeHardware

        self.flows.update()
        self._update_tests()
        self.update(self.hardware, self.base, self.target)

    def _setup(self):
        self.root_item = SectionItem(self.project_info, "project_name")
        self._setup_definitions()
        self._setup_documentations()
        self._setup_flow_items(self.project_info)
        self._setup_tests()
        self.appendRow(self.root_item)

    def _setup_flow_items(self, parent):
        self.flows = FlowItem.FlowItem(parent, "flows")
        self.production_flows = BaseItem(self.flows, "production")
        self.flows.appendRow(self.production_flows)
        self.engineering_flows = BaseItem(self.flows, "engineering")
        self.flows.appendRow(self.engineering_flows)
        self.validation_flows = BaseItem(self.flows, "validation")
        self.flows.appendRow(self.validation_flows)
        self.characterisation_flows = BaseItem(self.flows, "characterisation")
        self.flows.appendRow(self.characterisation_flows)

        self.quali_flows = FlowItem.FlowItem(self.project_info, "qualification", self.flows)
        self.quali_flows.appendRow(FlowItem.SimpleFlowItem(parent, "ZHM", "Zero Hour Measurements", None))
        self.quali_flows.appendRow(FlowItem.SimpleFlowItem(parent, "EC", "Endurance Cycling", None))
        self.quali_flows.appendRow(FlowItem.SimpleFlowItem(parent, "ABSMAX", "Absolute Maximum Ratings", None))
        self.quali_flows.appendRow(FlowItem.SimpleFlowItem(parent, "XRAY", "", None))
        self.quali_flows.appendRow(FlowItem.SimpleFlowItem(parent, "LI", "Lead Integrity", None))
        self.quali_flows.appendRow(FlowItem.SimpleFlowItem(parent, "RSH", "Resistance to Solder Heat", None))
        self.quali_flows.appendRow(FlowItem.SimpleFlowItem(parent, "SA", "SolderAbility", None))

        self.quali_flows.appendRow(self._make_multi_instance_quali_flow_item(parent, "ATE.org.actions_on.flow.ESD.esdwizard"))
        self.quali_flows.appendRow(self._make_multi_instance_quali_flow_item(parent, "ATE.org.actions_on.flow.HTOL.htolwizard"))
        self.quali_flows.appendRow(self._make_multi_instance_quali_flow_item(parent, "ATE.org.actions_on.flow.HTSL.htslwizard"))
        self.quali_flows.appendRow(self._make_multi_instance_quali_flow_item(parent, "ATE.org.actions_on.flow.DR.drwizard"))
        self.quali_flows.appendRow(self._make_multi_instance_quali_flow_item(parent, "ATE.org.actions_on.flow.RSH.rshwizard"))
        self.quali_flows.appendRow(self._make_multi_instance_quali_flow_item(parent, "ATE.org.actions_on.flow.AC.acwizard"))

        self.quali_flows.appendRow(self._make_single_instance_quali_flow_item(parent, "ATE.org.actions_on.flow.HAST.hastwizard"))
        self.quali_flows.appendRow(self._make_single_instance_quali_flow_item(parent, "ATE.org.actions_on.flow.ELFR.elfrwizard"))
        self.quali_flows.appendRow(self._make_single_instance_quali_flow_item(parent, "ATE.org.actions_on.flow.LU.luwizard"))
        self.quali_flows.appendRow(self._make_single_instance_quali_flow_item(parent, "ATE.org.actions_on.flow.TC.tcwizard"))
        self.quali_flows.appendRow(self._make_single_instance_quali_flow_item(parent, "ATE.org.actions_on.flow.THB.thbwizard"))
        self.quali_flows.appendRow(self._make_single_instance_quali_flow_item(parent, "ATE.org.actions_on.flow.LU.luwizard"))

        self.flows.appendRow(self.quali_flows)
        self.root_item.appendRow(self.flows)
        # Make sure the items have the correct state with respect to
        # the current toolbar state
        self.flows.update()

    def _make_single_instance_quali_flow_item(self, parent, module):
        return FlowItem.SingleInstanceQualiFlowItem(parent, "Tmp", module)

    def _make_multi_instance_quali_flow_item(self, parent, module):
        return FlowItem.MultiInstanceQualiFlowItem(parent, "Tmp", module)

    def _setup_documentations(self):
        # TODO: do we need a sorting-order (alphabetic, etc...) ?
        self.documentations_section = DocumentationItem("documentations", self.doc_path, is_editable=False)
        self.doc_observer = DocumentationObserver(self.doc_path, self.documentations_section)
        self.doc_observer.start_observer()

        self.root_item.insert_item(self.documentations_section)

    def _update_definitions(self):
        self.definition_section.update()

    def _setup_definitions(self):
        self.definition_section = SectionItem(self.project_info, "definitions")

        self.hardwaresetup = HardwaresetupItem(self.project_info, "hardwaresetups")
        self.definition_section.insert_item(self.hardwaresetup)

        self.maskset = MasksetItem(self.project_info, "masksets")
        self.definition_section.insert_item(self.maskset)

        self.die = DieItem(self.project_info, "dies")
        self.definition_section.insert_item(self.die)

        self.package = PackageItem(self.project_info, "packages")

        self.definition_section.insert_item(self.package)

        self.device = DeviceItem(self.project_info, "devices")
        self.definition_section.insert_item(self.device)

        self.product = ProductItem(self.project_info, "products")
        self.definition_section.insert_item(self.product)

        self.root_item.insert_item(self.definition_section)

    def _update(self, item, hw, base, target):
        self.update(hw, base, target)

    def update(self, hardware, base, target):
        # die update state
        self.hardware = hardware
        self.base = base
        self.target = target

        if self.die.has_children():
            self.die.set_children_hidden(False)
        else:
            if self.maskset.has_children() and \
               self.hardwaresetup.has_children() and \
               base == 'PR':
                self.die.set_children_hidden(False)
            else:
                self.die.set_children_hidden(True)

        # device update state
        if self.device.has_children():
            self.device.set_children_hidden(False)
        else:
            if self.die.has_children() and \
               self.package.has_children() and \
               self.hardwaresetup.has_children() and \
               base == 'FT':
                self.device.set_children_hidden(False)
            else:
                self.device.set_children_hidden(True)

        # product update state
        if self.product.has_children():
            self.product.set_children_hidden(False)
        else:
            if self.device.has_children() and \
               self.hardwaresetup.has_children() and \
               base == 'FT':
                self.product.set_children_hidden(False)
            else:
                self.product.set_children_hidden(True)

    def _setup_tests(self):
        self.tests_section = TestItem(self.project_info, "tests", self.tests_path, self)
        self.root_item.appendRow(self.tests_section)

    def _update_tests(self):
        self.tests_section.update()


# ToDo: Move this class to its own file.
# Also: Check if it is really needed. The added value basically none
class SectionItem(BaseItem):
    def __init__(self, project_info, name, parent=None):
        super().__init__(project_info, name, parent)
        self.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

    def insert_item(self, item):
        self.insertRow(0, item)

    def is_hidden(self):
        return True

    def is_editable(self):
        return True

    def update(self):
        for c in range(int(0), self.rowCount()):
            item = self.child(c)
            item.update()
