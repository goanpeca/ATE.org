#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 09:41:38 2020

@author: nerohmot
"""

import STDR

from utils import STDFError
from utils import __latest_STDF_version__


class BPS(STDR):
    """Begin Program Section Record
----------------------------

Function:
    Marks the beginning of a new program section (or sequencer) in the job plan.

Frequency:
    * Optional on each entry into the program segment.

Location:
    Anywhere after the PIR and before the PRR.
"""

    def __init__(self, version=None, endian=None, record=None):
        self. id = 'BPS'
        self.local_debug = False
        if version is None:
            self.version = __latest_STDF_version__
        else:
            self.version = version
            
        # implementation based on the version
        if version=='V4':
            self.info = self.__doc__
            # fmt: off
            self.fields = {
                'REC_LEN'  : {'#' :  0, 'Type' :  'U*2', 'Ref' : None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' : None, 'Note' : ''},
                'REC_TYP'  : {'#' :  1, 'Type' :  'U*1', 'Ref' : None, 'Value' :   20, 'Text' : 'Record type                           ', 'Missing' : None, 'Note' : ''},
                'REC_SUB'  : {'#' :  2, 'Type' :  'U*1', 'Ref' : None, 'Value' :   10, 'Text' : 'Record sub-type                       ', 'Missing' : None, 'Note' : ''},
                'SEQ_NAME' : {'#' :  3, 'Type' :  'C*n', 'Ref' : None, 'Value' : None, 'Text' : 'Sequence name                         ', 'Missing' :   '', 'Note' : ''}
            }
            # fmt: on
        else:
            raise STDFError("{self.id} object creation error: unsupported version '{self.version}'")
        self._default_init(endian, record)