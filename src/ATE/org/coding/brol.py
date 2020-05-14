#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 07:53:07 2020

@author: tom
"""
import os
import shutil
import numpy as np
import generate

hardware_definition = {
    'hardware': 'HW0',
    'PCB': {},
    'tester': ('SCT', 'import stuff'),
    'instruments': {},
    'actuators': {}}

test_definition = {
    'name': 'trial',
    'type': 'custom',
    'hardware': 'HW0',
    'base': 'FT',
    'doc_string': ['line1', 'line2'],
    'input_parameters': {
        'Temperature':    {'Shmoo': True, 'Min': -40.0, 'Default': 25.0, 'Max': 170.0, '10ᵡ': '', 'Unit': '°C', 'fmt': '.0f'},
        'new_parameter1': {'Shmoo': False, 'Min': -np.inf, 'Default': 0.0, 'Max': np.inf, '10ᵡ': 'μ', 'Unit':  'V', 'fmt': '.3f'},
        'new_parameter2': {'Shmoo': False, 'Min': -np.inf, 'Default':  0.123456789, 'Max': np.inf, '10ᵡ':  '', 'Unit':  'dB', 'fmt': '.6f'}},
    'output_parameters' : {
        'new_parameter1': {'LSL': -np.inf, 'LTL':  np.nan, 'Nom':  0.0, 'UTL': np.nan, 'USL': np.inf, '10ᵡ': '', 'Unit': '?', 'fmt': '.3f'},
        'new_parameter2': {'LSL': -np.inf, 'LTL': -5000.0, 'Nom': 10.0, 'UTL':   15.0, 'USL': np.inf, '10ᵡ': '', 'Unit': '?', 'fmt': '.1f'},
        'new_parameter3': {'LSL': -np.inf, 'LTL':  np.nan, 'Nom':  0.0, 'UTL': np.nan, 'USL': np.inf, '10ᵡ': '', 'Unit': '?', 'fmt': '.6f'},
        'new_parameter4': {'LSL': -np.inf, 'LTL':  np.nan, 'Nom':  0.0, 'UTL': np.nan, 'USL': np.inf, '10ᵡ': '', 'Unit': '?', 'fmt': '.3f'}},
    'dependencies' : {}}

program_definition = {
    'hardware': 'HW0',
    'base': 'FT',
    'target': 'target',
    'USER_TXT': 'H2LHH',
    'MOD_COD': 'P',  # see STDF V4 definition page 19 --> needs further elaboration on the codes ! P = Production
    'FLOW_ID': '1',  # see STDF V4 definition page 19 --> needs further elaboration
    'sequencer': ('Fixed Temperature', -40.0, 1),
    'sequence': {
        'test1': {
            'call values': {
                'ipname1': 123.456,
                'ipname2': 789.012
            },
            'limits': {  # (LTL, UTL)
                'opname1': (1.1, 2.2),
                'opname2': (3.3, 4.4)
            }
        },
        'test2': {
            'call values': {
                'ipname1': 1.234,
                'ipname2': 5.678
            },
            'limits': {
                'opname1': (5.5, 6.6),
                'opname2': (7.7, 8.8)
            }
        }
    },
    'binning': {  # TODO: needs some more thinking !!!
        'test1': {   # (TSTNUM, SBIN, SBIN_GROUP)
            'opname1': (10, 10, 'test1/opname1 fail'),
            'opname2': (11, 11, 'test1/opname2 fail')
        },
        'test2': {
            'opname1': (12, 12, 'test2/opname1 fail'),
            'opname2': (13, 13, 'test2/opname2 fail')
        }
    },
    'pingpong': {
        'PR1.1': ((1,),),
        'PR15.1': ((1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15),),
        'PR15.3': ((1, 2, 3, 4, 5), (6, 7, 8, 9, 10), (11, 12, 13, 14, 15)),
        'PR15.15': ((1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,), (9,), (10,), (11,), (12,), (13,), (14,), (15,))
    },
    'execution': {
        'PR1': {
            'test1': 'PR1.1',
            'test2': 'PR1.1'
        },
        'PR15': {
            'test1': 'PR15.1',
            'test2': 'PR15.3'
        }
    }
}

project_name = 'TRIAL'
project_path = os.path.join(os.path.dirname(__file__), project_name)
if os.path.exists(project_path):
    shutil.rmtree(project_path)

generate.project(project_path)

# HW_generator(project_path, hardware_definition)

# test_generator(project_path, test_definition)
# test_definition['base'] = 'PR'
# test_generator(project_path, test_definition)
