from ATE.org.actions_on.program.TestProgramWizard import TestProgramWizard
from ATE.org.actions_on.program.ViewTestProgramWizard import ViewTestProgramWizard


class EditTestProgramWizard(TestProgramWizard):
    def __init__(self, name, project_info, owner, prog_name):
        super().__init__(project_info, owner, edit_on=False, prog_name=prog_name)
        ViewTestProgramWizard.setup_view(self, name)


def edit_program_dialog(name, project_info, owner, prog_name):
    testProgramWizard = EditTestProgramWizard(name, project_info, owner, prog_name)
    testProgramWizard.exec_()
    del(testProgramWizard)
