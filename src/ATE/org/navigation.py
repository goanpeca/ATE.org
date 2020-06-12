# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 14:08:04 2020

@author: hoeren
"""

import os
import platform
import sqlite3
import pickle
import shutil
from pathlib import Path as create_file

from PyQt5.QtCore import QObject, pyqtSignal

from ATE.org.constants import TableIds as TableId
from ATE.org.validation import is_ATE_project


class ProjectNavigation(QObject):
    '''
    This class takes care of the project creation/navigation/evolution.
    '''
    # The parameter contains the type of the dbchange (i.e. which table was altered)
    database_changed = pyqtSignal(int)
    toolbar_changed = pyqtSignal(str, str, str)
    active_project_changed = pyqtSignal()
    hardware_added = pyqtSignal(str)
    hardware_activated = pyqtSignal(str)
    hardware_removed = pyqtSignal(str)
    update_target = pyqtSignal()
    update_settings = pyqtSignal(str, str, str)

    verbose = True

    def __init__(self, project_directory, workspace_path, parent, project_quality=''):
        super().__init__(parent)
        self.workspace_path = workspace_path
        self.__call__(project_directory, project_quality)

    def __call__(self, project_directory, project_quality=''):
        # determine OS, determine user & desktop
        self.os = platform.system()
        if self.os == 'Windows':
            self.desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        elif self.os == 'Linux':
            self.desktop_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
        elif self.os == 'Darwin':  # TODO: check on mac if this works
            self.desktop_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
        else:
            raise Exception("unrecognized operating system")
        self.user = self.desktop_path.split(os.sep)[-2]
        self.template_directory = os.path.join(os.path.dirname(__file__), 'templates')

        # TODO: take the keychain in here ?!?

        if project_directory == '':
            self.project_directory = ''
            self.active_target = ''
            self.active_hardware = ''
            self.active_base = ''
            self.project_name = ''
            self.project_quality = ''
            self.db_file = ''
            self.con = None
        else:
            self.project_directory = project_directory
            self.active_target = ''
            self.active_hardware = ''
            self.active_base = ''
            self.project_name = os.path.split(self.project_directory)[-1]

            self.db_file = os.path.join(project_directory, f"{self.project_name}.sqlite3")

            project_quality_file = os.path.join(self.project_directory, 'project_quality.pickle')
            if not os.path.exists(self.project_directory):  # brand new project, initialize it.
                self.create_project_structure()
                self.project_quality = project_quality
                if project_quality != '':
                    with open(project_quality_file, 'wb') as writer:
                        pickle.dump(project_quality, writer, 4)
                self.con = sqlite3.connect(self.db_file)
                self.cur = self.con.cursor()
                self.create_project_database()
            else:
                if os.path.exists(project_quality_file):
                    with open(project_quality_file, 'rb') as reader:
                        self.project_quality = pickle.load(reader)
                else:
                    self.project_quality = ''

                self._set_folder_structure()
                self.con = sqlite3.connect(self.db_file)
                self.cur = self.con.cursor()

        if self.verbose:
            print(f"operating system = '{self.os}'")
            print(f"user = '{self.user}'")
            print(f"desktop path = '{self.desktop_path}'")
            print(f"template path = '{self.template_directory}'")
            print(f"project path = '{self.project_directory}'")
            print(f"active target = '{self.active_target}'")
            print(f"active hardware = '{self.active_hardware}'")
            print(f"active base = '{self.active_base}'")
            print(f"project name = '{self.project_name}'")
            print(f"project grade = '{self.project_quality}'")
            print(f"project db file = '{self.db_file}'")

    def update_toolbar_elements(self, active_hardware, active_base, active_target):
        self.active_hardware = active_hardware
        self.active_base = active_base
        self.active_target = active_target
        self._store_settings()
        self.toolbar_changed.emit(self.active_hardware, self.active_base, self.active_target)

    def update_active_hardware(self, hardware):
        self.active_hardware = hardware
        self.hardware_activated.emit(hardware)

    def _set_folder_structure(self):
        # make sure that the doc structure is obtained
        doc_path = os.path.join(self.project_directory, "doc")
        os.makedirs(os.path.join(doc_path, "audits"), exist_ok=True)
        os.makedirs(os.path.join(doc_path, "exports"), exist_ok=True)

    def create_project_structure(self):
        '''
        this method creates a new project (self.project_directroy must *not*
        exist yet, otherwhise an exception will be raised)
        '''
        if os.path.exists(self.project_directory):
            raise Exception(f"project directory '{self.project_directory}' already exists.")
        else:
            from ATE.org.coding.generators import project_generator
            project_generator(self.project_directory)

    def create_project_database(self):
        '''
        this method will create a new (and empty) database file.
        '''
        # devices
        self.cur.execute('''CREATE TABLE "devices" (
                         "name"	TEXT NOT NULL UNIQUE,
                         "hardware"	TEXT NOT NULL,
                         "package"	TEXT NOT NULL,
                         "definition"	BLOB NOT NULL,
                         "is_enabled" BOOL,

                            PRIMARY KEY("name"),
                         FOREIGN KEY("hardware") REFERENCES "hardwares"("name"),
                         FOREIGN KEY("package") REFERENCES "packages"("name")
                         );''')
        self.con.commit()
        # dies
        self.cur.execute('''CREATE TABLE "dies" (
                         "name"	TEXT NOT NULL UNIQUE,
                         "hardware"	TEXT NOT NULL,
                         "maskset"	TEXT NOT NULL,
                         "grade"	TEXT NOT NULL
                                CHECK (grade=='A' OR
                                       grade=='B' OR
                                       grade=='C' OR
                                       grade=='D' OR
                                       grade=='E' OR
                                       grade=='F' OR
                                       grade=='G' OR
                                       grade=='H' OR
                                       grade=='I'),
                         "grade_reference"	TEXT NOT NULL,
                         "quality"	TEXT NOT NULL,
                         "type" TEXT NOT NULL,
                         "customer"	TEXT NOT NULL,
                         "is_enabled" BOOL,

                         PRIMARY KEY("name"),
                         FOREIGN KEY("hardware")
                                REFERENCES "hardware"("name"),
                         FOREIGN KEY("maskset")
                                REFERENCES "masksets"("name")
                         );''')
        self.con.commit()
        # flows
        self.cur.execute('''CREATE TABLE "flows" (
                         "name"   TEXT NOT NULL,
                         "base"   TEXT NOT NULL
                               CHECK(base=='PR' OR base=='FT'),
                         "target"	TEXT NOT NULL,
                         "type"   TEXT NOT NULL,
                         "is_enabled" BOOL,

                            PRIMARY KEY("name")
                         );''')
        self.con.commit()

        # qualification flow data:
        self.cur.execute('''CREATE TABLE "qualification_flow_data" (
                            "name"	    TEXT NOT NULL,
                            "type"       TEXT NOT NULL,
                            "product"    TEXT NOT NULL,
                            "data"	    BLOB NOT NULL,

                            PRIMARY KEY("name"),
                            FOREIGN KEY("product") REFERENCES "products"("name")
                         );''')
        self.con.commit()

        # hardwares
        self.cur.execute('''CREATE TABLE "hardwares" (
                         "name"	TEXT NOT NULL UNIQUE,
                         "definition"	BLOB NOT NULL,
                         "is_enabled" BOOL,

                             PRIMARY KEY("name")
                         );''')
        self.con.commit()
        # masksets
        self.cur.execute('''CREATE TABLE "masksets" (
                         "name"	TEXT NOT NULL UNIQUE,
                         "customer"	TEXT NOT NULL,
                         "definition"	BLOB NOT NULL,
                         "is_enabled" BOOL,
                         PRIMARY KEY("name")
                         );''')
        self.con.commit()
        # packages
        self.cur.execute('''CREATE TABLE "packages" (
                         "name"	TEXT NOT NULL UNIQUE,
                         "leads"	INTEGER NOT NULL
                               CHECK(leads>=2 AND leads<=99),
                         "is_enabled" BOOL,
                         "is_naked_die" BOOL,
                         PRIMARY KEY("name")
                         );''')
        self.con.commit()
        # products
        self.cur.execute('''CREATE TABLE "products" (
                         "name"	TEXT NOT NULL UNIQUE,
                         "device"	TEXT NOT NULL,
                         "hardware"	TEXT NOT NULL,
                         "is_enabled" BOOL,
                         "grade"	TEXT NOT NULL
                                CHECK (grade=='A' OR
                                       grade=='B' OR
                                       grade=='C' OR
                                       grade=='D' OR
                                       grade=='E' OR
                                       grade=='F' OR
                                       grade=='G' OR
                                       grade=='H' OR
                                       grade=='I'),
                         "grade_reference"	TEXT NOT NULL,
                         "quality"	TEXT NOT NULL,
                         "type" TEXT NOT NULL,
                         "customer"	TEXT NOT NULL,

                         PRIMARY KEY("name"),
                         FOREIGN KEY("device") REFERENCES "devices"("name"),
                         FOREIGN KEY("hardware") REFERENCES "hardware"("name")
                         );''')
        self.con.commit()
        # sequence
        self.cur.execute('''CREATE TABLE "sequence" (
                         "id"	INTEGER PRIMARY KEY AUTOINCREMENT,
                         "owner_name" TEXT NOT NULL,
                         "prog_name"  TEXT NOT NULL,
                         "test"     TEXT NOT NULL,
                         "test_order" INTEGER,
                         "definition"   BLOB NOT NULL
                         );''')
        self.con.commit()

        # programs
        self.cur.execute('''CREATE TABLE "programs" (
                         "id"	INTEGER PRIMARY KEY AUTOINCREMENT,
                         "prog_name"	TEXT NOT NULL,
                         "owner_name"	TEXT NOT NULL,
                         "prog_order" INTEGER,
                         "hardware"	TEXT NOT NULL,
                         "base"	TEXT NOT NULL
                                CHECK(base=='PR' OR base=='FT'),
                         "target" TEXT NOT NULL,
                         "usertext" TEXT NOT NULL,
                         "sequencer_type" TEXT NOT NULL,
                         "temperature" BLOB NOT NULL,
                         FOREIGN KEY("hardware") REFERENCES "hardwares"("name"),
                         FOREIGN KEY("target") REFERENCES "targets"("name")
                         );''')
        self.con.commit()

        # tests
        self.cur.execute('''CREATE TABLE "tests" (
                         "name"	TEXT NOT NULL UNIQUE,
                         "hardware"	TEXT NOT NULL,
                         "type"	TEXT NOT NULL
                               CHECK(type=='standard' OR type=='custom'),
                         "base"	TEXT NOT NULL
                               CHECK(base=='PR' OR base=='FT'),
                         "definition"	BLOB NOT NULL,
                         "is_enabled" BOOL,

                         PRIMARY KEY("name"),
                         FOREIGN KEY("hardware") REFERENCES "hardwares"("name")
                         );''')
        self.con.commit()

    def add_project(self, project_name, project_quality=''):
        project_directory = os.path.join(self.workspace_path, project_name)
        self.__call__(project_directory, project_quality)

    def dict_projects(self, workspace_path=''):
        '''
        given a workspace_path, create a list with projects as key, and their
        (absolute) project_path as value.
        if workspace_path is empty, the parent's "workspace_path" is used.
        '''
        retval = {}
        if workspace_path == '':
            workspace_path = self.workspace_path
        for directory in os.listdir(workspace_path):
            full_directory = os.path.join(workspace_path, directory)
            if os.path.isdir(full_directory):
                retval[directory] = full_directory
        return retval

    def list_projects(self, workspace_path=''):
        '''
        given a workspace_path, extract a list of all projects
        '''
        if workspace_path == '':
            workspace_path = self.workspace_path
        return list(self.dict_projects(workspace_path))

    def list_ATE_projects(self, workspace_path=''):
        '''
        given a workspace_path, extract a list of all ATE projects
        if workspace_path is empty, the parent's "workspace_path" will be used.
        '''
        if workspace_path == '':
            workspace_path = self.workspace_path
        return list(self.dict_ATE_projects(workspace_path))

    def dict_ATE_projects(self, workspace_path=''):
        '''
        given a workspace_path, create a dictionary with all ATE projects as key,
        and the (absolute) project_path as value.
        if workspace_path is empty, the parent's "workspace_path" is used.
        '''
        retval = {}
        if workspace_path == '':
            workspace_path = self.workspace_path
        all_projects = self.dict_projects(workspace_path)
        for candidate in all_projects:
            possible_ATE_project = all_projects[candidate]
            if is_ATE_project(possible_ATE_project):
                retval[candidate] = possible_ATE_project
        return retval

    def add_hardware(self, definition, is_enabled=True):
        '''This method adds a hardware setup to the project.

        The hardware is defined in the 'definition' parameter as follows:
            hardware_definition = {
                'hardware': 'HW0',
                'PCB': {},
                'tester': ('SCT', 'import stuff'),
                'instruments': {},
                'actuators': {}}

        This method returns the name of the Hardware on success and raises an
        exception on fail (no sense of continuing, this should work!)
        '''
        awaited_name = self.get_next_hardware()
        new_hardware = definition['hardware']
        if not awaited_name == new_hardware:
            raise Exception(f"something wrong with the name !!! '{awaited_name}'<->'{new_hardware}'")

        try:  # make the directory structure
            from ATE.org.coding.generators import hardware_generator
            hardware_generator(self.project_directory, definition)
        except Exception as e:  # explode on fail
            print(f"failed to create hardware structure for {definition['hardware']}")
            raise e

        # blob do not have to contain hardware name it's already our primary key
        # TODO: cleaner impl.
        definition.pop('hardware')
        # fill the database on success
        blob = pickle.dumps(definition, 4)
        query = '''INSERT INTO hardwares(name, definition, is_enabled) VALUES (?, ?, ?)'''
        self.cur.execute(query, (new_hardware, blob, is_enabled))
        self.con.commit()

        # let ATE.org know that we have new hardware
        self.hardware_added.emit(new_hardware)
        self.database_changed.emit(TableId.Hardware())

    def update_hardware(self, hardware, definition):
        '''
        this method will update hardware 'name' with 'definition'
        if name doesn't exist, a KeyError will be thrown
        '''
        # try:
        #     from ATE.org.coding.generators import hardware_generator
        #     hardware_generator(self.project_directory, definition)
        # except Exception as e:  # explode on fail
        #     print(f"failed to update hardware structure for {definition['hardware']}")
        #     raise e

        # blob do not have to contain hardware name it's already our primary key
        # TODO: cleaner impl.
        definition.pop('hardware')
        # update the database on success
        blob = pickle.dumps(definition, 4)
        update_blob_query = '''UPDATE hardwares SET definition = ? WHERE name = ?'''
        self.cur.execute(update_blob_query, (blob, hardware))
        self.con.commit()

    def get_hardwares_info(self):
        '''
        This method will return a DICTIONARY with as key all hardware names,
        and as key the definition.
        '''
        query = '''SELECT name, definition, is_enabled FROM hardwares'''
        self.cur.execute(query)
        retval = {}
        for row in self.cur.fetchall():
            retval[row[0]] = pickle.loads(row[1])
        return retval

    def get_available_hardwares(self):
        query = '''SELECT name, is_enabled FROM hardwares'''
        self.cur.execute(query)
        retval = []
        for row in self.cur.fetchall():
            if not row[1]:
                continue
            retval.append(row[0])

        return retval

    def get_hardwares(self):
        '''
        This method will return a list of all hardware names available
        '''
        return list(self.get_hardwares_info())

    def get_next_hardware(self):
        '''
        This method will determine the next available hardware name
        '''
        latest_hardware = self.get_latest_hardware()
        if latest_hardware == '':
            return "HW0"
        else:
            latest_hardware_number = int(latest_hardware.replace('HW', ''))
            return f"HW{latest_hardware_number + 1}"

    def get_latest_hardware(self):
        '''
        This method will determine the latest hardware name and return it
        '''
        available_hardwares = sorted(self.get_hardwares())
        if len(available_hardwares) == 0:
            return ""
        else:
            return available_hardwares[-1]

    def get_hardware_definition(self, name):
        '''
        this method retreives the hwr_data for hwr_nr.
        if hwr_nr doesn't exist, an empty dictionary is returned
        '''
        available_hardwares = self.get_hardwares_info()
        if name in available_hardwares:
            return available_hardwares[name]
        else:
            return {}

    def remove_hardware(self, name):
        query = '''DELETE FORM hardware WHERE name = ?'''
        self.cur.execute(query, (name,))
        self.con.commit()
        self.database_changed.emit(TableId.Hardware())

    def add_maskset(self, name, customer, definition, is_enabled=True):
        '''
        this method will insert maskset 'name' and 'definition' in the
        database, but prior it will check if 'name' already exists, if so
        it will trow a KeyError
        '''
        existing_masksets = self.get_masksets()
        if name in existing_masksets:
            raise KeyError(f"{name} already exists")
        insert_query = '''INSERT INTO masksets(name, customer, definition, is_enabled) VALUES (?, ?, ?, ?)'''
        blob = pickle.dumps(definition, 4)
        self.cur.execute(insert_query, (name, customer, blob, is_enabled))
        self.con.commit()
        self.database_changed.emit(TableId.Maskset())

    def update_maskset(self, name, definition):
        '''
        this method will update the definition of maskset 'name' to 'definition'
        '''
        existing_masksets = self.get_masksets()
        if name not in existing_masksets:
            raise KeyError
        blob = pickle.dumps(definition, 4)
        update_blob_query = '''UPDATE masksets SET definition = ? WHERE name = ?'''
        self.cur.execute(update_blob_query, (blob, name))
        self.con.commit()

    def get_masksets_info(self):
        '''
        this method returns a DICTIONARY with as key all maskset names,
        and as value the tuple (customer, definition)
        '''
        query = '''SELECT name, customer, definition FROM masksets'''
        self.cur.execute(query)
        retval = {}
        for row in self.cur.fetchall():
            retval[row[0]] = (row[1], pickle.loads(row[2]))
        return retval

    def get_available_masksets(self):
        '''
        this method returns a DICTIONARY with as key all maskset names,
        and as value the tuple (customer, definition)
        '''
        query = '''SELECT name, is_enabled FROM masksets'''
        self.cur.execute(query)
        retval = []
        for row in self.cur.fetchall():
            if not row[1]:
                continue

            retval.append(row[0])
        return retval

    def get_masksets(self):
        '''
        this method lists all available masksets
        '''
        return list(self.get_masksets_info())

    def get_ASIC_masksets(self):
        '''
        this method lists all 'ASIC' masksets
        '''
        all_masksets = self.get_masksets_info()
        retval = []
        for maskset in all_masksets:
            if all_masksets[maskset][0] != '':
                retval.append(maskset)
        return retval

    def get_ASSP_masksets(self):
        '''
        this method lists all 'ASSP' masksets
        '''
        all_masksets = self.get_masksets_info()
        retval = []
        for maskset in all_masksets:
            if all_masksets[maskset]['customer'] == '':
                retval.append(maskset)
        return retval

    def get_maskset_definition(self, name):
        '''
        this method will return the definition of maskset 'name'
        '''
        existing_masksets = self.get_masksets()
        if name not in existing_masksets:
            raise KeyError(f"maskset '{name}' doesn't exist")

        get_blob_query = '''SELECT definition FROM masksets WHERE name = ?'''
        self.cur.execute(get_blob_query, (name,))
        return pickle.loads(self.cur.fetchone()[0])

    def get_maskset_customer(self, name):
        '''
        this method will return the customer of maskset 'name'
        (empty string means no customer, thus 'ASSP')
        '''
        query = '''SELECT customer FROM masksets WHERE name = ?'''
        self.cur.execute(query, (name,))
        return self.cur.fetchone()[0]

    def remove_maskset(self, name):
        query = '''DELETE FROM maskset WHERE name = ?'''
        self.cur.execute(query, (name,))
        self.con.commit()
        self.database_changed.emit(TableId.Maskset())

    def add_die(self, name, hardware, maskset, quality, grade, grade_reference, type, customer, is_enabled=True):
        '''
        this method will add die 'name' with the given attributes to the database.
        if 'maskset' or 'hardware' doesn't exist, a KeyError will be raised.
        Also if 'name' already exists, a KeyError will be raised.
        if grade is not 'A'..'I' (9 possibilities) then a ValueError is raised
        if grade is 'A' then grade_reference must be an empty string
        if grade is not 'A', then grade_reference can not be an empty string,
        and it must reference another (existing) die with grade 'A'!
        '''
        insert_query = '''INSERT INTO dies(name, hardware, maskset, quality, grade, grade_reference, type, customer, is_enabled) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        self.cur.execute(insert_query, (name, hardware, maskset, quality, grade, grade_reference, type, customer, is_enabled))
        self.con.commit()
        self.database_changed.emit(TableId.Die())

    def update_die(self, name, hardware, maskset, grade, grade_reference, quality, type, customer, is_enabled=True):
        '''
        this method updates both maskset and hardware for die with 'name'
        '''
        update_query = '''UPDATE dies SET hardware = ?, maskset = ?, grade = ?, grade_reference = ?, quality = ?, type = ?, customer = ?, is_enabled = ?  WHERE name = ?'''
        self.cur.execute(update_query, (hardware, maskset, grade, grade_reference, quality, type, customer, is_enabled, name))
        self.con.commit()

    def update_die_hardware(self, name, hardware):
        '''
        this method will update die 'name' with 'hardware'.
        if 'name' doesn't exist, a KeyError will be raised.
        if 'hardware' doesn't exist, a KeyError will be raised.
        '''
        existing_dies = self.get_dies()
        if name not in existing_dies:
            raise KeyError(f"die'{name}' doesn't exist")

        existing_hardware = self.get_hardwares()
        if hardware not in existing_hardware:
            raise KeyError(f"hardware '{hardware}' doesn't exist")

        update_query = '''UPDATE dies SET hardware = ? WHERE name = ?'''
        self.cur.execute(update_query, (hardware, name))
        self.con.commit()

    def update_die_maskset(self, name, maskset):
        '''
        this method will update die 'name' with 'maskset'.
        if 'name' doesn't exist, a KeyError will be raised.
        if 'maskset' doesn't exist, a KeyError will be raised.
        '''
        existing_dies = self.get_dies()
        if name not in existing_dies:
            raise KeyError(f"{name} already exists")

        existing_masksets = self.get_masksets()
        if maskset not in existing_masksets:
            raise KeyError(f"{maskset} doesn't exist")

        update_query = '''UPDATE dies SET maskset = ? WHERE name = ?'''
        self.cur.execute(update_query, (maskset, name))
        self.con.commit()

    def update_die_grade(self, name, grade, grade_reference):
        print("update_die_grade not implemented yet")

    def update_die_customer(self, name, customer):
        '''
        Note : if the maskset is an ASIC, one can not change the customer to something else !
        '''
        print("update_die_customer not implemented yet")

    def get_dies_info(self):
        '''
        this method will return a DICTIONARY with as keys all existing die names,
        and as value the tuple (hardware, maskset, grade, grade_reference, customer)
        '''
        query = '''SELECT name, hardware, maskset, grade, grade_reference, quality, type, customer, is_enabled FROM dies'''
        self.cur.execute(query)
        retval = {}
        for row in self.cur.fetchall():
            retval[row[0]] = (row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])

        return retval

    def get_available_dies(self):
        query = '''SELECT name, is_enabled FROM dies'''
        self.cur.execute(query)
        retval = []
        for row in self.cur.fetchall():
            if not row[1]:
                continue

            retval.append(row[0])

        return retval

    def get_dies(self):
        '''
        this method will return a LIST of all dies
        '''
        return list(self.get_dies_info())

    def get_dies_for_hardware(self, hardware):
        '''
        this method will return a LIST of all dies that conform to 'hardware'
        '''
        dies_info = self.get_dies_info()
        retval = []
        for die in dies_info:
            if dies_info[die][0] == hardware and dies_info[die][7]:
                retval.append(die)
        return retval

    def get_dies_for_maskset(self, maskset):
        '''
        this method will return a LIST of all dies that conform to 'maskset'
        '''
        dies_info = self.get_dies_info()
        retval = []
        for die in dies_info:
            if dies_info[die][1] == maskset:
                retval.append(die)

        return retval

    def get_dies_for_grade(self, grade):
        '''
        this method will return a LIST of all dies that conform to 'maskset' with 'grade'
        '''
        dies_info = self.get_dies_info()
        retval = []
        for die in dies_info:
            if dies_info[die][2] == grade:
                retval.append(die)
        return retval

    def get_dies_for_grade_reference(self, grade_reference):
        '''
        this method will return a LIST of all dies that conform to 'maskset'
        '''
        dies_info = self.get_dies_info()
        retval = []
        for die in dies_info:
            if dies_info[die][3] == grade_reference:
                retval.append(die)
        return retval

    def get_dies_for_customer(self, customer):
        '''
        this method will return a LIST of all dies that conform to 'maskset'
        '''
        dies_info = self.get_dies_info()
        retval = []
        for die in dies_info:
            if dies_info[die][4] == customer:
                retval.append(die)
        return retval

    def get_die(self, name):
        '''
        this method returns a tuple (hardware, maskset, grade, grade_reference, customer) for die 'name'
        if name doesn't exist, a KeyError will be raised.
        '''
        dies_info = self.get_dies_info()
        if name not in dies_info:
            raise KeyError(f"die'{name}' doesn't exist")

        return dies_info[name]

    def get_die_maskset(self, name):
        '''
        this method returns the maskset of die 'name'
        '''
        return self.get_die(name)[1]

    def get_die_hardware(self, name):
        '''
        this method returns the hardware of die 'name'
        '''
        return self.get_die(name)[0]

    def remove_die(self, name):
        query = '''DELETE FROM die WHERE name = ?'''
        self.cur.execute(query, (name,))
        self.con.commit()
        self.database_changed.emit(TableId.die())

# Packages

    def add_package(self, name, leads, is_naked_die, is_enabled=True):
        '''
        this method will insert package 'name' and 'pleads' in the
        database, but prior it will check if 'name' already exists, if so
        it will trow a KeyError
        '''
        existing_packages = self.get_packages()
        if name in existing_packages:
            raise KeyError(f"package '{name}' already exists")
        query = '''INSERT INTO packages(name, leads, is_enabled, is_naked_die) VALUES (?, ?, ?, ?)'''
        self.cur.execute(query, (name, leads, is_enabled, is_naked_die))
        self.con.commit()
        self.database_changed.emit(TableId.Package())

    def update_package(self, name, leads, is_naked_die, is_enabled=True):
        update_query = '''UPDATE packages SET leads = ?, is_enabled = ?, is_naked_die=? WHERE name = ?'''
        self.cur.execute(update_query, (leads, is_enabled, is_naked_die, name))
        self.con.commit()

    def get_package(self, name):
        packages = self.get_packages_info()

        for key, package in packages.items():
            if key == name:
                return package

        return None

    def is_package_a_naked_die(self, package):
        query = f'''SELECT "is_naked_die" FROM packages where name=? LIMIT 1'''
        self.cur.execute(query, (package,))
        row = self.cur.fetchone()
        # Note: If we are called with an non-existing package this is
        # an error worthy of an exception.
        if row is None:
            raise KeyError
        return row[0]

    def update_package_leads(self, name, leads):
        '''
        this method will update the leads of 'package_name' to 'leads'
        '''
        existing_packages = self.get_packages()
        if name not in existing_packages:
            raise KeyError

        query = '''UPDATE packages SET leads = ? WHERE name = ?'''
        self.cur.execute(query, (leads, name))
        self.con.commit()

    def get_packages_info(self):
        '''
        this method will return a DICTIONARY with ALL packages as key and
        the number of leads as value
        '''
        query = '''SELECT name, leads FROM packages'''
        self.cur.execute(query)
        retval = {}
        for row in self.cur.fetchall():
            retval[row[0]] = [row[1]]

        return retval

    def get_available_packages(self):
        '''
        this method will return a DICTIONARY with ALL packages as key and
        the number of leads as value
        '''
        query = '''SELECT name, is_enabled FROM packages'''
        self.cur.execute(query)
        retval = []
        for row in self.cur.fetchall():
            if not row[1]:
                continue
            retval.append(row[0])

        return retval

    def get_packages(self):
        '''
        this method will return a LIST with all packages
        '''
        return list(self.get_packages_info())

    def package_remove(self, name):
        '''
        this method will remove the package defined by 'name'
        --> we need something like 'trace_package(self, name)'
            to understand what the implications are !!!
        '''
        raise NotImplementedError

# Devices
    def add_device(self, name, hardware, package, definition, is_enabled=True):
        '''
        this method will add device 'name' with 'package' and 'definition'
        to the database.
        if 'name' already exists, a KeyError is raised
        if 'package' doesn't exist, a KeyError is raised
        '''
        existing_packages = self.get_packages()
        if package not in existing_packages:
            raise KeyError(f"package '{package}' doesn't exist")

        insert_query = '''INSERT INTO devices(name, hardware, package, definition, is_enabled) VALUES (?, ?, ?, ?, ?)'''
        blob = pickle.dumps(definition, 4)
        self.cur.execute(insert_query, (name, hardware, package, blob, is_enabled))
        self.con.commit()
        self.database_changed.emit(TableId.Device())

    def update_device(self, name, hardware, package, definition):
        self.update_device_hardware(name, hardware)
        self.update_device_package(name, package)
        self.update_device_definition(name, definition)

    def update_device_hardware(self, name, hardware):
        update_query = '''UPDATE devices SET hardware = ? WHERE name = ?'''
        self.cur.execute(update_query, (hardware, name))
        self.con.commit()

    def update_device_package(self, name, package):
        '''
        this method will update the device package for 'name' to 'package'
        '''
        existing_devices = self.get_devices()
        if name not in existing_devices:
            raise KeyError(f"device '{name}' doesn't exist")

        existing_packages = self.get_packages()
        if package not in existing_packages:
            raise KeyError(f"package '{package}' doesn't exist")

        update_query = '''UPDATE devices SET package = ? WHERE name = ?'''
        self.cur.execute(update_query, (package, name))
        self.con.commit()

    def update_device_definition(self, name, definition):
        '''
        this method will update the definition of device 'name' to 'definition'
        '''
        existing_devices = self.get_devices()
        if name not in existing_devices:
            raise KeyError(f"device '{name}' doesn't exist")

        blob = pickle.dumps(definition, 4)
        update_query = '''UPDATE devices SET definition = ? WHERE name = ?'''
        self.cur.execute(update_query, (blob, name))
        self.con.commit()

    def get_devices(self):
        '''
        this method lists all available devices
        '''
        self.cur.execute("SELECT name FROM devices")
        retval = []
        for row in self.cur.fetchall():
            retval.append(row[0])
        return retval

    def get_devices_for_hardware(self, hardware_name):
        '''
        this method will return a list of devices for 'hardware_name'
        '''
        query = '''SELECT name, is_enabled FROM devices WHERE hardware = ?'''
        self.cur.execute(query, (hardware_name,))
        retval = []
        for row in self.cur.fetchall():
            if not row[1]:
                continue
            retval.append(row[0])
        return retval

    def get_devices_for_hardwares(self):
        query = '''SELECT name, is_enabled FROM devices'''
        self.cur.execute(query)
        retval = []
        for row in self.cur.fetchall():
            retval.append(row[0])

        return retval

    def get_device_hardware(self, name):
        select_query = '''SELECT hardware FROM devices WHERE name = ?'''
        self.cur.execute(select_query, (name,))
        return self.cur.fetchone()[0]

    def get_device_package(self, name):
        '''
        this method will return the package of device 'name'
        '''
        existing_devices = self.get_devices()
        if name not in existing_devices:
            raise KeyError(f"device '{name}' doesn't exist")

        select_query = '''SELECT package FROM devices WHERE name = ?'''
        self.cur.execute(select_query, (name,))
        return self.cur.fetchone()[0]

    def get_device_definition(self, name):
        '''
        this method will return the definition of device 'name'
        '''
        existing_devices = self.get_devices()
        if name not in existing_devices:
            raise KeyError(f"device '{name}' doesn't exist")

        get_blob_query = '''SELECT definition FROM devices WHERE name = ?'''
        self.cur.execute(get_blob_query, (name,))
        return pickle.loads(self.cur.fetchone()[0])

    def get_device(self, name):
        return {'hardware': self.get_device_hardware(name),
                'package': self.get_device_package(name),
                'definition': self.get_device_definition(name)}

    def get_device_dies(self, device):
        definition = self.get_device_definition(device)
        return definition['dies_in_package']

    def trace_device(self, name):
        '''
        this method returns a dictionary of affected objects when device
        'name' is to be deleted.
        '''
        pass

    def remove_device(self, name):
        query = '''DELETE FROM device WHERE name = ?'''
        self.cur.execute(query, (name,))
        self.con.commit()
        self.database_changed.emit(TableId.Device())

    def add_product(self, name, device, hardware, quality, grade, grade_reference, type, customer, is_enabled=True):
        '''
        this method will insert product 'name' from 'device' and for 'hardware'
        in the the database, but before it will check if 'name' already exists, if so
        it will trow a KeyError
        '''
        existing_products = self.get_products()
        if name in existing_products:
            raise KeyError(f"package '{name}' already exists")
        query = '''INSERT INTO products(name, device, hardware, quality, grade, grade_reference, type, customer, is_enabled) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        self.cur.execute(query, (name, device, hardware, quality, grade, grade_reference, type, customer, is_enabled))
        self.con.commit()
        self.database_changed.emit(TableId.Product())

    def update_product(self, name, device, hardware, quality, grade, grade_reference, type, customer):
        query = '''UPDATE products SET device = ?, hardware = ?, quality = ?, grade = ?, grade_reference = ?, type = ?, customer = ? WHERE name = ?'''
        self.cur.execute(query, (device, hardware, quality, grade, grade_reference, type, customer, name))
        self.con.commit()

    def get_products_info(self):
        query = '''SELECT name, hardware, device, grade, grade_reference, quality, type, customer, is_enabled FROM products'''
        self.cur.execute(query)
        retval = {}
        for row in self.cur.fetchall():
            retval[row[0]] = (row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])

        return retval

    def get_products(self):
        '''
        this method will return a list of all products
        '''
        query = '''SELECT name FROM products'''

        self.cur.execute(query)
        retval = []
        for row in self.cur.fetchall():
            retval.append(row[0])

        return retval

    def get_product(self, name):
        query = '''SELECT name, device, hardware, quality, grade, grade_reference, type, customer FROM products'''
        self.cur.execute(query)

        retval = {}
        for row in self.cur.fetchall():
            if row[0] == name:
                retval.update({'name': row[0], 'device': row[1], 'hardware': row[2], 'quality': row[3],
                               'grade': row[4], 'grade_reference': row[5], 'type': row[6], 'customer': row[7]})

        return retval

    def get_products_for_hardwares(self):
        '''
        this method will return a list of products for 'hardware_name'
        '''
        query = '''SELECT name FROM products'''
        self.cur.execute(query)
        retval = []
        for row in self.cur.fetchall():
            retval.append(row[0])
        return retval

    def get_product_device(self, name):
        get_blob_query = '''SELECT device FROM products WHERE name = ?'''
        self.cur.execute(get_blob_query, (name,))
        retval = []
        for row in self.cur.fetchall():
            retval.append(row[0])

        return retval

    def get_products_for_device(self, name):
        get_blob_query = '''SELECT name FROM products WHERE device = ?'''
        self.cur.execute(get_blob_query, (name,))
        retval = []
        for row in self.cur.fetchall():
            retval.append(row[0])

        return retval

    def get_product_hardware(self, name):
        get_blob_query = '''SELECT hardware FROM products WHERE name = ?'''
        self.cur.execute(get_blob_query, (name,))
        retval = []
        for row in self.cur.fetchall():
            retval.append(row[0])

        return retval

    def remove_product(self, name):
        query = '''DELETE FROM product WHERE name =`?'''
        self.cur.execute(query, (name,))
        self.con.commit()
        self.database_changed.emit(TableId.Product())

    def tests_get_info(self):
        '''
        this method will return a DICTIONARY with *ALL* existing tests as key,
        and as value the tuple (hardware, type, base, definition)
        '''
        retval = {}
        query = '''SELECT name, hardware, type, base, definition FROM tests'''
        self.cur.execute(query)
        for row in self.cur.fetchall():
            #        name   hardware    type    base     def
            retval[row[0]] = (row[1], row[2], row[3], row[4])
        return retval

    def tests_get_standard_tests(self, hardware, base):
        '''
        given 'hardware' and 'base', this method will return a LIST
        of all existing STANDARD TESTS.
        '''
        all_tests = self.tests_get_info()
        retval = []
        for test in all_tests:
            if (all_tests[test][0] == hardware) and (all_tests[test][2] == base):
                retval.append(test)

        return retval

    def add_standard_test(self, name, hardware, base):
        import runpy
        from ATE.org.coding.standard_tests import names as standard_test_names

        if name in standard_test_names:
            temp = runpy.run_path(standard_test_names[name])
            # TODO: fix this
            if not temp['dialog'](name, hardware, base):
                print(f"... no joy creating standard test '{name}'")
        else:
            raise Exception(f"{name} not a standard test ... WTF!")

    def add_custom_test(self, definition, is_enabled=True):
        '''This method adds a 'custom' test to the project.

        'definition' is a structure as follows:

            test_definition = {
                'name': 'trial',
                'type': 'custom', <-- needs to be 'custom' otherwhise explode
                'quality': 'automotive',
                'hardware': 'HW0',
                'base': 'FT',
                'doc_string': ['line1', 'line2'],
                'input_parameters': {
                    'Temperature':    {'Shmoo': True, 'Min': -40.0, 'Default': 25.0, 'Max': 170.0, '10ᵡ': '', 'Unit': '°C', 'fmt': '.0f'},
                    'new_parameter1': {'Shmoo': False, 'Min': -np.inf, 'Default': 0.0, 'Max': np.inf, '10ᵡ': 'μ', 'Unit':  'V', 'fmt': '.3f'},
                    'new_parameter2': {'Shmoo': False, 'Min': -np.inf, 'Default':  0.123456789, 'Max': np.inf, '10ᵡ':  '', 'Unit':  'dB', 'fmt': '.6f'}},
                'output_parameters' : {
                    'new_parameter1': {'LSL': -np.inf, 'LTL':  np.nan, 'Nom':  0.0, 'UTL': np.nan, 'USL': np.inf, '10ᵡ': '', 'Unit': '?', 'fmt': '.3f'},
                    'new_parameter2': {'LSL': -np.inf, 'LTL': -5000.0, 'Nom': 10.0, 'UTL':   15.0, 'USL': np.inf, '10ᵡ': '', 'Unit': '?', 'fmt': '.1f'},
                    'new_parameter3': {'LSL': -np.inf, 'LTL':  np.nan, 'Nom':  0.0, 'UTL': np.nan, 'USL': np.inf, '10ᵡ': '', 'Unit': '?', 'fmt': '.6f'},
                    'new_parameter4': {'LSL': -np.inf, 'LTL':  np.nan, 'Nom':  0.0, 'UTL': np.nan, 'USL': np.inf, '10ᵡ': '', 'Unit': '?', 'fmt': '.3f'}},
                'dependencies' : {}}
        '''

        name = definition['name']
        hardware = definition['hardware']
        base = definition['base']
        test_type = definition['type']

        if test_type != 'custom':
            raise Exception(f"not a 'custom' test!!!")

        # TODO: move this check to the wizard
        tests = self.get_tests_from_db(hardware, base)
        if name in tests:
            # use print as a hint until we fix this
            print('test exists already')
            return

        try:  # generate the test with everythin around it.
            from ATE.org.coding.generators import test_generator
            test_generator(self.project_directory, definition)
        except Exception as e:  # explode on fail
            print(f"failed to create test structure for {definition['hardware']}/{definition['base']}/{definition['name']}")
            raise e

        # add to database on pass
        query = '''INSERT INTO tests(name, hardware, base, type, definition, is_enabled) VALUES (?, ?, ?, ?, ?, ?)'''
        # TODO: hack is used, this must be refactored
        definition.pop('name')
        definition.pop('hardware')
        definition.pop('base')
        definition.pop('type')
        blob = pickle.dumps(definition, 4)

        self.cur.execute(query, (name, hardware, base, test_type, blob, is_enabled))
        self.con.commit()
        self.database_changed.emit(TableId.Test())

    def update_custom_test(self, name, hardware, base, type, definition, is_enabled=True):
        query = '''REPLACE INTO tests(name, hardware, base, type, definition, is_enabled) VALUES (?, ?, ?, ?, ?, ?)'''
        blob = pickle.dumps(definition, 4)

        self.cur.execute(query, (name, hardware, base, type, blob, is_enabled))
        self.con.commit()
        self.database_changed.emit(TableId.Test())

    def get_tests_from_files(self, hardware, base, test_type='all'):
        '''
        given hardware , base and type this method will return a dictionary
        of tests, and as value the absolute path to the tests.
        by searching the directory structure.
        type can be:
            'standard' --> standard tests
            'custom' --> custom tests
            'all' --> standard + custom tests
        '''
        retval = {}
        tests_directory = os.path.join(self.project_directory, 'src', 'tests', hardware, base)
        potential_tests = os.listdir(tests_directory)
        from ATE.org.actions_on.tests import standard_test_names

        for potential_test in potential_tests:
            if potential_test.upper().endswith('.PY'):  # ends with .PY, .py, .Py or .pY
                if '_' not in potential_test.upper().replace('.PY', ''):  # name doesn't contain an underscore
                    if '.' not in potential_test.upper().replace('.PY', ''):  # name doesn't contain extra dot(s)
                        if test_type == 'all':
                            retval[potential_test.split('.')[0]] = os.path.join(tests_directory, potential_test)
                        elif test_type == 'standard':
                            if '.'.join(potential_test.split('.')[0:-1]) in standard_test_names:
                                retval[potential_test.split('.')[0]] = os.path.join(tests_directory, potential_test)
                        elif test_type == 'custom':
                            if '.'.join(potential_test.split('.')[0:-1]) not in standard_test_names:
                                retval[potential_test.split('.')[0]] = os.path.join(tests_directory, potential_test)
                        else:
                            raise Exception('unknown test type !!!')
        return retval

    def get_test_definition(self, name):
        get_blob_query = '''SELECT hardware, type, base, definition FROM tests WHERE name = ?'''
        self.cur.execute(get_blob_query, (name,))
        definition = {}
        retval = self.cur.fetchone()
        definition['name'] = name
        definition['hardware'] = retval[0]
        definition['type'] = retval[1]
        definition['base'] = retval[2]
        in_out_param = pickle.loads(retval[3])
        definition['input_parameters'] = in_out_param['input_parameters']
        definition['output_parameters'] = in_out_param['output_parameters']
        definition['docstring'] = in_out_param['docstring']
        return definition

    def get_test_hardware(self, name):
        get_blob_query = '''SELECT hardware FROM tests WHERE name = ?'''
        self.cur.execute(get_blob_query, (name,))
        retval = []
        for row in self.cur.fetchall():
            retval.append(row[0])

        return retval

    def get_test_definiton(self, name):
        get_blob_query = '''SELECT definition FROM tests WHERE name = ?'''
        self.cur.execute(get_blob_query, (name,))
        definiton = self.cur.fetchone()

        return pickle.loads(definiton[0])

    def get_test_temp_limits(self, name):
        test = self.get_test_definition(name)
        temp = test['input_parameters']['Temperature']
        return int(temp['Min']), int(temp['Max'])

    def get_tests_from_db(self, hardware, base, test_type='all'):
        '''
        given hardware and base, this method will return a dictionary
        of tests, and as value the absolute path to the tests.
        by querying the database.
        type can be:
            'standard' --> standard tests
            'custom' --> custom tests
            'all' --> standard + custom tests
        '''
        if test_type == 'all':
            # query = '''SELECT name FROM tests WHERE hardware = ? AND base = ?'''
            # TODO: remove this until we set primary keys correctly
            query = '''SELECT name FROM tests WHERE base = ?'''
            self.cur.execute(query, (base,))
        elif test_type in ('standard', 'custom'):
            # query = '''SELECT name FROM tests WHERE hardware = ? AND base = ? AND type = ?'''
            # TODO: remove this until we set primary keys correctly
            query = '''SELECT name FROM tests WHERE base = ? AND type = ?'''
            self.cur.execute(query, (base, test_type))
        else:
            raise Exception('unknown test type !!!')

        retval = []
        for row in self.cur.fetchall():
            retval.append(row[0])

        return retval

    def remove_test(self, name):
        query = '''DELETE from tests WHERE name=?'''
        self.cur.execute(query, (name,))

        query = '''DELETE from sequence WHERE test=?'''
        self.cur.execute(query, (name,))
        self.con.commit()
        self.database_changed.emit(TableId.Test())

    def delete_test_from_program(self, test_name):
        query = '''DELETE from sequence WHERE test = ?'''
        self.cur.execute(query, (test_name,))
        self.con.commit()
        self.database_changed.emit(TableId.Test())

    def get_data_for_qualification_flow(self, quali_flow_type, product):
        query = '''SELECT * from qualification_flow_data where type = ? AND product = ?'''
        self.cur.execute(query, (quali_flow_type, product))
        retval = []
        for row in self.cur.fetchall():
            unpickleddata = pickle.loads(row[3])
            retval.append((row[0], row[1], row[2], unpickleddata))
        return retval

    def get_unique_data_for_qualifcation_flow(self, quali_flow_type, product):
        '''
            Returns one and only one instance of the data for a given quali_flow.
            Will throw if multiple instances are found in db.
            Will return a default item, if nothing exists.
        '''
        items = self.get_data_for_qualification_flow(quali_flow_type, product)
        if(len(items) == 0):
            return {"product": product}
        elif(len(items) == 1):
            return items[0][3]
        else:
            raise Exception("Multiple items for qualification flow, where only one is allowed")

    def add_or_update_qualification_flow_data(self, quali_flow_data):
        '''
            Inserts a given set of qualification flow data into the database,
            updating any already existing data with the same "name" field. Note
            that we expect a "type" field to be present.
        '''

        query = '''INSERT OR REPLACE INTO qualification_flow_data VALUES(?,?,?,?)'''
        blob = pickle.dumps(quali_flow_data, 4)
        self.cur.execute(query, (quali_flow_data["name"], quali_flow_data["type"], quali_flow_data["product"], blob))
        self.con.commit()
        self.database_changed.emit(TableId.Flow())

    def delete_qualifiaction_flow_instance(self, quali_flow_data):
        query = '''DELETE from qualification_flow_data WHERE name=? and type=? and product=?'''
        self.cur.execute(query, (quali_flow_data["name"], quali_flow_data["type"], quali_flow_data["product"]))
        self.con.commit()
        self.database_changed.emit(TableId.Flow())

    def insert_program(self, name, hardware, base, target, usertext, sequencer_typ, temperature, definition, owner_name, order):
        query = '''INSERT INTO programs (prog_name, owner_name, prog_order, hardware, base, target, usertext, sequencer_type, temperature) VALUES(?,?,?,?,?,?,?,?,?)'''
        self.cur.execute(query, (name, owner_name, order, hardware, base, target, usertext, sequencer_typ, pickle.dumps(temperature)))

        self._insert_sequence_informations(owner_name, name, definition)
        self.con.commit()
        self.database_changed.emit(TableId.Flow())

    def _insert_sequence_informations(self, owner_name, prog_name, definition):
        seq_query = '''INSERT INTO sequence(owner_name, prog_name, test, test_order, definition) VALUES (?, ?, ?, ?, ?)'''
        for index, test in enumerate(definition['sequence']):
            tuple_test = list(test.items())
            blob = pickle.dumps(tuple_test[0][1], 4)
            self.cur.execute(seq_query, (owner_name, prog_name, tuple_test[0][0], index, blob))

    def update_program(self, name, hardware, base, target, usertext, sequencer_typ, temperature, definition, owner_name):
        query = '''UPDATE programs set hardware=?, base=?, target=?, usertext=?, sequencer_type=?, temperature=? WHERE owner_name=? and prog_name=?'''
        self.cur.execute(query, (hardware, base, target, usertext, sequencer_typ, pickle.dumps(temperature), owner_name, name))

        self._delete_program_sequence(name, owner_name)

        self._insert_sequence_informations(owner_name, name, definition)
        self.con.commit()
        self.database_changed.emit(TableId.Flow())

    def _delete_program_sequence(self, prog_name, owner_name):
        seq_query = '''DELETE FROM sequence WHERE prog_name=? and owner_name=?'''
        self.cur.execute(seq_query, (prog_name, owner_name))
        self.con.commit()

    def _generate_program_name(self, program_name, index):
        prog_name = program_name[:-1]
        return prog_name + str(index)

    def delete_program(self, program_name, owner_name, program_order):
        query = '''DELETE from programs WHERE prog_name=? and owner_name=?'''
        self.cur.execute(query, (program_name, owner_name))

        del_seq_query = '''DELETE from sequence WHERE prog_name = ?'''
        self.cur.execute(del_seq_query, (program_name,))

        for index in range(program_order, self.get_program_owner_element_count(owner_name) + 1):
            query = '''UPDATE programs SET prog_order = ?, prog_name = ? where owner_name = ? and prog_order = ?'''
            new_name = self._generate_program_name(program_name, index)
            self.cur.execute(query, (index - 1, new_name, owner_name, index))

            query = '''UPDATE sequence SET prog_name = ? where owner_name = ? and prog_name = ?'''
            name = self._generate_program_name(program_name, index + 1)
            self.cur.execute(query, (new_name, owner_name, name))

        self.con.commit()
        self.database_changed.emit(TableId.Flow())

    def move_program(self, program_name, owner_name, program_order, is_up):
        query = '''SELECT prog_order, id from programs where prog_name = ? and owner_name = ?'''
        self.cur.execute(query, (program_name, owner_name))
        result = self.cur.fetchone()
        order = result[0]
        prog_id = result[1]

        count = self.get_program_owner_element_count(owner_name)
        if is_up:
            if order == 0:
                return
            prev = order - 1
        else:
            if order == count - 1:
                return
            prev = order + 1

        self._update_elements(program_name, owner_name, order, prev, prog_id)

        self.database_changed.emit(TableId.Flow())

    def _get_program_ids_from_sequence(self, prog_name, owner_name):
        ids = '''SELECT id from sequence where prog_name = ? and owner_name = ?'''
        prog_ids = []
        self.cur.execute(ids, (prog_name, owner_name))
        for id in self.cur.fetchall():
            prog_ids.append(id[0])

        return prog_ids

    def _update_program_name_for_sequence(self, new_prog_name, owner_name, ids):
        placeholders = ', '.join(str(x) for x in ids)
        prog_query = f'UPDATE sequence SET prog_name = ? where owner_name = ? and id in ({placeholders})'
        self.cur.execute(prog_query, (new_prog_name, owner_name))
        self.con.commit()

    def _update_sequnce(self, prog_name, new_prog_name, owner_name, prog_id):
        prog_ids = self._get_program_ids_from_sequence(prog_name, owner_name)
        new_prog_ids = self._get_program_ids_from_sequence(new_prog_name, owner_name)

        self._update_program_name_for_sequence(new_prog_name, owner_name, prog_ids)
        self._update_program_name_for_sequence(prog_name, owner_name, new_prog_ids)

        self.database_changed.emit(TableId.Flow())

    def _get_test_program_name(self, prog_order, owner_name):
        query = '''SELECT prog_name from programs where prog_order = ? and owner_name = ?'''
        self.cur.execute(query, (prog_order, owner_name))
        prog_name = self.cur.fetchone()[0]
        return prog_name

    def _update_test_program_name(self, prog_name, new_name):
        query = '''UPDATE programs SET prog_name = ? where prog_name = ?'''
        self.cur.execute(query, (new_name, prog_name))
        self.con.commit()

    def _update_elements(self, prog_name, owner_name, prev_order, order, id):
        neighbour = self._get_test_program_name(order, owner_name)
        self._update_sequnce(prog_name, neighbour, owner_name, id)

        self._update_program_order(owner_name, prev_order, order, neighbour)
        self._update_program_order_neighbour(owner_name, order, prev_order, prog_name, id)

    def _update_program_order_neighbour(self, owner_name, prev_order, order, new_name, id):
        query = '''UPDATE programs SET prog_order = ?, prog_name = ? where owner_name = ? and prog_order = ? and id != ?'''
        self.cur.execute(query, (order, new_name, owner_name, prev_order, id))
        self.con.commit()

    def _update_program_order(self, owner_name, prev_order, order, new_name):
        query = '''UPDATE programs SET prog_order = ?, prog_name = ? where owner_name = ? and prog_order = ?'''
        self.cur.execute(query, (order, new_name, owner_name, prev_order))
        self.con.commit()

    def get_program_owner_element_count(self, owner_name):
        query = '''SELECT COUNT (*) FROM programs where owner_name = ?'''
        self.cur.execute(query, (owner_name,))
        rowcount = self.cur.fetchone()[0]
        return rowcount

    def get_programs_for_owner(self, owner_name):
        query = '''SELECT prog_name from programs where owner_name = ? ORDER BY prog_order'''
        self.cur.execute(query, (owner_name,))
        retval = []
        for row in self.cur.fetchall():
            retval.append(row[0])

        return retval

    def get_program_configuration_for_owner(self, owner_name, prog_name):
        query = '''SELECT hardware, base, target, usertext, sequencer_type, temperature from programs where owner_name = ? and prog_name = ?'''
        self.cur.execute(query, (owner_name, prog_name))
        retval = {}
        row = self.cur.fetchone()
        retval.update({"hardware": row[0]})
        retval.update({"base": row[1]})
        retval.update({"target": row[2]})
        retval.update({"usertext": row[3]})
        retval.update({"sequencer_type": row[4]})
        retval.update({"temperature": ','.join(str(x) for x in pickle.loads(row[5]))})

        return retval

    def get_program_test_configuration(self, program, owner):
        query = '''SELECT test, test_order, definition FROM sequence WHERE prog_name=? and owner_name=?'''
        self.cur.execute(query, (program, owner))
        retval = []
        for row in self.cur.fetchall():
            tests = {}
            tests[row[0]] = pickle.loads(row[2])
            retval.insert(row[1], tests)

        return retval

    def get_tests_for_program(self, prog_name, owner_name):
        query = '''SELECT test from sequence where prog_name = ? and owner_name= ?'''
        self.cur.execute(query, (prog_name, owner_name))
        retval = []
        for row in self.cur.fetchall():
            retval.append(row[0])

        return retval

    def get_programs_for_node(self, type, name):
        query = "SELECT prog_name, owner_name from programs " f"WHERE {type} " f" = ?"
        self.cur.execute(query, (name,))
        retval = {}

        for row in self.cur.fetchall():
            if retval.get(row[1]) and row[0] in retval[row[1]]:
                continue

            retval.setdefault(row[1], []).append(row[0])

        return retval

    def get_programs_for_test(self, test_name):
        query = '''SELECT prog_name, owner_name from sequence WHERE test=?'''
        self.cur.execute(query, (test_name,))
        retval = {}

        for row in self.cur.fetchall():
            if retval.get(row[1]) and row[0] in retval[row[1]]:
                continue

            retval.setdefault(row[1], []).append(row[0])

        return retval

    def get_programs_for_hardware(self, hardware):
        query = '''SELECT prog_name, owner_name from programs WHERE hardware = ?'''
        self.cur.execute(query, (hardware,))
        retval = {}

        for row in self.cur.fetchall():
            retval.setdefault(row[1], []).append(row[0])

        return retval

    def get_available_testers(self):
        # TODO: implement once the pluggy stuff is in place.
        return ['SCT', 'CT']

    def get_available_instruments(self):
        # TODO: implement once the pluggy stuff is in place.
        return {'Keithley': ['K2000', 'K3000'],
                'Keysight': ['x', 'y', 'z']}

    def get_available_equipment(self):
        # TODO: implement once the pluggy stuff is in place.
        # what about handlers and probers ?
        # maybe best is to add them, and ignore them where not applicalbe ?!?
        # ... probably this function should ask the TCC what is available ...
        # needs some more thinking !
        return {'coildrivers': {
                'STL': ['DCS1K', 'DCS6K'],
                'TDK': ['SourceControl']},
                'thermostreamers': {
                'MPI': ['TA3000A'],
                'TempTronic': ['ATS710', 'XStream4300']}}

    def _get_dependant_objects_for_node(self, node, dependant_objects, node_type):
        tree = {}
        for definition in dependant_objects:
            query = f"SELECT * FROM {definition} WHERE {node_type} = ?"
            self.cur.execute(query, (node,))
            for row in self.cur.fetchall():
                if tree.get(definition) is None:
                    tree[definition] = [row[0]]
                else:
                    tree[definition].append(row[0])

        return tree

    def get_dependant_objects_for_hardware(self, hardware):
        dependant_objects = ['devices', 'dies', 'products', 'tests']
        node_type = 'hardware'

        programs = {'programs': self.get_programs_for_hardware(hardware)}
        objs = self._get_dependant_objects_for_node(hardware, dependant_objects, node_type)
        if not programs['programs']:
            return objs

        objs.update(programs)
        return objs

    def get_dependant_objects_for_maskset(self, maskset):
        dependant_objects = ['dies']
        node_type = 'maskset'

        return self._get_dependant_objects_for_node(maskset, dependant_objects, node_type)

    def get_dependant_objects_for_die(self, die):
        objs = {}
        deps = {'devices': []}
        devices = self.get_devices()
        for name in devices:
            definition = self.get_device_definition(name)['dies_in_package']
            if die in definition:
                deps['devices'].append(name)

        if deps['devices']:
            objs.update(deps)

        programs = {'programs': self.get_programs_for_node('target', die)}
        if programs['programs']:
            objs.update(programs)

        return objs

    def get_dependant_objects_for_package(self, package):
        deps = {'devices': []}
        devices = self.get_devices()
        for name in devices:
            definition = self.get_device_package(name)
            if package in definition:
                deps['devices'].append(name)

        if len(deps['devices']) == 0:
            return {}

        return deps

    def get_dependant_objects_for_device(self, device):
        deps = {'products': []}
        products = self.get_products()
        for name in products:
            product = self.get_products_for_device(device)
            deps['products'] = product

        if len(deps['products']) == 0:
            return {}

        return deps

    def get_dependant_objects_for_test(self, test):
        return self.get_programs_for_test(test)

    def _get_state(self, name, type):
        query = f"SELECT name, is_enabled FROM {type}"
        self.cur.execute(query,)
        for row in self.cur.fetchall():
            if row[0] == name:
                return row[1]

        return None

    def _update_state(self, update_query, name, state):
        self.cur.execute(update_query, (state, name))
        self.con.commit()

    def get_hardware_state(self, name):
        return self._get_state(name, 'hardwares')

    def update_hardware_state(self, name, state):
        update_query = "UPDATE hardwares SET is_enabled = ? WHERE name = ?"
        self._update_state(update_query, name, state)
        if not state:
            self.hardware_removed.emit(name)
        else:
            self.hardware_added.emit(name)

    def get_maskset_state(self, name):
        return self._get_state(name, 'masksets')

    def update_maskset_state(self, name, state):
        update_query = "UPDATE masksets SET is_enabled = ? WHERE name = ?"
        self._update_state(update_query, name, state)

    def get_die_state(self, name):
        return self._get_state(name, 'dies')

    def update_die_state(self, name, state):
        update_query = "UPDATE dies SET is_enabled = ? WHERE name = ?"
        self._update_state(update_query, name, state)
        self.update_target.emit()

    def get_package_state(self, name):
        return self._get_state(name, 'packages')

    def update_package_state(self, name, state):
        update_query = "UPDATE packages SET is_enabled = ? WHERE name = ?"
        self._update_state(update_query, name, state)

    def get_device_state(self, name):
        return self._get_state(name, 'devices')

    def update_device_state(self, name, state):
        update_query = "UPDATE devices SET is_enabled = ? WHERE name = ?"
        self._update_state(update_query, name, state)
        self.update_target.emit()

    def get_product_state(self, name):
        return self._get_state(name, 'products')

    def update_product_state(self, name, state):
        update_query = "UPDATE products SET is_enabled = ? WHERE name = ?"
        self._update_state(update_query, name, state)

    def get_test_state(self, name):
        return self._get_state(name, 'tests')

    def update_test_state(self, name, state):
        update_query = "UPDATE tests SET is_enabled = ? WHERE name = ?"
        self._update_state(update_query, name, state)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if not self.con:
            return

        self.con.close()

    def delete_item(self, type, name):
        query = f"DELETE from {type.strip()} " f"WHERE name = ?"
        self.cur.execute(query, (name,))
        self.con.commit()
        self.database_changed.emit(TableId.Definition())

    def last_project_setting(self):
        return os.path.join(self.project_directory, '.lastsettings')

    def _store_settings(self):
        import json
        settings = {'settings': {'hardware': self.active_hardware,
                                 'base': self.active_base,
                                 'target': self.active_target}
                    }

        with open(self.last_project_setting(), 'w') as f:
            json.dump(settings, f, indent=4)

    def load_project_settings(self):
        import json
        settings_path = self.last_project_setting()
        if not os.path.exists(settings_path):
            return '', '', ''

        with open(settings_path, 'r') as f:
            settings = json.load(f)
            settings = settings['settings']
            return settings['hardware'], settings['base'], settings['target']
