# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 12:14:36 2020

@author: hoeren

this script runs over the whole 'src' directory structure to find (and list)
all 'TODO.md' files.

"""
import os

if __name__ == '__main__':
    source_root = os.path.split(os.path.dirname(__file__))[0]
    for root, _, files in os.walk(source_root):
        for File in files:
            if File == 'TODO.md' or File == 'README.md':
                print(f"{os.path.join(root, File)}")
