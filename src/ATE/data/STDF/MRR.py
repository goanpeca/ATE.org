#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 23 15:08:15 2020

@author: tom
"""

import time
import STDR

from utils import STDFError
from utils import __latest_STDF_version__


class MRR(STDR):
    """Master Results Record (MRR)
---------------------------

Function:
    The Master Results Record (MRR) is a logical extension of the Master Information
    Record (MIR). The data can be thought of as belonging with the MIR, but it is not
    available when the tester writes the MIR information. Each data stream must have
    exactly one MRR as the last record in the data stream.

Frequency:
    * Obligatory
    * One per data stream

Location:
    Must be the last record in the data stream.
"""

    def __init__(self, version=None, endian=None, record=None):
        self.id = 'MRR'
        self.local_debug = False
        if version is None:
            self.version = __latest_STDF_version__
        else:
            self.version = version

        # implementation base on the version
        if self.version == 'V4':
            self.info = self.__doc__
            missing_time = int(time.time())
            self.fields = {
                'REC_LEN'  : {'#' : 0, 'Type' : 'U*2', 'Ref' : None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' :         None},
                'REC_TYP'  : {'#' : 1, 'Type' : 'U*1', 'Ref' : None, 'Value' :    1, 'Text' : 'Record type                           ', 'Missing' :         None},
                'REC_SUB'  : {'#' : 2, 'Type' : 'U*1', 'Ref' : None, 'Value' :   20, 'Text' : 'Record sub-type                       ', 'Missing' :         None},
                'FINISH_T' : {'#' : 3, 'Type' : 'U*4', 'Ref' : None, 'Value' : None, 'Text' : 'Date and time last part tested        ', 'Missing' : missing_time},
                'DISP_COD' : {'#' : 4, 'Type' : 'C*1', 'Ref' : None, 'Value' : None, 'Text' : 'Lot disposition code                  ', 'Missing' :          ' '},
                'USR_DESC' : {'#' : 5, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : 'Lot description supplied by user      ', 'Missing' :           ''},
                'EXC_DESC' : {'#' : 6, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : 'Lot description supplied by exec      ', 'Missing' :           ''}
            }
        else:
            raise STDFError(f"{self.id} object creation error: unsupported version '{self.version}'")
        self._default_init(endian, record)
