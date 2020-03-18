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


def test_generator(project_path, test_name, hardware, base, definition):
    '''
    This function will generate the actual python test file and 
    return the RELATIVE path to this file
    '''
    relative_path = os.path.join('src', 'tests', hardware, base, "%s.py" % test_name)
    absolute_path = os.path.join(project_path, relative_path)
    now = DT()
    user = getpass.getuser()
    with open(absolute_path, 'w') as tf:
        tf.write("#!/usr/bin/env python\n") #TODO: conda activate & run ?!? ~ conda activate MiniSCT
        tf.write("# -*- coding: utf-8 -*-\n")
        tf.write("'''\n")
        tf.write(f"Created on {now}\n\n")
        tf.write(f"@author: {user}\n")
        tf.write("'''\n\n")
        
        tf.write("import SCT\n")
        tf.write("from ATE.org.Testing import testABC\n\n")
    
        tf.write(f"class {test_name}(testABC):\n")        
        if 'description' in definition:
            tf.write("\t'''\n")
            for line in definition['description']:
                tf.write("\t{line}\n")
            tf.write("\t'''\n")
        tf.write("\tpass\n")
    
        tf.write("if __name__ == '__main__':\n")
        tf.write("\tpass")
    
    return relative_path

def test_program_generator():
    pass