from ATE.org.actions_on.die.DieWizard import DieWizard
from ATE.org.actions_on.die.ViewDieWizard import ViewDieWizard
import re
import os


class EditDieWizard(DieWizard):
    def __init__(self, project_info, name):
        super().__init__(project_info, read_only=True)
        self.dieName.setEnabled(False)
        self.setWindowTitle(' '.join(re.findall('.[^A-Z]*', os.path.basename(__file__).replace('.py', ''))))
        ViewDieWizard._setup_dialog_fields(self, name)

    def OKButtonPressed(self):
        configuration = self._get_current_configuration()
        self.project_info.update_die(configuration['name'], configuration['hardware'], configuration['maskset'],
                                     configuration['grade'], configuration['grade_reference'], configuration['quality'],
                                     configuration['customer'])
        self.accept()


def edit_die_dialog(project_info, name):
    edit_hw = EditDieWizard(project_info, name)
    edit_hw.exec_()
    del(edit_hw)
