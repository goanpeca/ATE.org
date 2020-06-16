#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 15:52:53 2020

@author: nerohmot
"""

import STDR

from utils import STDFError
from utils import __latest_STDF_version__


class GDR(STDR):
    """
Generic Data Record
-------------------

Function:
    Contains information that does not conform to any other record type defined by the
    STDF specification. Such records are intended to be written under the control of job
    plans executing on the tester. This data may be used for any purpose that the user
    desires.

Frequency:
    * Optional, a test data file may contain any number of GDRs.

Location:
    Anywhere in the data stream after the initial "FAR-(ATRs)-MIR-(RDR)-(SDRs)" sequence.
"""

    def __init__(self, version=None, endian=None, record=None):
        self.id = 'GDR'
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
                'REC_LEN'  : {'#' : 0, 'Type' :  'U*2', 'Ref' :      None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' : None},
                'REC_TYP'  : {'#' : 1, 'Type' :  'U*1', 'Ref' :      None, 'Value' :   50, 'Text' : 'Record type                           ', 'Missing' : None},
                'REC_SUB'  : {'#' : 2, 'Type' :  'U*1', 'Ref' :      None, 'Value' :   10, 'Text' : 'Record sub-type                       ', 'Missing' : None},
                'FLD_CNT'  : {'#' : 3, 'Type' :  'U*2', 'Ref' :      None, 'Value' : None, 'Text' : 'Count of data fields in record        ', 'Missing' :    0},
                'GEN_DATA' : {'#' : 4, 'Type' : 'xV*n', 'Ref' : 'FLD_CNT', 'Value' : None, 'Text' : 'Data type code and data for one field ', 'Missing' :   []}
            }
            # fmt: on
        else:
            raise STDFError(f"{self.id} object creation error: unsupported version '{self.version}'")
        self._default_init(endian, record)
