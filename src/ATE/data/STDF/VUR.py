#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 23 14:07:48 2020

@author: tom
"""

import STDR

from utils import STDFError
from utils import __latest_STDF_version__


class VUR(STDR):
    """Version Update Record (VUR)
---------------------------

Function:
    Version update Record is used to identify the updates over version V4.
    Presence of this record indicates that the file may contain records defined by the new standard.

Frequency:
    * One for each extension to STDF V4 used.

Location:
    Just before the MIR
"""

    def __init__(self, version=None, endian=None, record=None):
        self.id = 'VUR'
        self.local_debug = False
        if version is None:
            self.version = __latest_STDF_version__
        else:
            self.version = version

        # implementation base on the version
        if self.version == 'V4':
            self.info = self.__doc__
            # fmt: off
            self.fields = {
                'REC_LEN'  : {'#' : 0, 'Type' : 'U*2', 'Ref' : None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' : None},
                'REC_TYP'  : {'#' : 1, 'Type' : 'U*1', 'Ref' : None, 'Value' :    0, 'Text' : 'Record type                           ', 'Missing' : None},
                'REC_SUB'  : {'#' : 2, 'Type' : 'U*1', 'Ref' : None, 'Value' :   30, 'Text' : 'Record sub-type                       ', 'Missing' : None},
                'UPD_NAM'  : {'#' : 3, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : 'Update Version Name                   ', 'Missing' :   ''},
            }
            # fmt: on
        else:
            raise STDFError(f"{self.id} object creation error: unsupported version '{self.version}'")
        self._default_init(endian, record)
