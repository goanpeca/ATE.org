from ATE.org.actions_on.hardwaresetup.HardwareWizard import HardwareWizard
from ATE.org.actions_on.hardwaresetup.ViewHardwaresetupSettings import ViewHardwaresetupSettings
import re
import os


class EditHardwaresetupWizard(HardwareWizard):
    def __init__(self, project_info, hw_name):
        super().__init__(project_info)

        self.setWindowTitle(' '.join(re.findall('.[^A-Z]*', os.path.basename(__file__).replace('.py', ''))))
        self.hardware.setText(hw_name)

        ViewHardwaresetupSettings._setup_dialog_fields(self, hw_name)

    def OKButtonPressed(self):
        self.project_info.update_hardware(self.hardware.text(), self._get_current_configuration())
        self.accept()


def edit_hardwaresetup_dialog(project_info, hw_name):
    edit_hw = EditHardwaresetupWizard(project_info, hw_name)
    edit_hw.exec_()
    del(edit_hw)
