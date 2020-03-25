# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 11:56:05 2020

@author: hoeren

This module holds the code that generates:
    1) a test (class)
    2) a test program
based on the supplied info.
"""

import os
import getpass

from ATE.utils.DT import DT


def test_generator(project_path, name, hardware, Type, base, definition):
    '''
    This function will generate the actual python test based on the supplied info.
        - project_path : the absolute path to the project root
        - name : the test name
        - hardware : the hardware that the test is based on
        - Type : the type of test ('standard' or 'custom')
        - base : the base of the test ('FT' or 'PR')
        - definition : a dictionary as follows
                {'doc_string' : [], #list of lines
                 'input_parameters' : {},
                 'output_parameters' : {}}
    This function will return the RELATIVE path to the generated file upon 
    success, and '' upon fail

    If the target file already exists, then an Exception is raised, as this
    should not be possible!
    '''

    now = DT()
    user = getpass.getuser()
        
    rel_path_to_file = os.path.join('src', 'tests', hardware, base, f"{name}.py")
    print(f"rel_path_to_file = '{rel_path_to_file}'")
    abs_path_to_file = os.path.join(project_path, rel_path_to_file)
    print(f"abs_path_to_file = '{abs_path_to_file}'")
    
    if os.path.exists(abs_path_to_file):
        raise Exception("asked to generate a test that already exists ! should not be possible")

    with open(abs_path_to_file, 'w') as tf:
        # reference : https://stackoverflow.com/questions/41914739/how-do-i-activate-a-conda-env-in-a-subshell
        tf.write("#!/usr/bin/env conda run -n SCT python\n") 
        tf.write("# -*- coding: utf-8 -*-\n") # not sure if in python 3 this is still necessary, but just in case
        tf.write("'''\n")
        tf.write(f"Created on {now}\n\n")
        tf.write(f"@author: {user}\n")
        tf.write(f"\thardware = '{hardware}'\n")
        tf.write(f"\tBase = '{base}'\n")
        tf.write(f"\tType = '{Type}'\n")
        tf.write("'''\n\n")
        
        tf.write("import SCT\n")
        tf.write("from ATE.org.abc import testABC\n\n")
    
        tf.write(f"class {name}(testABC):\n")        
        if 'doc_sting' in definition:
            tf.write("\t'''\n")
            for line in definition['doc_string']:
                tf.write("\t{line}\n")
            tf.write("\t'''\n")
        tf.write("\tpass\n") # temporary
    
        tf.write("if __name__ == '__main__':\n")
        tf.write("\tpass")
    
    return rel_path_to_file

def program_generator():
    pass