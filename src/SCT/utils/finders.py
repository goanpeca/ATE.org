# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 14:14:34 2020

@author: hoeren
"""

class SCT_finder(object):
    '''
    this class finds Mini- and Maxi-SCT's via zeroconf (cfr : SBuoy)
    
    '''
    def __init__(self):
        pass
    
    def list_testers(self):
        return list(self.dict_testers())
    
    def dict_testers(self):
        temp = {"Tom's MiniSCT" : '10.32.48.52',
                "Achim's MiniSCT" : '10.32.48.60',
                "Sigi's MiniSCT" : '13.32.48.5'}
        return temp    


if __name__ == '__main__':
    finder = SCT_finder()
    print(finder.tester_list())     