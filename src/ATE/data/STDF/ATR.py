#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 23 13:52:36 2020

@author: tom
"""

import STDR

from utils import STDFError
from utils import __latest_STDF_version__


class ATR(STDR):
    """Audit Trail Record (ATR)
------------------------

Function:
    Used to record any operation that alters the contents of the STDF file. The name of the
    program and all its parameters should be recorded in the ASCII field provided in this
    record. Typically, this record will be used to track filter programs that have been
    applied to the data.

Frequency:
    * Optional
    * One for each filter or other data transformation program applied to the STDF data.

Location:
    Between the File Attributes Record (FAR) and the Master Information Record (MIR).
    The filter program that writes the altered STDF file must write its ATR immediately
    after the FAR (and hence before any other ATRs that may be in the file). In this way,
    multiple ATRs will be in reverse chronological order.
"""

    def __init__(self, version=None, endian=None, record=None):
        self.id = 'ATR'
        self.local_debug = False
        if version is None:
            self.version = __latest_STDF_version__
        else:
            self.version = version

        # Implementation based on the Version
        if self.version == 'V4':
            self.info = self.__doc__
            # fmt: off
            self.fields = {
                'REC_LEN'  : {'#' :  0, 'Type' : 'U*2' , 'Ref' : None, 'Value' :   None, 'Text' : 'Bytes of data following header        ', 'Missing' : None, 'Note' : ''},
                'REC_TYP'  : {'#' :  1, 'Type' : 'U*1' , 'Ref' : None, 'Value' :      0, 'Text' : 'Record type                           ', 'Missing' : None, 'Note' : ''},
                'REC_SUB'  : {'#' :  2, 'Type' : 'U*1' , 'Ref' : None, 'Value' :     20, 'Text' : 'Record sub-type                       ', 'Missing' : None, 'Note' : ''},
                'MOD_TIM'  : {'#' :  3, 'Type' : 'U*4' , 'Ref' : None, 'Value' :   None, 'Text' : 'Date & time of STDF file modification ', 'Missing' :    0, 'Note' : ''},
                'CMD_LINE' : {'#' :  4, 'Type' : 'C*n' , 'Ref' : None, 'Value' :   None, 'Text' : 'Command line of program               ', 'Missing' :   '', 'Note' : ''}
            }
            # fmt: on
        else:
            raise STDFError(f"{self.id} object creation error: unsupported version '{self.version}'")
        self._default_init(endian, record)
