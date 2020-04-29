# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 14:06:14 2020

@author: hoeren

This script assembles all TODO's and README's into a top level README.md
"""


import os

from ATE.utils.DT import DT

if __name__ == '__main__':
    source_root = os.path.split(os.path.dirname(__file__))[0]
    root_readme = os.path.join(source_root, 'README.md')
    items = {'TODO-Files' : [],
              'README-Files' : [],
              'TODO-Items' : [],
              'Strange-Files' : []}
    now = DT()

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
                        items['Strange-Files'].append(os.path.join(root, File).replace(source_root+os.path.sep, ''))
                    items_in_file = {}
                    for line_nr, line_contents in enumerate(content):
                        if 'TODO:' in line_contents:
                            items_in_file[line_nr] = line_contents.split('TODO:')[1].strip()
                        if 'ToDo:' in line_contents:
                            items_in_file[line_nr] = line_contents.split('ToDo:')[1].strip()
                        if 'todo:' in line_contents:
                            items_in_file[line_nr] = line_contents.split('todo:')[1].strip()
                if items_in_file != {}:
                    items['TODO-Items'].append((os.path.join(root, File).replace(source_root+os.path.sep, ''), items_in_file))

    if os.path.exists(root_readme):
        os.remove(root_readme)


    with open(root_readme, 'w') as fd:
        fd.write("# `TODO.md` files\n\n")
        for todo_file in items['TODO-Files']:
            File = todo_file.replace(os.path.sep, '/')
            fd.write(f"- [{File}]({File})\n")
        
        fd.write("\n# `README.md` files\n\n")
        for readme_file in items['README-Files']:
            File = readme_file.replace(os.path.sep, '/')
            if File == 'README.md':
                continue
            fd.write(f"- [{File}]({File})\n")
        
        fd.write("\n# `TODO` items\n\n")
        for code_file, itemdict in items['TODO-Items']:
            File = code_file.replace(os.path.sep, '/')
            fd.write(f"- [{File}]({File})\n\n")
            for line_nr in itemdict:
                fd.write(f"\t{line_nr} : [{itemdict[line_nr]}]({File}#L{line_nr+1})\n\n")
            
        fd.write("\n# Strange files\n\n")
        for code_file in items['Strange-Files']:
            File = code_file.replace(os.path.sep, '/')
            fd.write(f"- [{File}]({File})\n")
            
        fd.write('---\n')
        fd.write(f'auto generated on {now}')
        
        
