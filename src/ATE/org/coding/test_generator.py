# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 11:37:12 2020

@author: hoeren
"""

import os
import getpass

from ATE.utils.DT import DT


def test_generator(project_path, name, hardware, base, definition, Type='custom'):
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
    domain = str(os.environ.get('USERDNSDOMAIN')) #TODO: maybe move this to 'company specific stuff' later on ?
    if domain == 'None':
        user_email = ''
    else:
        user_email = f"{user}@{domain}".lower()

    rel_path_to_file = os.path.join('src', 'tests', hardware, base, f"{name}.py")
    abs_path_to_file = os.path.join(project_path, rel_path_to_file)
    
    if os.path.exists(abs_path_to_file):
        raise Exception("asked to generate a test that already exists ! should not be possible")

    with open(abs_path_to_file, 'w') as tf:
        # reference : https://stackoverflow.com/questions/41914739/how-do-i-activate-a-conda-env-in-a-subshell
        tf.write("#!/usr/bin/env conda run -n ATE python\n") 
        tf.write("# -*- coding: utf-8 -*-\n") # not sure if in python 3 this is still necessary, but just in case
        tf.write("'''\n")
        tf.write(f"Created on {now}\n")
        tf.write(f"By @author: {user} ({user_email})\n")
        tf.write(f"\thardware = '{hardware}'\n")
        tf.write(f"\tBase = '{base}'\n")
        tf.write(f"\tType = '{Type}'\n")
        tf.write("'''\n\n")
        
        tf.write("import SCT\n")
        tf.write("from ATE.org.abc import testABC\n\n")
    
        tf.write(f"class {name}(testABC):\n")        
        if 'doc_string' in definition:
            tf.write("\t'''\n")
            for line in definition['doc_string']:
                tf.write("\t{line}\n")
            tf.write("\t'''\n")
        tf.write("\tpass\n") # temporary
    
        tf.write("if __name__ == '__main__':\n")
        tf.write("\tpass")
    
    return rel_path_to_file


def tippprint(fd, ip):
    '''
    Test Input Parameters Pretty PRINT
    
    This function will be given a file descriptor of an open test file, 
    and the input parameters (dictionary). 
    The function will print the dictionary nicely aligned to the file descriptor.
    '''
    pass

def toppprint(fd, op):
    '''
    Test Output Parameters Pretty PRINT
    
    same as tippprint but for output parameters to a test file.
    '''
    pass


