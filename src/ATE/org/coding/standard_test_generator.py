# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 11:37:54 2020

@author: hoeren
"""



def standard_test_generator(standard_test_name):
    from ATE.org.coding.standard_tests import names as standard_test_names
    
    if standard_test_name not in standard_test_names:
        print(f"unknown standard test '{standard_test_name}'")


