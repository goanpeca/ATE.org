# -*- coding: utf-8 -*-
"""
Created on Tuesday, May 12 2020 @ 20:15:47 (Q2 20202)
By tom

Do **NOT** change anything in this module, as it is automatically generated thus your changes **WILL** be lost in time!

If you have the need to add things, add it to 'trial.py' or 'common.py'

BTW : YOU SHOULD **NOT** BE READING THIS !!!
"""

import numpy as np
from ATE.org.coding.abc import testABC, ipBC, opBC
from ATE.data.descriptors import IPDescriptor, OPDescriptor


class trial_OP(opBC):
    """Class definition for the output parameters of trial."""

    new_parameter1 = OPDescriptor('new_parameter1')
    new_parameter2 = OPDescriptor('new_parameter2')
    new_parameter3 = OPDescriptor('new_parameter3')
    new_parameter4 = OPDescriptor('new_parameter4')

    def __init__(self):
        super().__init__()
        self._output_parameters = {
            'new_parameter1': {'LSL': -np.inf, 'LTL': np.nan, 'Nom': 0.0, 'UTL': np.nan, 'USL': np.inf, '10ᵡ': '', 'Unit': '?', 'fmt': '.3f'},
            'new_parameter2': {'LSL': -np.inf, 'LTL': -5000.0, 'Nom': 10.0, 'UTL': 15.0, 'USL': np.inf, '10ᵡ': '', 'Unit': '?', 'fmt': '.1f'},
            'new_parameter3': {'LSL': -np.inf, 'LTL': np.nan, 'Nom': 0.0, 'UTL': np.nan, 'USL': np.inf, '10ᵡ': '', 'Unit': '?', 'fmt': '.6f'},
            'new_parameter4': {'LSL': -np.inf, 'LTL': np.nan, 'Nom': 0.0, 'UTL': np.nan, 'USL': np.inf, '10ᵡ': '', 'Unit': '?', 'fmt': '.3f'}}
        self.__call__()


class trial_IP(ipBC):
    """Class definition for the input parameters of trial."""

    Temperature = IPDescriptor('Temperature')
    new_parameter1 = IPDescriptor('new_parameter1')
    new_parameter2 = IPDescriptor('new_parameter2')

    def __init__(self):
        super().__init__()
        self._input_parameters = {
            'Temperature': {'Shmoo': True, 'Min': -40.0, 'Default': 25.0, 'Max': 170.0, '10ᵡ': '', 'Unit': '°C', 'fmt': '.0f'},
            'new_parameter1': {'Shmoo': False, 'Min': -np.inf, 'Default': 0.0, 'Max': np.inf, '10ᵡ': 'μ', 'Unit': 'V', 'fmt': '.3f'},
            'new_parameter2': {'Shmoo': False, 'Min': -np.inf, 'Default': 0.123456789, 'Max': np.inf, '10ᵡ': '', 'Unit': 'dB', 'fmt': '.6f'}}
        self.__call__()


class trial_BC(testABC):
    '''Base class definition for trial'''

    hardware = 'HW0'
    base = 'FT'
    Type = 'custom'

    def __init__(self):
        super().__init__()
        self.ip = trial_IP()
        self.op = trial_OP()
