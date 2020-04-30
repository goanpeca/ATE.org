from ATE.org.actions_on.product.NewProductWizard import NewProductWizard

import os
import re


class ViewProductWizard(NewProductWizard):
    def __init__(self, name, project_info):
        super().__init__(project_info)
        self._setup_view(name)
        ViewProductWizard._setup_dialog_fields(self, name)

    def _setup_view(self, name):
        self.setWindowTitle(' '.join(re.findall('.[^A-Z]*', os.path.basename(__file__).replace('.py', ''))))

        self.WithHardware.setEnabled(False)
        self.ProductName.setEnabled(False)
        self.FromDevice.setEnabled(False)
        self.productQuality.setEnabled(False)
        self.isAGrade.setChecked(False)
        self.isAGrade.setEnabled(False)
        self.referenceGrade.setEnabled(False)
        self.grade.setEnabled(False)
        self.Type.setEnabled(False)
        self.customer.setEnabled(False)

        self.CancelButton.setEnabled(True)
        self.CancelButton.clicked.connect(self.accept)

    @staticmethod
    def _setup_dialog_fields(dialog, name):
        configuration = dialog.project_info.get_product(name)

        dialog.ProductName.setText(name)
        dialog.WithHardware.setCurrentText(configuration['hardware'])
        dialog.FromDevice.setCurrentText(configuration['device'])
        # TODO: no specified
        # dialog.productQuality.setCurrentText('')
        # dialog.isAGrade.setChecked(False)
        # dialog.referenceGrade.setCurrentText('')
        # dialog.grade.setCurrentText('')
        # dialog.Type.setChecked('')

        dialog.Feedback.setText("")
        dialog.OKButton.setEnabled(True)

    def _connect_event_handler(self):
        pass


def display_product_settings_dialog(name, project_info):
    view = ViewProductWizard(name, project_info)
    view.exec_()
    del(view)
