# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 14:08:04 2020

@author: hoeren
"""

import os
import sys
import sqlite3
import pickle
import shutil
from pathlib import Path as create_file

from PyQt5.QtCore import QObject, pyqtSignal

from ATE.org.constants import TableIds as TableId


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

    def __init__(self, project_directory, parent=None):
        super().__init__(parent)
        print(f"project_directory = {project_directory}")
        self.template_directory = os.path.join(os.path.dirname(__file__), 'Templates')
        self.project_directory = project_directory

        self.db_file = os.path.join(project_directory,
                                    os.path.split(project_directory)[-1] + '.sqlite3')

        if not os.path.exists(self.project_directory):  # brand new project, initialize it.
            self.create_project_structure()
            self.con = sqlite3.connect(self.db_file)
            self.cur = self.con.cursor()
            self.create_project_database()
        else:
            self.con = sqlite3.connect(self.db_file)
            self.cur = self.con.cursor()

        self.active_target = ''
        self.active_hardware = ''
        self.active_base = ''
        self.project_name = os.path.split(self.project_directory)[-1]

    def update_toolbar_elements(self, active_hardware, active_base, active_target):
        self.active_hardware = active_hardware
        self.active_base = active_base
        self.active_target = active_target
        self.toolbar_changed.emit(self.active_hardware, self.active_base, self.active_target)

    def update_active_hardware(self, hardware):
        self.active_hardware = hardware
        self.hardware_activated.emit(hardware)

    def create_project_structure(self):
        '''
        this method creates a new project (self.project_directroy must *not*
        exist yet, otherwhise an exception will be raised)
        '''
        # project root directory
        os.makedirs(self.project_directory)
        shutil.copyfile(os.path.join(self.template_directory, 'dunder_main.py'),
                        os.path.join(self.project_directory, '__main__.py'))
        create_file(os.path.join(self.project_directory, '__init__.py')).touch() # not sure if this one is needed ...
        shutil.copyfile(os.path.join(self.template_directory, 'dot_gitignore'),
                        os.path.join(self.project_directory, '.gitignore'))
        # setup.py ???
        # .pre-commit-config.yaml ???

        # spyder
        #TODO: once we are integrated in Spyder, we need to get the following
        #      stuff from Spyder, and no longer from the template directroy.
        pspyd = os.path.join(self.project_directory, '.spyproject')
        os.makedirs(pspyd)
        shutil.copyfile(os.path.join(self.template_directory, 'codestyle.ini'),
                        os.path.join(pspyd, 'codestyle.ini'))
        shutil.copyfile(os.path.join(self.template_directory, 'encoding.ini'),
                        os.path.join(pspyd, 'encoding.ini'))
        shutil.copyfile(os.path.join(self.template_directory, 'vcs.ini'),
                        os.path.join(pspyd, 'vcs.ini'))
        shutil.copyfile(os.path.join(self.template_directory, 'workspace.ini'),
                        os.path.join(pspyd, 'workspace.ini'))
        create_file(os.path.join(pspyd, 'ATE.config')).touch()

        os.makedirs(os.path.join(pspyd, 'config'))

        pspydefd = os.path.join(pspyd, 'defaults')
        os.makedirs(pspydefd)
        shutil.copyfile(os.path.join(self.template_directory, 'defaults-codestyle-0.2.0.ini'),
                        os.path.join(pspydefd, 'defaults-codestyle-0.2.0.ini'))
        shutil.copyfile(os.path.join(self.template_directory, 'defaults-encoding-0.2.0.ini'),
                        os.path.join(pspydefd, 'defaults-encoding-0.2.0.ini'))
        shutil.copyfile(os.path.join(self.template_directory, 'defaults-vcs-0.2.0.ini'),
                        os.path.join(pspydefd, 'defaults-vcs-0.2.0.ini'))
        shutil.copyfile(os.path.join(self.template_directory, 'defaults-workspace-0.2.0.ini'),
                        os.path.join(pspydefd, 'defaults-workspace-0.2.0.ini'))

        # documentation
        os.makedirs(os.path.join(self.project_directory, 'doc'))
        os.makedirs(os.path.join(self.project_directory, 'doc', 'standards'))
        os.makedirs(os.path.join(self.project_directory, 'doc', 'audit'))
        os.makedirs(os.path.join(self.project_directory, 'doc', 'export'))

        # sources
        psrcd = os.path.join(self.project_directory, 'src')
        os.makedirs(psrcd)
        create_file(os.path.join(psrcd, '__init__.py')).touch()

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
	                           "name"	TEXT NOT NULL,
	                           "base"	TEXT NOT NULL
                                  CHECK(base=='PR' OR base=='FT'),
	                           "target"	TEXT NOT NULL,
	                           "type"	TEXT NOT NULL,
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

	                          PRIMARY KEY("name")
                           );''')
        self.con.commit()
        # products
        self.cur.execute('''CREATE TABLE "products" (
	                           "name"	TEXT NOT NULL UNIQUE,
	                           "device"	TEXT NOT NULL,
	                           "hardware"	TEXT NOT NULL,
                               "is_enabled" BOOL,

	                           PRIMARY KEY("name"),
	                           FOREIGN KEY("device") REFERENCES "devices"("name"),
	                           FOREIGN KEY("hardware") REFERENCES "hardware"("name")
                            );''')
        self.con.commit()
        # programs
        self.cur.execute('''CREATE TABLE "programs" (
	                           "name"	TEXT NOT NULL,
	                           "hardware"	TEXT NOT NULL,
	                           "base"	TEXT NOT NULL
                                   CHECK(base=='PR' OR base=='FT'),
	                           "definition"	BLOB NOT NULL,
	                           "relative_path"	TEXT NOT NULL,
                               "is_enabled" BOOL,

 	                           PRIMARY KEY("name")
                            );''')
        self.con.commit()

        # program owers (i.e. the flows who got a given program assigned)
        self.cur.execute('''CREATE TABLE "program_owner" (
                            "id"	INTEGER PRIMARY KEY AUTOINCREMENT,
                            "prog_name"	TEXT NOT NULL,
                            "owner_name"	TEXT NOT NULL
                        );''')
        self.con.commit()

        # tests
        self.cur.execute('''CREATE TABLE "tests" (
	                           "name"	TEXT NOT NULL,
	                           "hardware"	TEXT NOT NULL,
	                           "type"	TEXT NOT NULL
                                  CHECK(type=='standard' OR type=='custom'),
	                           "base"	TEXT NOT NULL
                                  CHECK(base=='PR' OR base=='FT'),
	                           "definition"	BLOB NOT NULL,
	                           "relative_path"	TEXT NOT NULL,
                               "is_enabled" BOOL,

	                           PRIMARY KEY("name")
                            );''')
        self.con.commit()

    def add_hardware(self, definition, is_enabled=True):
        '''
        this method adds a hardware setup (defined in 'definition') and returns
        the name for this.
        '''
        new_hardware = self.get_next_hardware()
        blob = pickle.dumps(definition, 4)
        query = '''INSERT INTO hardwares(name, definition, is_enabled) VALUES (?, ?, ?)'''
        self.cur.execute(query, (new_hardware, blob, is_enabled))
        self.con.commit()
        # Attention, this might be dangerous in the long run
        # -> we might have to do this after the whole create file stuff.
        self.database_changed.emit(TableId.Hardware())

        os.makedirs(os.path.join(self.project_directory, 'src', new_hardware))

        os.makedirs(os.path.join(self.project_directory, 'src', new_hardware), exist_ok=True)
        create_file(os.path.join(self.project_directory, 'src', new_hardware, '__init__.py')).touch()

        os.makedirs(os.path.join(self.project_directory, 'src', new_hardware, 'FT'))
        create_file(os.path.join(self.project_directory, 'src', new_hardware, 'FT', '__init__.py')).touch()
        os.makedirs(os.path.join(self.project_directory, 'src', new_hardware, 'FT', 'patterns'))
        create_file(os.path.join(self.project_directory, 'src', new_hardware, 'FT', 'patterns', '__init__.py')).touch()
        os.makedirs(os.path.join(self.project_directory, 'src', new_hardware, 'FT', 'protocols'))
        create_file(os.path.join(self.project_directory, 'src', new_hardware, 'FT', 'protocols', '__init__.py')).touch()
        os.makedirs(os.path.join(self.project_directory, 'src', new_hardware, 'FT', 'states'))
        create_file(os.path.join(self.project_directory, 'src', new_hardware, 'FT', 'states', '__init__.py')).touch()

        os.makedirs(os.path.join(self.project_directory, 'src', new_hardware, 'PR'))
        create_file(os.path.join(self.project_directory, 'src', new_hardware, 'PR', '__init__.py')).touch()
        os.makedirs(os.path.join(self.project_directory, 'src', new_hardware, 'PR', 'patterns'))
        create_file(os.path.join(self.project_directory, 'src', new_hardware, 'PR', 'patterns', '__init__.py')).touch()
        os.makedirs(os.path.join(self.project_directory, 'src', new_hardware, 'PR', 'protocols'))
        create_file(os.path.join(self.project_directory, 'src', new_hardware, 'PR', 'protocols', '__init__.py')).touch()
        os.makedirs(os.path.join(self.project_directory, 'src', new_hardware, 'PR', 'states'))
        create_file(os.path.join(self.project_directory, 'src', new_hardware, 'PR', 'states', '__init__.py')).touch()

        #TODO: and the common.py in .../src/HWx/common.py --> comes from the wizard!!!

        self.hardware_added.emit(new_hardware)
        return new_hardware

    def update_hardware(self, name, definition):
        '''
        this method will update hardware 'name' with 'definition'
        if name doesn't exist, a KeyError will be thrown
        '''
        existing_hardware = self.get_hardwares()
        if name not in existing_hardware:
            raise KeyError
        blob = pickle.dumps(definition, 4)
        update_blob_query = '''UPDATE hardwares SET definition = ? WHERE name = ?'''
        self.cur.execute(update_blob_query, (blob, name))
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
        '''
        this method will remove the hardware refered to by 'name'
        --> we need something like 'trace_hardware(self, name)'
            to understand what the implications are!!!
        '''
        raise NotImplementedError

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
        '''
        this method will remove the maskset defined by 'name'

        --> we need something like 'trace_maskset(self, name)'
            to understand what the implications are !!!
        '''
        raise NotImplementedError

    def add_die(self, name, hardware, maskset, quality, grade, grade_reference, customer, is_enabled=True):
        '''
        this method will add die 'name' with the given attributes to the database.
        if 'maskset' or 'hardware' doesn't exist, a KeyError will be raised.
        Also if 'name' already exists, a KeyError will be raised.
        if grade is not 'A'..'I' (9 possibilities) then a ValueError is raised
        if grade is 'A' then grade_reference must be an empty string
        if grade is not 'A', then grade_reference can not be an empty string,
        and it must reference another (existing) die with grade 'A'!
        '''
        insert_query = '''INSERT INTO dies(name, hardware, maskset, quality, grade, grade_reference, customer, is_enabled) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
        self.cur.execute(insert_query, (name, hardware, maskset, quality, grade, grade_reference, customer, is_enabled))
        self.con.commit()
        self.database_changed.emit(TableId.Die())

    def update_die(self, name, hardware, maskset, grade, grade_reference, quality, customer, is_enabled=True):
        '''
        this method updates both maskset and hardware for die with 'name'
        '''
        update_query = '''UPDATE dies SET hardware = ?, maskset = ?, grade = ?, grade_reference = ?, quality = ?, customer = ?, is_enabled = ?  WHERE name = ?'''
        self.cur.execute(update_query, (hardware, maskset, grade, grade_reference, quality, customer, is_enabled, name))
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
        query = '''SELECT name, hardware, maskset, grade, grade_reference, quality, customer, is_enabled FROM dies'''
        self.cur.execute(query)
        retval = {}
        for row in self.cur.fetchall():
            retval[row[0]] = (row[1], row[2], row[3], row[4], row[5], row[6], row[7])

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
            if dies_info[die][0] == hardware and dies_info[die][6]:
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
        '''
        this method will removes the die defined by 'name'

        --> we need something like 'trace_die(self, name)'
            to understand what the implications are !!!
        '''
        raise NotImplementedError

# Packages

    def add_package(self, name, leads, is_enabled=True):
        '''
        this method will insert package 'name' and 'pleads' in the
        database, but prior it will check if 'name' already exists, if so
        it will trow a KeyError
        '''
        existing_packages = self.get_packages()
        if name in existing_packages:
            raise KeyError(f"package '{name}' already exists")
        query = '''INSERT INTO packages(name, leads, is_enabled) VALUES (?, ?, ?)'''
        self.cur.execute(query, (name, leads, is_enabled))
        self.con.commit()
        self.database_changed.emit(TableId.Package())

    def update_package(self, name, leads, is_enabled=True):
        update_query = '''UPDATE packages SET leads = ?, is_enabled = ? WHERE name = ?'''
        self.cur.execute(update_query, (leads, is_enabled, name))
        self.con.commit()

    def get_package(self, name):
        packages = self.get_packages_info()

        for key, package in packages.items():
            if key == name:
                return package

        return None

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
        existing_devices = self.get_devices()
        if name in existing_devices:
            raise KeyError(f"device '{name}' already exists")

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
        '''
        this method will remove the package defined by 'name'
        --> we need something like 'trace_package(self, name)'
            to understand what the implications are !!!
        '''
        raise NotImplementedError

    def add_product(self, name, device, hardware, is_enabled=True):
        '''
        this method will insert product 'name' from 'device' and for 'hardware'
        in the the database, but before it will check if 'name' already exists, if so
        it will trow a KeyError
        '''
        existing_products = self.get_products()
        if name in existing_products:
            raise KeyError(f"package '{name}' already exists")
        query = '''INSERT INTO products(name, device, hardware, is_enabled) VALUES (?, ?, ?, ?)'''
        self.cur.execute(query, (name, device, hardware, is_enabled))
        self.con.commit()
        self.database_changed.emit(TableId.Product())

    def update_product(self, name):
        pass

    def update_product_device(self, name, device):
        pass

    def update_product_hardware(self, name, hardware):
        pass

    # def update_product_flows(self, name, flows):
    #     pass

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
        query = '''SELECT name, device, hardware FROM products'''
        self.cur.execute(query)

        retval = {}
        for row in self.cur.fetchall():
            if row[0] == name:
                retval.update({'name': row[0], 'device': row[1], 'hardware': row[2]})

        return retval

    def get_products_for_hardware(self, hardware_name):
        '''
        this method will return a list of products for 'hardware_name'
        '''
        query = '''SELECT name FROM products WHERE hardware = ?'''
        self.cur.execute(query, (hardware_name,))
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
        pass

    def tests_get_info(self):
        '''
        this method will return a DICTIONARY with *ALL* existing tests as key,
        and as value the tuple (hardware, type, base, definition, relative_path)
        '''
        retval = {}
        query = '''SELECT name, hardware, type, base, definition, relative_path FROM tests'''
        self.cur.execute(query)
        for row in self.cur.fetchall():
            #        name   hardware    type    base     def  relpath
            retval[row[0]] = (row[1], row[2], row[3], row[4], row[5])
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

    def test_add(self, name, hardware, Type, base, definition):
        '''
        given a name, hardware, Type, base and definition, this method will
        create the test (.py) file at the right place (=test_file_path), it
        will add the test to the database, and return the relative path to
        test_file_path.

        If a failure of some kind arrises an exception is raised
        '''
        from ATE.org.coding import test_generator

        try:
            rel_path = test_generator(self.project_directory, name, hardware, Type, base, definition)
            query = '''INSERT INTO tests(name, hardware, type, base, definition, relative_path) VALUES (?, ?, ?, ?, ?, ?)'''
            blob = pickle.dumps(definition, 4)
            self.cur.execute(query, (name, hardware, Type, base, blob, rel_path))
            self.con.commit()
            self.database_changed.emit(TableId.Flow())
        except:
            raise
        else:
            return rel_path

    def standard_test_add(self, name, hardware, base):
        import runpy
        from ATE.org.coding.standard_tests import names as standard_test_names

        if name in standard_test_names:
            temp = runpy.run_path(standard_test_names[name])
            # TODO: fix this
            if not temp['dialog'](name, hardware, base):
                print(f"... no joy creating standard test '{name}'")
        else:
            raise Exception(f"{name} not a standard test ... WTF!")


    def add_test(self, name, hardware, base, test_type, definition, is_enabled=True):
        '''
        given the name, hardware, base and test_numbers for a test,
        create the test based on the supplied info and add the info to
        the database.
        '''
        from ATE.org.coding import test_generator

        relative_path = test_generator(self.project_directory, name, hardware, base, definition)
        query = '''INSERT INTO tests(name, hardware, base, type, definition, relative_path, is_enabled) VALUES (?, ?, ?, ?, ?, ?, ?)'''
        blob = pickle.dumps(definition, 4)
        self.cur.execute(query, (name, hardware, base, test_type, blob, relative_path, is_enabled))
        self.con.commit()
        self.database_changed.emit(TableId.Test())

    def update_test(self, name):
        pass

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
            if potential_test.upper().endswith('.PY'): # ends with .PY, .py, .Py or .pY
                if not '_' in potential_test.upper().replace('.PY', ''): # name doesn't contain an underscore
                    if not '.' in potential_test.upper().replace('.PY', ''): # name doesn't contain extra dot(s)
                        if test_type=='all':
                            retval[potential_test.split('.')[0]] = os.path.join(tests_directory, potential_test)
                        elif test_type=='standard':
                            if '.'.join(potential_test.split('.')[0:-1]) in standard_test_names:
                                retval[potential_test.split('.')[0]] = os.path.join(tests_directory, potential_test)
                        elif test_type=='custom':
                            if '.'.join(potential_test.split('.')[0:-1]) not in standard_test_names:
                                retval[potential_test.split('.')[0]] = os.path.join(tests_directory, potential_test)
                        else:
                            raise Exception('unknown test type !!!')
        return retval

    def get_test_hardware(self, name):
        get_blob_query = '''SELECT hardware FROM tests WHERE name = ?'''
        self.cur.execute(get_blob_query, (name,))
        retval = []
        for row in self.cur.fetchall():
            retval.append(row[0])

        return retval

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
        query = '''SELECT name, relative_path FROM tests WHERE hardware = ? AND base = ? AND type = ?'''
        if test_type == 'all':
            test_type = '*'
        elif test_type not in ['standard', 'custom']:
            raise Exception('unknown test type !!!')

        self.cur.execute(query, (hardware, base, test_type))
        retval = {}
        for row in self.cur.fetchall():
            retval[row[0]] = row[1]
        return retval

    def remove_test(self, name):
        query = '''DELETE from tests WHERE name=?'''
        self.cur.execute(query, (name,))
        self.con.commit()

    def trace_test(self, hardware, base, name):
        pass

    def add_program(self, name):
        pass

    def update_program(self, name):
        pass

    def remove_program(self, name):
        pass

    def get_states(self, hardware):
        pass

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

    def insert_program_owner(self, program_name, owner_name):
        query = '''INSERT INTO program_owner (prog_name, owner_name) VALUES(?,?)'''
        self.cur.execute(query, (program_name, owner_name))
        self.con.commit()
        self.database_changed.emit(TableId.Flow())

    def delete_program_owner(self, program_name, owner_name):
        query = '''DELETE from program_owner WHERE prog_name=? and owner_name=?'''
        self.cur.execute(query, (program_name, owner_name))
        self.con.commit()
        self.database_changed.emit(TableId.Flow())

    def get_programs_for_owner(self, owner_name):
        query = '''SELECT prog_name from program_owner where owner_name = ?'''
        self.cur.execute(query, (owner_name,))
        retval = []
        for row in self.cur.fetchall():
            retval.append((row[0]))
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
        dependant_objects = ['devices', 'dies', 'products', 'programs', 'tests']
        node_type = 'hardware'

        return self._get_dependant_objects_for_node(hardware, dependant_objects, node_type)

    def get_dependant_objects_for_maskset(self, maskset):
        dependant_objects = ['dies']
        node_type = 'maskset'

        return self._get_dependant_objects_for_node(maskset, dependant_objects, node_type)

    def get_dependant_objects_for_die(self, die):
        deps = {'devices': []}
        devices = self.get_devices()
        for name in devices:
            definition = self.get_device_definition(name)['dies_in_package']
            if die in definition:
                deps['devices'].append(name)

        if len(deps['devices']) == 0:
            return {}

        return deps

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
