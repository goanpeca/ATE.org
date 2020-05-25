# -*- coding: utf-8 -*-
"""
Created on Sat May 23 13:38:37 2020

@author: tom
"""

import STDR

from utils import sys_cpu
from utils import STDFError
from utils import __latest_STDF_version__


class FAR(STDR):
    """File Attributes Record (FAR)
----------------------------

Function:
    Contains the information necessary to determine how to decode the STDF data contained in the file.

Frequency:
    * Obligatory
    * One per datastream

Location:
    First record of the STDF file
"""

    def __init__(self, version=None, endian=None, record=None):
        self.id = 'FAR'
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
                'REC_LEN'  : {'#' :  0, 'Type' : 'U*2', 'Ref' : None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' :                 None},
                'REC_TYP'  : {'#' :  1, 'Type' : 'U*1', 'Ref' : None, 'Value' :    0, 'Text' : 'Record type                           ', 'Missing' :                 None},
                'REC_SUB'  : {'#' :  2, 'Type' : 'U*1', 'Ref' : None, 'Value' :   10, 'Text' : 'Record sub-type                       ', 'Missing' :                 None},
                'CPU_TYPE' : {'#' :  3, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : 'CPU type that wrote this file         ', 'Missing' :            sys_cpu()},
                'STDF_VER' : {'#' :  4, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : 'STDF version number                   ', 'Missing' : int(self.version[1])},
            }
            # fmt: on
        else:
            raise STDFError(f"{self.id} object creation error: unsupported version '{self.version}'")
        self._default_init(endian, record)
