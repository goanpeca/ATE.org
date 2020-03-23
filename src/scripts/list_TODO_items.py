# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 12:38:36 2020

@author: hoeren

this script runs over the whole 'src' directory structure to find (and list)
all '#TODO:' items in .py files.
"""
import os

if __name__ == '__main__':
    source_root = os.path.split(os.path.dirname(__file__))[0]
    for root, _, files in os.walk(source_root):
        for File in files:
            if File == 'list_TODO_items': 
                continue
            if File.upper().endswith('.PY'):
                report = {}
                with open(os.path.join(root, File), 'r') as fd:
                    try:
                        content = fd.readlines()
                    except:
                        print(f"something strange going on in file {os.path.join(root, File)}")
                        #TODO: probably there is a unicode thing inside, need to strip it out
                for line_nr, line_contents in enumerate(content):
                    if '#TODO:' in line_contents:
                        report[line_nr] = line_contents.split('#TODO:')[1].strip()
                if report != {}:
                    print(f"{os.path.join(root, File)} :")
                    for line_nr in report:
                        print(f"   {line_nr} : {report[line_nr]}")
                        
                    

