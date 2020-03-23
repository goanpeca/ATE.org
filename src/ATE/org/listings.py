'''
Created on Nov 20, 2019

@author: hoeren
'''
import os
import sqlite3

from ATE.org.Templates import project_structure
from ATE.org.validation import is_ATE_project

def dict_projects(workspace_path):
    '''
    given a workspace_path, create a list with projects as key, and their
    project_path as value
    '''
    retval = {}
    for directory in os.listdir(workspace_path):
        full_directory = os.path.join(workspace_path, directory)
        if os.path.isdir(full_directory):
            retval[directory] = full_directory
    return retval

def list_projects(workspace_path):
    '''
    given a workspace_path, extract a list of all projects
    '''
    return list(dict_projects(workspace_path))

def dict_ATE_projects(workspace_path):
    '''
    given a workspace_path, create a dictionary with all ATE projects as key,
    and the project_path as value.
    '''
    retval = {}
    all_projects = dict_projects(workspace_path)
    for candidate in all_projects:
        possible_ATE_project = all_projects[candidate]
        if is_ATE_project(possible_ATE_project):
            retval[candidate] = possible_ATE_project
    return retval

def list_ATE_projects(workspace_path):
    '''
    given a workspace_path, extract a list of all ATE projects
    '''
    return list(dict_ATE_projects(workspace_path))


def list_MiniSCTs():
    retval = ["Tom's MiniSCT", "Rudie's MiniSCT", "Achim's MiniSCT", "Siegfried's MiniSCT"]
    return retval

if __name__ == '__main__':
    homedir = os.path.expanduser("~")
    workspace_path = os.path.join(homedir, "__spyder_workspace__")    

    pd = dict_projects(workspace_path)
    pl = list_projects(workspace_path)
    ad = dict_ATE_projects(workspace_path)
    al = list_ATE_projects(workspace_path)
    
    for project in pl:
        if project in al:
            print(f"* {project} : {pd[project]}")
        else:
            print(f"  {project} : {pd[project]}")


