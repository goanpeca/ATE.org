# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 14:22:59 2020

@author: hoeren
"""

class Spyder_project_finder(object):
    
    def __init__(self, workspace_directory):
        self.__call__(workspace_directory)
    
    def __call__(self, workspace_directory):
        self.workspace_directory = workspace_directory
        
    def list_Spyder_projects(self):
        '''
        this method will return a dictionary with as key the ATE project name 
        under self.workspace_directory, and value the absolute path of each project.
        '''
        pass
    
