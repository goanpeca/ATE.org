#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 11:18:26 2020

@author: tom
"""

import numpy as np


class IPDescriptor(object):
    """descriptor for all input parameters.

    This descriptor presumes that the 'instance' holds:
        - a class variable ._input_parameters
        - an object variable ._input_data
    """

    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        """Returns the parameter's value"""
        if 'value' not in instance._input_parameters[self.name]:
            instance._input_parameters[self.name]['value'] = instance._input_parameters[self.name]['Default']
        return instance._input_parameters[self.name]['value']

    def __set__(self, instance, value):
        """Sets the parameter's value according to 'Min' and 'Max."""
        if value > instance._input_parameters[self.name]['Max']:
            value = instance._input_parameters[self.name]['Max']
        if value < instance._input_parameters[self.name]['Min']:
            value = instance._input_parameters[self.name]['Min']
        instance._input_parameters[self.name]['value'] = value
        return value


class OPDescriptor(object):
    """descriptor for all output parameters.

    This descriptor resumes that the 'instance' holds:
        - a class variable ._output_parameters
        - an object variable ._input_data
    """

    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        """returns the parameter's value"""
        if 'value' not in instance._output_parameters[self.name]:
            instance._outut_parameters[self.name]['value'] = np.nan
        return instance._input_parameters[self.name]['value']

    def __set__(self, instance, owner, value):
        """sets the parameter's value"""
        if value > instance._output_parameters[self.name]['UTL']:
            value = instance._output_parameters[self.name]['UTL']
        if value < instance._output_parameters[self.name]['LTL']:
            value = instance._output_parameters[self.name]['LTL']
        instance._output_parameters[self.name]['value'] = value
        return value
