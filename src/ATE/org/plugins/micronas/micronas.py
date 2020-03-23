# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 14:43:05 2020

@author: hoeren
"""

from ATE.org.plugins import ATE_plugin

class Micronas(ATE_plugin):
    
    def __init__(self):
        super().__init__()
    
    def importMaskset(self):
        pass
    
    
if __name__ == '__main__':
    brol = Micronas()
    print(brol.company)
