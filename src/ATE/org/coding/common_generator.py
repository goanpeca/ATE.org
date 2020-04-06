# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 11:37:36 2020

@author: hoeren
"""

import os
import getpass

from ATE.utils.DT import DT

def common_generatror(project_path, hardware, base):
    '''
    This function will generate the project's base "common.py" file from scratch,
    then the TE can add things to it.
    The idea is here that the whole tester initialization (and/or instruments
    initialization is done here), TCC initialization and so on is done here.
    each test includes this with "from src import common"
    '''
    pass

