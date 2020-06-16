#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 16:03:45 2020

@author: nerohmot
"""

import STDR

from utils import STDFError
from utils import __latest_STDF_version__


class WIR(STDR):
    """
Wafer Information Record
------------------------

Function:
    Acts mainly as a marker to indicate where testing of a particular wafer begins for each
    wafer tested by the job plan. The WIR and the Wafer Results Record (WRR) bracket all
    the stored information pertaining to one tested wafer. This record is used only when
    testing at wafer probe. A WIR/WRR pair will have the same HEAD_NUM and SITE_GRP values.

Frequency:
    * Obligatory for Wafer sort
    * One per wafer tested.

Location:
    Anywhere in the data stream after the initial sequence (see page 14) and before the MRR.
    Sent before testing each wafer.
"""

    def __init__(self, version=None, endian=None, record=None):
        self.id = 'WIR'
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
                'REC_LEN'  : {'#' :  0, 'Type' : 'U*2', 'Ref' : None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' : None},
                'REC_TYP'  : {'#' :  1, 'Type' : 'U*1', 'Ref' : None, 'Value' :    2, 'Text' : 'Record type                           ', 'Missing' : None},
                'REC_SUB'  : {'#' :  2, 'Type' : 'U*1', 'Ref' : None, 'Value' :   10, 'Text' : 'Record sub-type                       ', 'Missing' : None},
                'HEAD_NUM' : {'#' :  3, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : 'Test head number                      ', 'Missing' : 1   },
                'SITE_GRP' : {'#' :  4, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : 'Site group number                     ', 'Missing' : 255 },
                'START_T'  : {'#' :  5, 'Type' : 'U*4', 'Ref' : None, 'Value' : None, 'Text' : 'Date and time first part tested       ', 'Missing' : 0   },
                'WAFER_ID' : {'#' :  6, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : 'Wafer ID                              ', 'Missing' : ''  }
            }
            # fmt: on
            raise STDFError(f"{self.id} object creation error: unsupported version '{self.version}'")
        self._default_init(endian, record)
