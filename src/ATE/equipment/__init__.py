# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 11:41:20 2020

@author: hoeren

This module holds the abstract base classes for :
    - probers
    - handlers
    - thermo streams
    - coil drivers
    - ...
"""

class ProberABC(object):
    pass

class HandlerABC(object):
    
    # getter & setter on the handler type
    # - pick and place / post singulation
    # - gravity / post singulation
    # - strip handler / pre-singulation
    # ...
    
    pass

class ThermoABC(object):
    pass

class CoildriverABC(object):
    pass








