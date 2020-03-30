from ATE.org.actions_on.hardwaresetup.NewHardwaresetupWizard import NewHardwaresetupWizard
from ATE.org.actions_on.hardwaresetup.ViewHardwaresetupSettings import ViewHardwaresetupSettings
import re
import os


class EditHardwaresetupWizard(NewHardwaresetupWizard):
    def __init__(self, project_info, hw_name):
        super().__init__(project_info)

        self.setWindowTitle(' '.join(re.findall('.[^A-Z]*', os.path.basename(__file__).replace('.py', ''))))
        self.HardwareSetup.setText(hw_name)

        self.hw_configuration = self.project_info.get_hardware_definition(hw_name)
        ViewHardwaresetupSettings._show(self, self.hw_configuration)

    def OKButtonPressed(self):
        self.project_info.update_hardware(self.HardwareSetup.text(), self._get_actual_definition())
        self.accept()


def edit_hardwaresetup_dialog(project_info, hw_name):
    edit_hw = EditHardwaresetupWizard(project_info, hw_name)
    edit_hw.exec_()
    del(edit_hw)
