# -*- coding: utf-8 -*-
from ATE.org.actions_on.flow.qualificationwizardbase.parameter import parameter
from PyQt5 import QtCore, QtGui, QtWidgets, uic

# The option parameter represents a parameter with a name and
# a predefined number of choices. It will create a combobox
# containing the choiches and a lable containing the name. As
# the user is locked into predefined choices no validation is
# done on the input date.
# Attention: Serialisation of this parameter stores the name of
# the selected item. If the OptionParam is fed data that is
# not compatible it will fall to the default value for this
# parameter. This will also happen if the dialog  using the 
# parameter changes the name of a parameter and loads data
# with the older parameter name.
class OptionParam(parameter):
    
    def __init__(self, name, items: list):
        self.name = name
        self.items = items
        self.combobox = QtWidgets.QComboBox()
 
        self.combobox.setObjectName(f"cb{name}")
        for itm in items:
            self.combobox.addItem(str(itm), str(itm))

    # This method shall create the ui controls that
    # represent this parameter
    def create_ui_components(self, parent_container, on_change_handler):
        
        self.combobox.currentIndexChanged.connect(on_change_handler)
        
        # Create Label with parameter name
        layout = QtWidgets.QHBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignLeft)

        textField = QtWidgets.QLabel()
        textField.setText(self.name)
        textField.setMaximumWidth(196)
        layout.addWidget(textField)
        
        # Append combo box
        self.combobox.setMaximumWidth(256)
        layout.addWidget(self.combobox)
        layout.insertStretch(1)
        
        parent_container.addLayout(layout)
        return layout

    def get_selection(self) -> str:
        return self.combobox.currentText()

    # The validate method shall yield true, if the
    # data entered in the parameters fields is correct
    def validate(self) -> bool:
        return self.combobox.currentIndex() >= 0

    def disable_ui_components(self):
        self.combobox.setEnabled(False)

    def store_values(self, dst: dict):
        dst[self.name] = self.combobox.currentText()


    def load_values(self, src):
        if(self.name in src):
            self.combobox.setCurrentIndex(self.combobox.findData(src[self.name]))
        else:
            self.combobox.setCurrentIndex(0)