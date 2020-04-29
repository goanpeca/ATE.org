# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 14:06:14 2020

@author: hoeren

This script assembles all TODO's and README's into a top level README.md
"""


import os

if __name__ == '__main__':
    source_root = os.path.split(os.path.dirname(__file__))[0]
    root_readme = os.path.join(source_root, 'README.md')
    items = {'TODO-Files' : [],
              'README-Files' : [],
              'TODO-Items' : []}
    
    for root, _, files in os.walk(source_root):
        for File in files:
            if File == 'TODO.md':
                items['TODO-Files'].append(os.path.join(root, File).replace(source_root+os.path.sep, ''))
            if File == 'README.md':
                items['README-Files'].append(os.path.join(root, File).replace(source_root+os.path.sep, ''))
            if File.upper().endswith('.PY'):
                with open(os.path.join(root, File), 'r') as fd:
                    try:
                        content = fd.readlines()
                    except:
                        print(f"something strange going on in file {os.path.join(root, File)}")
                        #TODO: probably there is a unicode thing inside, need to strip it out
                    items_in_file = {}
                    for line_nr, line_contents in enumerate(content):
                        if 'TODO:' in line_contents:
                            items_in_file[line_nr] = line_contents.split('TODO:')[1].strip()
                        if 'ToDo:' in line_contents:
                            items_in_file[line_nr] = line_contents.split('ToDo:')[1].strip()
                        if 'todo:' in line_contents:
                            items_in_file[line_nr] = line_contents.split('todo:')[1].strip()

                items['TODO-Items'].append((os.path.join(root, File).replace(source_root+os.path.sep, ''), items_in_file))

    if os.path.exists(root_readme):
        os.remove(root_readme)

    with open(root_readme, 'w') as fd:
        fd.write("TODO.md files :\n")
        for todo_file in items['TODO-Files']:
            fd.write(f"[{todo_file}]({todo_file})\n")
        
        
        
        
