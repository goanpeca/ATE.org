# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 14:03:24 2020

@author: hoeren

this script runs over the whole 'src' directory structure to find (and deletes)
the following directories :
    __pycache__
    .pylint.d

"""

import os
import shutil

if __name__ == '__main__':
    source_root = os.path.split(os.path.dirname(__file__))[0]
    for root, dirs, _ in os.walk(source_root):
        for Dir in dirs:
            if Dir in ['__pycache__', '.pylint.d']:
                pycache = os.path.join(root, Dir)
                print(f"Deleting '{pycache}' ...", end='')
                shutil.rmtree(pycache, ignore_errors=True)    
                print("Done.")
