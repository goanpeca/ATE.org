#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  9 09:14:27 2020

@author: tom

references:
    - https://docs.python.org/3/howto/descriptor.html
    - https://docs.python.org/3/reference/datamodel.html
    - https://rszalski.github.io/magicmethods/
"""

import numpy as np
import inspect
from ATE.data.STDF.records import PTR

class IPDescriptor(object):
    """descriptor for all input parameters."""

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


class IPBC(object):

    def keys(self, parameter=None):
        """a List of all descriptors."""
        if parameter is None:
            return list(self._input_parameters)
        elif parameter in self._input_parameters:
            return list(self._input_parameters[parameter])
        else:
            return []


class OPDescriptor(object):
    """descriptor for all output parameters."""

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


class OPBC(object):
    """ Output Parameters Base Class.

    It presumes that the child of this class **CLASS VARIABLEs** defined as follows:

    _output_parameters = {
        'new_parameter1': {'LSL': -np.inf, 'LTL':  np.nan, 'Nom':  0.0, 'UTL': np.nan, 'USL': np.inf, '10ᵡ': '', 'Unit': '?', 'fmt': '.3f'},
        'new_parameter2': {'LSL': -np.inf, 'LTL': -5000.0, 'Nom': 10.0, 'UTL':   15.0, 'USL': np.inf, '10ᵡ': '', 'Unit': '?', 'fmt': '.1f'},
        'new_parameter3': {'LSL': -np.inf, 'LTL':  np.nan, 'Nom':  0.0, 'UTL': np.nan, 'USL': np.inf, '10ᵡ': '', 'Unit': '?', 'fmt': '.6f'},
        'new_parameter4': {'LSL': -np.inf, 'LTL':  np.nan, 'Nom':  0.0, 'UTL': np.nan, 'USL': np.inf, '10ᵡ': '', 'Unit': '?', 'fmt': '.3f'}}

    new_parameter1 = OPDescriptor('new_parameter1')
    new_parameter2 = OPDescriptor('new_parameter2')
    new_parameter3 = OPDescriptor('new_parameter3')
    new_parameter4 = OPDescriptor('new_parameter4')

    """

    def __init__(self):
        for parameter in self._output_parameters:
            if np.isnan(self._output_parameters[parameter]['LTL']):
                self._output_parameters[parameter]['LTL'] = self._output_parameters[parameter]['LSL']
            if np.isnan(self._output_parameters[parameter]['UTL']):
                self._output_parameters[parameter]['UTL'] = self._output_parameters[parameter]['USL']
            if 'value' not in self._output_parameters[parameter]:
                self._output_parameters[parameter]['value'] = np.nan
            if 'STDF' not in self._output_parameters[parameter]:
                obj = PTR()
                obj.set_value('TEST_TXT', )
                # TODO: fill in the PTR correctly
                self._output_parameters[parameter]['STDF'] = obj

    def clear(self):
        """clears the data from a previous run"""
        for parameter in self._output_parameters:
            self._output_parameters[parameter]['STDF'].set_value('RESULT', np.nan)


    def __bytes__(self):
        """creates a byte array of all prameters."""
        # TODO: go back to the STDF records, and do the following:
        #    __str__ is creating a human readable output string (unicoded!)
        #    __repr__ is creating a string (unicoded) that holds the statement that re-creates the object
        #    __bytes__ is creating the binary encoded record --> new in Python 3





class OP(OPBC):
    pass


class IP(IPBC):

    _input_parameters = {
        'Temperature':    {'Shmoo':  True, 'Min':   -40.0, 'Default': 25.0, 'Max':  170.0, '10ᵡ':  '', 'Unit': '°C', 'fmt': '.0f'},
        'new_parameter1': {'Shmoo': False, 'Min': -np.inf, 'Default':  0.0, 'Max': np.inf, '10ᵡ': 'μ', 'Unit':  'V', 'fmt': '.3f'},
        'new_parameter2': {'Shmoo': False, 'Min': -np.inf, 'Default':  0.0, 'Max': np.inf, '10ᵡ':  '', 'Unit':  'dB', 'fmt': '.6f'}}

    Temperature = IPDescriptor('Temperature')
    new_parameter1 = IPDescriptor('new_parameter1')
    new_parameter2 = IPDescriptor('new_parameter2')

    def __init__(self):
        pass


if __name__ == '__main__':
    input_parameters = {
        'Temperature':    {'Shmoo':  True, 'Min':   -40.0, 'Default': 25.0, 'Max':  170.0, '10ᵡ':  '', 'Unit': '°C', 'fmt': '.0f'},
        'new_parameter1': {'Shmoo': False, 'Min': -np.inf, 'Default':  0.0, 'Max': np.inf, '10ᵡ': 'μ', 'Unit':  'V', 'fmt': '.3f'},
        'new_parameter2': {'Shmoo': False, 'Min': -np.inf, 'Default':  0.0, 'Max': np.inf, '10ᵡ':  '', 'Unit':  'dB', 'fmt': '.6f'}}

    output_parameters = {
        'new_parameter1': {'LSL': -np.inf, 'LTL':  np.nan, 'Nom':  0.0, 'UTL': np.nan, 'USL': np.inf, '10ᵡ': '', 'Unit': '?', 'fmt': '.3f'},
        'new_parameter2': {'LSL': -np.inf, 'LTL': -5000.0, 'Nom': 10.0, 'UTL':   15.0, 'USL': np.inf, '10ᵡ': '', 'Unit': '?', 'fmt': '.1f'},
        'new_parameter3': {'LSL': -np.inf, 'LTL':  np.nan, 'Nom':  0.0, 'UTL': np.nan, 'USL': np.inf, '10ᵡ': '', 'Unit': '?', 'fmt': '.6f'},
        'new_parameter4': {'LSL': -np.inf, 'LTL':  np.nan, 'Nom':  0.0, 'UTL': np.nan, 'USL': np.inf, '10ᵡ': '', 'Unit': '?', 'fmt': '.3f'}}

    ip = IP()
    print(ip.Temperature)
    ip.Temperature = 0
    print(ip.Temperature)
    ip.keys()
