# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 14:08:04 2020

@author: hoeren
"""

import os
import sqlite3
import pickle
import shutil
from pathlib import Path as create_file


class project_navigator(object):
    '''
    This class takes care of the project creation/navigation/evolution.
    '''
    
    def __init__(self, project_directory):
        self.template_directory = os.path.join(os.path.dirname(__file__), 'Templates')
        self.__call__(project_directory)
            
    def __call__(self, project_directory):
        
        print(f"project_directory = {project_directory}")
        
        if not isinstance(project_directory, str):
            self.project_directory = ''
        else:
            self.project_directory = project_directory
            
        if len(self.project_directory.split(os.path.sep)) >= 2:
            self.db_file = os.path.join(project_directory, os.path.split(project_directory)[-1]+'.sqlite3')
    
            if not os.path.exists(project_directory):
                self.create_project_structure()
            if not os.path.exists(self.db_file):
                self.create_project_database()
            self.con = sqlite3.connect(self.db_file)
            self.cur = self.con.cursor()
            print("navigator")
        else:
            self.db_file = None
            self.con = None
            self.cur = None
            print("no navigator")
    
    def create_project_structure(self):
        '''
        this method creates a new project (self.project_directroy must *not* 
        exist yet, otherwhise an exception will be raised)
        '''
        if len(self.project_directory.split(os.path.sep)) >= 2:
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
            os.makedirs(os.path.join(self.project_directory, 'doc', 'export', 'pdf'))
            os.makedirs(os.path.join(self.project_directory, 'doc', 'export', 'ppt'))
            os.makedirs(os.path.join(self.project_directory, 'doc', 'export', 'xls'))
            
            # sources
            psrcd = os.path.join(self.project_directory, 'src')
            os.makedirs(psrcd)
            create_file(os.path.join(psrcd, '__init__.py')).touch()
            os.makedirs(os.path.join(psrcd, 'patterns'))
            create_file(os.path.join(psrcd, 'patterns', '__init__.py')).touch()
            os.makedirs(os.path.join(psrcd, 'protocols'))
            create_file(os.path.join(psrcd, 'protocols', '__init__.py')).touch()
            os.makedirs(os.path.join(psrcd, 'states'))
            create_file(os.path.join(psrcd, 'states', '__init__.py')).touch()
            shutil.copyfile(os.path.join(self.template_directory, 'init_hardware.py'),
                            os.path.join(psrcd, 'states', 'init_hardware.py'))
            os.makedirs(os.path.join(psrcd, 'tests'))
            create_file(os.path.join(psrcd, 'tests', '__init__.py')).touch()
            os.makedirs(os.path.join(psrcd, 'programs'))
            create_file(os.path.join(psrcd, 'programs', '__init__.py')).touch()
    
    def create_project_database(self):
        '''
        this method will create a new (and empty) database file.
        '''
        
        self.con = sqlite3.connect(self.db_file)
        self.cur = self.con.cursor()
        # devices
        self.cur.execute('''CREATE TABLE "devices" (
	                           "name"	TEXT NOT NULL UNIQUE,
	                           "hardware"	TEXT NOT NULL,
	                           "package"	TEXT NOT NULL,
	                           "definition"	BLOB NOT NULL,

                               PRIMARY KEY("name"),
	                           FOREIGN KEY("hardware") REFERENCES "hardwares"("name"),
	                           FOREIGN KEY("package") REFERENCES "packages"("name")
                            );''')
        self.con.commit()
        # dies
        self.cur.execute('''CREATE TABLE "dies" (
	                           "name"	TEXT NOT NULL UNIQUE,
	                           "maskset"	TEXT NOT NULL,
	                           "hardware"	INTEGER NOT NULL,

	                           PRIMARY KEY("name"),
	                           FOREIGN KEY("maskset") REFERENCES "masksets"("name"),
	                           FOREIGN KEY("hardware") REFERENCES "hardware"("name")
                            );''')
        self.con.commit()
        # flows
        self.cur.execute('''CREATE TABLE "flows" (
	                           "name"	TEXT NOT NULL,
	                           "base"	TEXT NOT NULL 
                                  CHECK(base=='PR' OR base=='FT'),
	                           "target"	TEXT NOT NULL,
	                           "type"	TEXT NOT NULL,

 	                           PRIMARY KEY("name")
                            );''')
        self.con.commit()
        # hardwares
        self.cur.execute('''CREATE TABLE "hardwares" (
	                           "name"	TEXT NOT NULL UNIQUE,
	                           "definition"	BLOB NOT NULL,

	                           PRIMARY KEY("name")
                            );''')
        self.con.commit()
        # masksets
        self.cur.execute('''CREATE TABLE "masksets" (
	                           "name"	TEXT NOT NULL UNIQUE,
	                           "definition"	BLOB NOT NULL,

	                           PRIMARY KEY("name")
                            );''')
        self.con.commit()
        # packages
        self.cur.execute('''CREATE TABLE "packages" (
	                           "name"	TEXT NOT NULL UNIQUE,
	                           "definition"	BLOB NOT NULL,
                               
	                           PRIMARY KEY("name")
                            );''')
        self.con.commit()
        # products
        self.cur.execute('''CREATE TABLE "products" (
	                           "name"	TEXT NOT NULL UNIQUE,
	                           "device"	TEXT NOT NULL,
	                           "hardware"	TEXT NOT NULL,

	                           PRIMARY KEY("name"),
	                           FOREIGN KEY("device") REFERENCES "devices"("name"),
	                           FOREIGN KEY("hardware") REFERENCES "hardware"("name")
                            );''')
        self.con.commit()
        # programs  
        self.cur.execute('''CREATE TABLE "programs" (
	                           "name"	TEXT NOT NULL,
	                           "hardware"	INTEGER NOT NULL,
	                           "base"	TEXT NOT NULL 
                                  CHECK(base=='PR' OR base=='FT'),
	                           "relative_path"	TEXT NOT NULL,

                           	   PRIMARY KEY("name")
                            );''')
        self.con.commit()
        # tests  
        self.cur.execute('''CREATE TABLE "tests" (
	                           "name"	TEXT NOT NULL,
	                           "hardware"	INTEGER NOT NULL,
	                           "base"	TEXT NOT NULL 
                                  CHECK(base=='PR' OR base=='FT'),
	                           "definition"	BLOB NOT NULL,
	                           "relative_path"	TEXT NOT NULL,

 	                           PRIMARY KEY("name")
                            );''')
        self.con.commit()

    def add_hardware(self, definition):
        '''
        this method adds a hardware setup (defined in 'definition') and returns
        the name for this.
        '''
        new_hardware = self.get_next_hardware_name()
        blob = pickle.dumps(definition, 4)
        query = '''INSERT INTO hardwares(name, definition) VALUES (?, ?)'''
        self.cur.execute(query, (new_hardware, blob))
        self.con.commit()

        os.makedirs(os.path.join(self.project_directory, 'src', 'patterns', new_hardware))
        create_file(os.path.join(self.project_directory, 'src', 'patterns', new_hardware, '__init__.py')).touch()        

        os.makedirs(os.path.join(self.project_directory, 'src', 'programs', new_hardware))
        create_file(os.path.join(self.project_directory, 'src', 'programs', new_hardware, '__init__.py')).touch()        

        os.makedirs(os.path.join(self.project_directory, 'src', 'protocols', new_hardware))
        create_file(os.path.join(self.project_directory, 'src', 'protocols', new_hardware, '__init__.py')).touch()        

        os.makedirs(os.path.join(self.project_directory, 'src', 'states', new_hardware))
        create_file(os.path.join(self.project_directory, 'src', 'states', new_hardware, '__init__.py')).touch()        
        os.makedirs(os.path.join(self.project_directory, 'src', 'states', new_hardware, 'FT'))
        create_file(os.path.join(self.project_directory, 'src', 'states', new_hardware, 'FT', '__init__.py')).touch()
        os.makedirs(os.path.join(self.project_directory, 'src', 'states', new_hardware, 'PR'))
        create_file(os.path.join(self.project_directory, 'src', 'states', new_hardware, 'PR', '__init__.py')).touch()


        os.makedirs(os.path.join(self.project_directory, 'src', 'tests', new_hardware))
        create_file(os.path.join(self.project_directory, 'src', 'tests', new_hardware, '__init__.py')).touch()
        os.makedirs(os.path.join(self.project_directory, 'src', 'tests', new_hardware, 'FT'))
        create_file(os.path.join(self.project_directory, 'src', 'tests', new_hardware, 'FT', '__init__.py')).touch()
        os.makedirs(os.path.join(self.project_directory, 'src', 'tests', new_hardware, 'PR'))
        create_file(os.path.join(self.project_directory, 'src', 'tests', new_hardware, 'PR', '__init__.py')).touch()
        
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

    def get_hardwares(self):
        '''
        This method will return a list of all hardware names available
        '''
        self.cur.execute("SELECT name FROM hardwares")
        retval = []
        for row in self.cur.fetchall():
            retval.append(row[0])
        return retval
    
    def get_next_hardware_name(self):
        '''
        This method will determine the next available hardware name
        '''
        available_hardwares = self.get_hardwares()
        if len(available_hardwares)==0:
            return "HW1"
        else:
            available_hardwares_ = [int(i.replace('HW', '')) for i in available_hardwares]
            return "HW%d" % (max(available_hardwares_)+1)
                
    def get_latest_hardware_name(self):
        '''
        This method will determine the latest hardware name and return it
        '''
        available_hardwares = self.get_hardwares()
        if len(available_hardwares)==0:
            return ""
        else:
            print(f"available_hardwares = {available_hardwares}")
            available_hardwares_ = [int(i.replace('HW', '')) for i in available_hardwares]
            return "HW%d" % (max(available_hardwares_))
        
    def get_hardware_definition(self, name):
        '''
        this method retreives the hwr_data for hwr_nr.
        if hwr_nr doesn't exist, an empty dictionary is returned
        '''
        get_blob_query = '''SELECT definition FROM hardwares WHERE name = ?'''
        self.cur.execute(get_blob_query, (name,))
        return pickle.loads(self.cur.fetchone()[0])        

    def remove_hardware(self, name):
        '''
        this method will remove the hardware refered to by 'name'
        
        --> we need something like 'trace_hardware(self, name)'
            to understand what the implications are!!!
        '''
        raise NotImplementedError
        
    
    def add_maskset(self, name, definition):
        '''
        this method will insert maskset 'name' and 'definition' in the 
        database, but prior it will check if 'name' already exists, if so
        it will trow a KeyError
        '''
        existing_masksets = self.get_masksets()
        if name in existing_masksets:
            raise KeyError(f"{name} already exists")
        insert_query = '''INSERT INTO masksets(name, definition) VALUES (?, ?)'''
        blob = pickle.dumps(definition, 4)
        self.cur.execute(insert_query, (name, blob))
        self.con.commit()        
    
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

    def get_masksets(self):
        '''
        this method lists all available masksets
        '''
        self.cur.execute("SELECT name FROM masksets")
        retval = []
        for row in self.cur.fetchall():
            retval.append(row[0])
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

    def remove_maskset(self, name):
        '''
        this method will remove the maskset defined by 'name'
        
        --> we need something like 'trace_maskset(self, name)'
            to understand what the implications are !!!
        '''
        raise NotImplementedError
    
    def add_die(self, name, maskset, hardware):
        '''
        this method will add die 'name' with 'maskset' and 'hardware'
        to the database. if 'maskset' or 'hardware' doesn't exist, a
        KeyError will be raised. Also if 'name' already exists, a KeyError
        will be raised.
        '''
        existing_dies = self.get_dies()
        if name in existing_dies:
            raise KeyError(f"{name} already exists")

        existing_masksets = self.get_masksets()
        if maskset not in existing_masksets:
            raise KeyError(f"{maskset} doesn't exist")

        existing_hardware = self.get_hardwares()
        if hardware not in existing_hardware:
            raise KeyError(f"{hardware} doesn't exist")

        insert_query = '''INSERT INTO dies(name, maskset, hardware) VALUES (?, ?, ?)'''
        self.cur.execute(insert_query, (name, maskset, hardware))
        self.con.commit()        
    
    def update_die(self, name, maskset, hardware):
        '''
        this method updates both maskset and hardware for die with 'name'
        '''
        self.update_die_maskset(name, maskset)
        self.update_die_hardware(name, hardware)
    
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
    
    def get_dies(self):
        '''
        this method will return a list of existing dies.
        '''
        self.cur.execute("SELECT name FROM dies")
        retval = []
        for row in self.cur.fetchall():
            retval.append(row[0])
        return retval

    def get_dies_for_hardware(self, hardware_name):
        '''
        this method will return a list of all dies for hardware 'hardware_name'
        '''
        query = '''SELECT name FROM dies WHERE hardware = ?'''
        
        self.cur.execute(query, (hardware_name,))
        retval = []
        for row in self.cur.fetchall():
            retval.append(row[0])
        return retval
        
    def get_die(self, name):
        '''
        this method returns a tuple (maskset, hardware) for die 'name'
        if name doesn't exist, a KeyError will be raised.
        '''
        existing_dies = self.get_dies()
        if name not in existing_dies:
            raise KeyError(f"die'{name}' doesn't exist")
        
        select_query = '''SELECT maskset, hardware FROM dies WHERE name=?'''
        self.cur.execute(select_query, (name,))
        temp = self.cur.fetchone()
        return temp[0], temp[1]
    
    def get_die_maskset(self, name):
        '''
        this method returns the maskset of die 'name'
        '''
        return self.get_die(name)[0]
    
    def get_die_hardware(self, name):
        '''
        this method returns the hardware of die 'name'
        '''
        return self.get_die(name)[1]
    
    def remove_die(self, name):
        '''
        this method will removes the die defined by 'name'
        
        --> we need something like 'trace_die(self, name)'
            to understand what the implications are !!!
        '''
        raise NotImplementedError
    
    def add_package(self, name, definition):
        '''
        this method will insert package 'name' and 'definition' in the 
        database, but prior it will check if 'name' already exists, if so
        it will trow a KeyError
        '''
        existing_packages = self.get_packages()
        if name in existing_packages:
            raise KeyError(f"package '{name}' already exists")
        insert_query = '''INSERT INTO packages(name, definition) VALUES (?, ?)'''
        blob = pickle.dumps(definition, 4)
        self.cur.execute(insert_query, (name, blob))
        self.con.commit()        

    def update_package(self, name, definition):
        '''
        this method will update the definition of package 'name' to 'definition'
        '''
        existing_packages = self.get_packages()
        if name not in existing_packages:
            raise KeyError
        blob = pickle.dumps(definition, 4)
        update_query = '''UPDATE packages SET definition = ? WHERE name = ?'''
        self.cur.execute(update_query, (blob, name))
        self.con.commit()        
    
    def get_packages(self):
        '''
        this method lists all available packages
        '''
        self.cur.execute("SELECT name FROM packages")
        retval = []
        for row in self.cur.fetchall():
            retval.append(row[0])
        return retval
    
    def get_package_definition(self, name):
        '''
        this method will return the definition of package 'name'
        '''
        existing_packages = self.get_packages()
        if name not in existing_packages:
            raise KeyError(f"package '{name}' doesn't exist")
        
        get_blob_query = '''SELECT definition FROM packages WHERE name = ?'''
        self.cur.execute(get_blob_query, (name,))
        return pickle.loads(self.cur.fetchone()[0])         
    
    def remove_package(self, name):
        '''
        this method will remove the package defined by 'name'
        
        --> we need something like 'trace_package(self, name)'
            to understand what the implications are !!!
        '''
        raise NotImplementedError
    
    def add_device(self, name, hardware, package, definition):
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

        insert_query = '''INSERT INTO devices(name, hardware, package, definition) VALUES (?, ?, ?, ?)'''
        blob = pickle.dumps(definition, 4)
        self.cur.execute(insert_query, (name, hardware, package, blob))
        self.con.commit()
    
    def update_device(self, name, package, definition):
        self.update_device_package(name, package)
        self.update_device_definition(name, definition)
    
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
        query = '''SELECT name FROM devices WHERE hardware = ?'''
        
        self.cur.execute(query, (hardware_name,))
        retval = []
        for row in self.cur.fetchall():
            retval.append(row[0])
        return retval
        
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

    def add_product(self, name, device, hardware):
        '''
        this method will insert product 'name' from 'device' and for 'hardware'
        in the the database, but before it will check if 'name' already exists, if so
        it will trow a KeyError
        '''
        existing_products = self.get_products()
        if name in existing_products:
            raise KeyError(f"package '{name}' already exists")
        query = '''INSERT INTO products(name, device, hardware) VALUES (?, ?, ?)'''
        self.cur.execute(query, (name, device, hardware))
        self.con.commit()        
    
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
        pass
    
    def get_product_hardware(self, name):
        pass
    
    def remove_product(self, name):
        pass


        
        
        
    
    def add_test(self, name, hardware, base, definition):
        '''
        given the name, hardware, base and test_numbers for a test, 
        create the test based on the supplied info and add the info to 
        the database.
        '''
        from ATE.org.coding import test_generator
        
        relative_path = test_generator(self.project_directory, name, hardware, base, definition)
        query = '''INSERT INTO tests(name, hardware, base, definition, relative_path) VALUES (?, ?, ?, ?, ?)'''
        blob = pickle.dumps(definition, 4)
        self.cur.execute(query, (name, hardware, base, blob, relative_path))
        self.con.commit() 

    def update_test(self, name):
        pass
    
    def get_tests_from_files(self, hardware, base):
        '''
        given hardware and base, this method will return a dictionary
        of tests, and as value the absolute path to the tests.
        by searching the directory structure.
        '''
        retval = {}
        tests_directory = os.path.join(self.project_directory, 'src', 'tests', hardware, base)
        potential_tests = os.listdir(tests_directory)
        for potential_test in potential_tests:
            if potential_test.upper().endswith('.PY'): # ends with .PY, .py, .Py or .pY
                if not '_' in potential_test.upper().replace('.PY', ''): # name doesn't contain an underscore
                    if not '.' in potential_test.upper().replace('.PY', ''): # name doesn't contain extra dot(s)
                        retval['.'.join(potential_test.split('.')[0:-1])] = os.path.join(tests_directory, potential_test)
        return retval
    
    def get_tests_from_db(self, hardware, base):
        '''
        given hardware and base, this method will return a dictionary
        of tests, and as value the absolute path to the tests.
        by querying the database.
        '''
        query = '''SELECT name, relative_path FROM tests WHERE hardware = ? AND base = ?'''
        self.cur.execute(query, (hardware, base))
        retval = {}
        for row in self.cur.fetchall():
            retval[row[0]]=row[1]
        return retval
    
    def remove_test(self, name):
        pass
    
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
    
    
    
if __name__ == '__main__':
    project_test_directory = os.path.join(os.path.dirname(__file__), 'test')
    navigator = project_navigator(project_test_directory)

    navigator.add_hardware({1:1,"foo":"boe"})

    for name in navigator.get_hardwares():
        print(f"HWR#{name}")
        print(navigator.get_hardware_definition(name))
