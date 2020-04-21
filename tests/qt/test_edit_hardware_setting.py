import pytest
from PyQt5 import QtCore, Qt

import sqlite3
import pickle

from ATE.org.actions_on.hardwaresetup.EditHardwaresetupWizard import EditHardwaresetupWizard
from ATE.org.navigation import project_navigator

from pytestqt.qt_compat import qt_api  # debug prints inside unittests


def debug_message(message):
    qt_api.qWarning(message)


# using this function when running CI build will block for ever
# !!! DON'T !!!
# just for localy debuging purposes
def debug_visual(window, qtbot):
    window.show()
    qtbot.stopForInteraction()


CONFIGURATION = {'SingleSiteLoadboard': 'abc',
                 'SingleSiteDIB': 'bca',
                 'MultiSiteLoadboard': 'c',
                 'MultiSiteDIB': 'd',
                 'ProbeCard': 'e',
                 'Parallelism': 1}

DEFAULT_CONFIGURATION = {'SingleSiteLoadboard': 'a',
                         'SingleSiteDIB': 'b',
                         'MultiSiteLoadboard': 'c',
                         'MultiSiteDIB': 'd',
                         'ProbeCard': 'e',
                         'Parallelism': 1}

DB_FILE = "./tests/qt/test.sqlite5"
HW_NAME = "HW1"


def setup_method():
    def setup(test_func):
        def wrap(qtbot):
            proj_nav = project_navigator(None, "./tests/qt/")
            proj_nav.db_file = DB_FILE
            return test_func(proj_nav, qtbot)
        return wrap
    return setup

@setup_method()
def test_store_configuration(proj_nav, qtbot):
    con = proj_nav.con
    cur = proj_nav.cur
    cur.execute('DROP TABLE IF EXISTS hardwares')
    cur.execute('CREATE TABLE hardwares ("name", "definition")')

    # insert new hw configuration
    blob = pickle.dumps(DEFAULT_CONFIGURATION, 4)
    query = 'insert into hardwares(name, definition) VALUES (?, ?)'
    cur.execute(query, (HW_NAME, blob))

    get_blob_query = 'select definition from hardwares where name = ?'
    cur.execute(get_blob_query, (HW_NAME,))
    config = pickle.loads(cur.fetchone()[0])

    # check db content with stored configuration
    for key, value in config.items():
        assert DEFAULT_CONFIGURATION[key] == value

    window = EditHardwaresetupWizard(proj_nav, HW_NAME)
    qtbot.addWidget(window)

    # edit Dialog components
    window.SingleSiteLoadboard.clear()
    qtbot.keyClicks(window.SingleSiteLoadboard, "abc")
    window.SingleSiteDIB.clear()
    qtbot.keyClicks(window.SingleSiteDIB, "bca")

    with qtbot.waitSignal(window.OKButton.clicked):
        qtbot.mouseClick(window.OKButton, QtCore.Qt.LeftButton)

        get_blob_query = 'select definition from hardwares where name = ?'
        cur.execute(get_blob_query, (HW_NAME,))
        config = pickle.loads(cur.fetchone()[0])

        # check after edit
        for key, value in config.items():
            assert CONFIGURATION[key] == value

        con.close()
