# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 13:16:58 2019

@author: hoeren
"""

import os
import sqlite3
import pickle


class project_navigator(object):
    
    def __init__(self, project_directory):
        self.project_directory = project_directory
        if not os.path.exists(project_directory):
            # maybe just create the damn thing ?
            raise Exception("{project_directory} does not exist.")

        self.db_file = os.path.join(project_directory, os.path.split(project_directory)[-1]+'.sqlite3')
        if not os.path.exists(self.db_file):
            self.create_new_database()
        else:
            self.con = sqlite3.connect(self.db_file)
            self.cur = self.con.cursor()
    
    def create_new_project(self):
        pass
        

    
    def create_new_database(self):
        '''
        this method will create a new (and empty) database file.
        '''
        self.con = sqlite3.connect(self.db_file)
        self.cur = self.con.cursor()
        # devices
        self.cur.execute('''CREATE TABLE "devices" (
	                           "name"	TEXT NOT NULL UNIQUE,
	                           "package"	TEXT NOT NULL,
	                           "definition"	BLOB NOT NULL,

	                           PRIMARY KEY("name"),
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
                                  CHECK(base=='die' OR base=='product'),
	                           "target"	TEXT NOT NULL,
	                           "type"	TEXT NOT NULL,

 	                           PRIMARY KEY("name")
                            );''')
        self.con.commit()
        # hardware
        self.cur.execute('''CREATE TABLE "hardware" (
	                           "name"	INTEGER NOT NULL,
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
	                           "hardware"	INTEGER NOT NULL,

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
	                           "test_numbers"	BLOB NOT NULL,
	                           "relative_path"	TEXT NOT NULL,

 	                           PRIMARY KEY("name")
                            );''')
        self.con.commit()

    def add_hardware(self, definition):
        '''
        this method adds a hardware setup (defined in hw_data) and returns
        the hw_nr for this.
        '''
        existing_hw_nrs = self.get_hardware_names()
        if existing_hw_nrs == []:
            new_hw_nr = 1
        else:
            new_hw_nr = max(existing_hw_nrs)+1
        blob = pickle.dumps(definition, 4)
        insert_blob_query = '''INSERT INTO hardware(name, definition) VALUES (?, ?)'''
        self.cur.execute(insert_blob_query, (new_hw_nr, blob))
        self.con.commit()        
        return new_hw_nr
    
    def update_hardware(self, name, definition):
        '''
        this method will update hardware 'name' with 'definition'
        if name doesn't exist, a KeyError will be thrown
        '''
        existing_hardware = self.get_hardware_names()
        if name not in existing_hardware:
            raise KeyError
        blob = pickle.dumps(definition, 4)
        update_blob_query = '''UPDATE hardware SET definition = ? WHERE name = ?'''
        self.cur.execute(update_blob_query, (blob, name))
        self.con.commit()        

    def get_hardware_names(self):
        '''
        This method will return a list of all hardware names available
        '''
        self.cur.execute("SELECT name FROM hardware")
        retval = []
        for row in self.cur.fetchall():
            retval.append(row[0])
        return retval
                
    def get_hardware_definition(self, name):
        '''
        this method retreives the hwr_data for hwr_nr.
        if hwr_nr doesn't exist, an empty dictionary is returned
        '''
        get_blob_query = '''SELECT definition FROM hardware WHERE name = ?'''
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
        existing_masksets = self.get_masksets_names()
        if name in existing_masksets:
            raise KeyError(f"{name} already exists")
        insert_query = '''INSERT INTO maskset(name, definition) VALUES (?, ?)'''
        blob = pickle.dumps(definition, 4)
        self.cur.execute(insert_query, (name, blob))
        self.con.commit()        
    
    def update_maskset(self, name, definition):
        '''
        this method will update the definition of maskset 'name' to 'definition'
        '''
        existing_masksets = self.get_masksets_names()
        if name not in existing_masksets:
            raise KeyError
        blob = pickle.dumps(definition, 4)
        update_blob_query = '''UPDATE masksets SET definition = ? WHERE name = ?'''
        self.cur.execute(update_blob_query, (blob, name))
        self.con.commit()        

    def get_masksets_names(self):
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
        existing_masksets = self.get_masksets_names()
        if name not in existing_masksets:
            raise KeyError(f"maskset '{name}' doesn't exist")
        
        get_blob_query = '''SELECT definition FROM maskset WHERE name = ?'''
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
        existing_dies = self.get_dies_names()
        if name in existing_dies:
            raise KeyError(f"{name} already exists")

        existing_masksets = self.get_masksets_names()
        if maskset not in existing_masksets:
            raise KeyError(f"{maskset} doesn't exist")

        existing_hardware = self.get_hardware_names()
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
        existing_dies = self.get_dies_names()
        if name not in existing_dies:
            raise KeyError(f"{name} already exists")

        existing_masksets = self.get_masksets_names()
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
        existing_dies = self.get_dies_names()
        if name not in existing_dies:
            raise KeyError(f"die'{name}' doesn't exist")

        existing_hardware = self.get_hardware_names()
        if hardware not in existing_hardware:
            raise KeyError(f"hardware '{hardware}' doesn't exist")
    
        update_query = '''UPDATE dies SET hardware = ? WHERE name = ?'''
        self.cur.execute(update_query, (hardware, name))
        self.con.commit()        
    
    def get_dies_names(self):
        '''
        this method will return a list of existing dies.
        '''
        self.cur.execute("SELECT name FROM dies")
        retval = []
        for row in self.cur.fetchall():
            retval.append(row[0])
        return retval

    def get_die(self, name):
        '''
        this method returns a tuple (maskset, hardware) for die 'name'
        if name doesn't exist, a KeyError will be raised.
        '''
        existing_dies = self.get_dies_names()
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
        existing_packages = self.get_packages_names()
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
        existing_packages = self.get_packages_names()
        if name not in existing_packages:
            raise KeyError
        blob = pickle.dumps(definition, 4)
        update_query = '''UPDATE packages SET definition = ? WHERE name = ?'''
        self.cur.execute(update_query, (blob, name))
        self.con.commit()        
    
    def get_packages_names(self):
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
        existing_packages = self.get_packages_names()
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
    
    def add_device(self, name, package, definition):
        pass
    
    def update_device(self, name, package, definition):
        self.update_device_package(name, package)
        self.update_device_definition(name, definition)
    
    def update_device_package(self, name, package):
        pass
    
    def update_device_definition(self, name, definition):
        pass
    
    def get_devices_names(self):
        pass
    
    def get_device_package(self, name):
        pass
    
    def get_device_definition(self, name):
        pass
    
    def remove_device(self, name):
        pass
    
    
    
if __name__ == '__main__':
    project_directory = r'C:\Users\hoeren\Desktop\ATE.org\src\ATE\org\Templates'
    pdb = project_navigator(project_directory)

    brol = {1:1,"foo":"boe"}
    pdb.update_hardware(1, brol)

    for name in pdb.get_hardware_names():
        print(f"#{name}")
        print(pdb.get_hardware_definition(name))
