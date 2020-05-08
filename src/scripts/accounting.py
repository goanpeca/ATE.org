# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 09:23:31 2020

@author: hoeren

this script runs over the whole 'src' directory structure to count the lines
of actual code (non-empty lines)

"""

import os, sys

verbose = False
with_comments = False

if __name__ == '__main__':
    source_root = os.path.split(os.path.dirname(__file__))[0]
    summary = ['TTL']
    extensions = ['.PY', '.UI', '.JSON']
    modules = [i for i in os.listdir(source_root)]
    counts = {m:{e:(0,0) for e in extensions+summary} for m in modules}
   
    if verbose:
        print('verbose ', end='')
    print('Summary ', end='')
    if with_comments:
        print('counting also comment lines')
    else:
        print('disregarding comment lines')
    print('-'*100)
    
    for root, _, files in os.walk(source_root):
        Dir = os.path.split(root)[1]
        if Dir in ['__pycache__', '.pylint.d']:
            continue
        for File in files:
            file_path = os.path.join(root, File)
            rel_path = os.path.sep.join(file_path.replace(source_root, '').split(os.path.sep)[1:])
            module = rel_path.split(os.path.sep)[0]
            extension = ('.' + File.split(".")[-1]).upper()
            if extension in extensions:
                if verbose: 
                    print(f"{module}{os.path.sep}{rel_path} : ", end='')
                loc = 0
                with open(file_path, encoding="utf8") as fd:
                    for line in fd:
                        line = line.strip()
                        commentless_line = line.split('#')[0].strip()
                        if with_comments:
                            if len(line)>0:
                                loc+=1
                        else:
                            if len(commentless_line)>0:
                                loc+=1
                if verbose:
                    print(f"{loc} lines of code")
                file_count, line_count = counts[module][extension]
                file_count+=1
                line_count+=loc
                counts[module][extension]=(file_count, line_count)
                file_count, line_count = counts[module]['TTL']
                file_count+=1
                line_count+=loc
                counts[module]['TTL']= (file_count, line_count)
    if verbose:
        print('-'*100)
    total_line_count = 0
    total_file_count = 0
    for module in counts:
        print(f"Module '{module}' :")
        for extension in counts[module]:
            if extension not in extensions:
                continue
            print(f"   {counts[module][extension][0]:3} '{extension}'",
                  " files hold ",
                  f"{counts[module][extension][1]:,}",
                  " lines of code", end='')
            if counts[module][extension][0] != 0:
                average_line_count = counts[module][extension][1]/counts[module][extension][0]
                print(f", averaging {average_line_count:.1f} lines of code per file.")
            else:
                print()
            total_line_count+=counts[module][extension][1]
            total_file_count+=counts[module][extension][0]
    print("-"*100)
    print(f"Total file count = {total_file_count:,}")
    print(f"Total line count = {total_line_count:,}")
                        
            
        
        
