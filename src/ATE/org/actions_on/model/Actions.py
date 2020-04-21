from ATE.org.actions_on.model.Constants import MenuActionTypes
import qtawesome as qta


ACTIONS = {MenuActionTypes.Edit(): (qta.icon('mdi.lead-pencil', color='orange'), "Edit"),
           MenuActionTypes.Add(): (qta.icon('mdi.plus', color='orange'), "New"),
           MenuActionTypes.AddFile(): (qta.icon('mdi.file-plus', color='orange'), "File"),
           MenuActionTypes.AddFolder(): (qta.icon('mdi.folder-plus', color='orange'), "Folder"),
           MenuActionTypes.View(): (qta.icon('mdi.eye-outline', color='orange'), "View"),
           MenuActionTypes.Delete(): (qta.icon('mdi.minus', color='orange'), "Delete"),
           MenuActionTypes.Import(): (qta.icon('mdi.application-import', color='orange'), "Import"),
           MenuActionTypes.ImportFile(): (qta.icon('mdi.file-import', color='orange'), "File"),
           MenuActionTypes.ImportFolder(): (qta.icon('mdi.folder-download', color='orange'), "Folder"),
           MenuActionTypes.Activate(): (qta.icon('mdi.check', color='orange'), "Activate"),
           MenuActionTypes.CloneTo(): (qta.icon('mdi.application-export', color='orange'), "Clone to ..."),
           MenuActionTypes.CloneFrom(): (qta.icon('mdi.application-import', color='orange'), "Clone from ..."),
           MenuActionTypes.Trace(): (qta.icon('mdi.share-variant', color='orange'), "Trace usage"),
           MenuActionTypes.AddStandardTest(): (qta.icon('mdi.plus-box-outline', color='orange'), "Add Standard Test"),
           MenuActionTypes.Rename(): (qta.icon('mdi.file-edit', color='orange'), "Rename"),
           MenuActionTypes.Move(): (qta.icon('mdi.file-move', color='orange'), "Move"),
           MenuActionTypes.DeleteFile(): (qta.icon('mdi.file-remove', color='orange'), "Remove")}