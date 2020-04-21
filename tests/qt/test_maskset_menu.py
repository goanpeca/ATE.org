import pytest
from PyQt5 import QtCore, Qt, QtWidgets

from ATE.org.actions_on.maskset.MasksetItem import MasksetItem
from ATE.org.actions_on.maskset.MasksetItem import MasksetItemChild
from ATE.org.actions_on.model.BaseItem import BaseItem
from ATE.org.actions_on.model.TreeModel import TreeModel

from pytestqt.qt_compat import qt_api  # debug prints inside unittests


def debug_message(message):
    qt_api.qWarning(message)


class MainWindowMock():
    def __init__(self):
        pass


def test_create_parent_child_node(mocker):
    mocker.patch.object(MasksetItem, '_get_children_names', return_value=['abs', 'sba'])

    mocker.patch.object(MasksetItemChild, '_get_children_names', return_value=[])

    main = MainWindowMock()
    parent_name = "maskset"
    maskset = MasksetItem(main, parent_name)
    assert parent_name == maskset.text()
    assert len(maskset.child_set) == 2
    assert maskset.rowCount() == 2
    assert maskset.child(0).text() == 'abs'
    assert maskset.child(1).text() == 'sba'
