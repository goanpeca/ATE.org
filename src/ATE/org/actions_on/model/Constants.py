from enum import Enum


class MenuActionTypes(Enum):
    Add = "new_item"
    Edit = "edit_item"
    View = "display_item"
    Delete = "delete_item"
    Import = "import_item"
    Activate = "activate_item"
    CloneTo = "clone_to_item"
    CloneFrom = "clone_from_item"
    Trace = "trace_item"
    AddStandardTest = "add_standard_test_item"
    Rename = "rename_item"
    Move = "move_item"
    AddFile = "add_file__item"
    AddFolder = "add_folder_item"
    DeleteFile = "delete_item"
    ImportFile = "import_file_item"
    ImportFolder = "import_dir_item"

    def __call__(self):
        return self.value
