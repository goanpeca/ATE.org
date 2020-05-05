# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 11:37:12 2020

@author: hoeren
"""

import os
import getpass

from ATE.utils.DT import DT


def generator(project_path, definition):
    '''
    This function will generate the actual python test based on the supplied info.
        - project_path : the absolute path to the project root
        - definition : a dictionary as follows
                {'name' : str, # holding the test name
                 'type' : str, # holding the strin 'custom' or 'standard'
                 'hardware' : str,
                 'base' : str,
                 'docstring' : [], # list of lines
                 'input_parameters' : {
                     'name' : {'Shmoo' : bool,
                               'Min' : float,
                               'Default' : float,
                               'Max' : float,
                               '10ᵡ' : str,
                               'Unit' : str,
                               'fmt' : str},
                     ...},
                 'output_parameters' : {
                     'name' : {'LSL': float,
                               'LTL': float,
                               'Nom': float,
                               'UTL': float,
                               'USL': float,
                               '10ᵡ': str,
                               'Unit': str,
                               'fmt': str},
                     ...},
                 'dependencies' : {'Name' : bool, # only one bool enabled, this indicates what test (name) is **IMMEDIATELY** before the current test, all others are somewhere before.
                                   ...}
                 }

    This function will return the RELATIVE path to the generated file upon
    success, and '' upon fail

    If the target file already exists, then an Exception is raised, as this
    should not be possible!
    '''
    print(definition)
    rel_path_to_file = os.path.join('src', definition['hardware'], definition['base'], f"{definition['name']}.py")
    abs_path_to_file = os.path.join(project_path, rel_path_to_file)
    abs_dir = os.path.dirname(abs_path_to_file)

    if not os.path.exists(abs_dir):
        os.makedirs(abs_dir)

    if os.path.exists(abs_path_to_file): # overwrite
        print("asked to generate a test that already exists ... hence 'overwrite'!") #TODO: implement
    else: # create new
        with open(abs_path_to_file, 'w') as tf:
            # reference : https://stackoverflow.com/questions/41914739/how-do-i-activate-a-conda-env-in-a-subshell
            tf.write("#!/usr/bin/env conda run -n ATE python\n")
            tf.write("# -*- coding: utf-8 -*-\n") # not sure if in python 3 this is still necessary, but just in case
            tf.write("from ATE.org.abc import testABC\n")
            tf.write("import .common\n\n")
        # class definition
            tf.write(f"class {definition['name']}(testABC):\n")
        # docstring
            if 'docstring' in definition:
                tf.write("\t'''\n")
                for line in definition['docstring']:
                    tf.write(f"\t{line}\n")
                tf.write("\t'''\n")
            tf.write("\n")
        # class variables
            tf.write(f"\thardware = '{definition['hardware']}'\n")
            tf.write(f"\tbase = '{definition['base']}'\n")
            tf.write(f"\tType = '{definition['type']}'\n\n")
            tippprint(tf, definition['input_parameters'])
            toppprint(tf, definition['output_parameters'])
        # do-function
            tf.write(f"\tdef do(ip, op):\n")
            tf.write(f"\t\tpass\n\n")
        # main
            tf.write("if __name__ == '__main__':\n")
            tf.write("\timport os\n")
            tf.write("\ttester = os.environ.get('TESTER')\n")
            tf.write("\ttester_mode = os.environ.get('TESTERMODE')\n")
            tf.write("\tif tester_mode == 'DIRECT':\n")
            tf.write("\t\tpass #TODO: implement\n")
            tf.write("\telse: # 'INTERACTIVE'\n")
            tf.write("\t\tfrom ATE.org import TestRunner\n")
            tf.write("\t\ttestRunner = TestRunner(__file__)\n")

    return rel_path_to_file


def tippprint(fd, ip):
    '''
    Test Input Parameters Pretty PRINT

    This function will be given a file descriptor of an open test file,
    and the input parameters (dictionary).
    The function will print the dictionary nicely aligned to the file descriptor.
    '''

    fd.write("\tinput_parameters = {\n")
    for name in ip:
        name_def = "{'a' : True, b : np.inf}"


        fd.write(f"\t\t{name} = {name_def}\n")

    fd.write("\n")

def toppprint(fd, op):
    '''
    Test Output Parameters Pretty PRINT

    same as tippprint but for output parameters to a test file.
    '''
    fd.write("\toutput_parameters = {\n")
    for name in op:
        fd.write(f"\t\t{name} = ''\n")
    fd.write("\n")

