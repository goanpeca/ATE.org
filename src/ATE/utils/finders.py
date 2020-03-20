# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 14:15:04 2020

@author: hoeren
"""

class ATE_project_finder(object):
    
    def __init__(self, workspace_directory):
        self.__call__(workspace_directory)
    
    def __call__(self, workspace_directory):
        self.workspace_directory = workspace_directory
        
    def list_ATE_projects(self):
        '''
        this method will return a list of all ATE projects (in self.workspace_directory)
        '''
        return list(self.dict_ATE_projects())
    
    def dict_ATE_projects(self):
        '''
        this method will return a dictionary with as key the ATE project name 
        under self.workspace_directory, and value the absolute path of each project.
        it is guaranteed that the list has at least one element (even if this
        element is '')
        '''
        temp = {"" : None}
        return temp
