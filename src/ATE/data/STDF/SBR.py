#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 23 18:53:50 2020

@author: tom
"""

import STDR

from utils import STDFError
from utils import __latest_STDF_version__


class SBR(STDR):
    """Software Bin Record (SBR)
-------------------------

Function:
    Stores a count of the parts associated with a particular logical bin after testing. This
    bin count can be for a single test site (when parallel testing) or a total for all test sites.
    The STDF specification also supports a Hardware Bin Record (HBR) for actual physical
    binning. A part is "physically" placed in a hardware bin after testing. A part can be
    "logically" associated with a software bin during or after testing.

Frequency:
    * Obligatory
    * One per software bin for each head/site combination
    * One per software bin for all head/site combinations together ('HEAD_NUM' = 255)
    * May be included to name unused bins.

Location:
    Anywhere in the data stream after the initial "FAR-(ATRs)-MIR-(RDR)-(SDRs)" sequence and before the MRR.
    When data is being recorded in real time, this record usually appears near the end of the data stream.
"""

    def __init__(self, version=None, endian=None, record=None):
        self.id = 'SBR'
        self.local_debug = False
        if version is None:
            self.version = __latest_STDF_version__
        else:
            self.version = version

        # implementation base on the version
        if self.version == 'V4':
            self.info = self.__doc__
            self.fields = {
                'REC_LEN'  : {'#' :  0, 'Type' :  'U*2', 'Ref' : None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' : None},
                'REC_TYP'  : {'#' :  1, 'Type' :  'U*1', 'Ref' : None, 'Value' :    1, 'Text' : 'Record type                           ', 'Missing' : None},
                'REC_SUB'  : {'#' :  2, 'Type' :  'U*1', 'Ref' : None, 'Value' :   50, 'Text' : 'Record sub-type                       ', 'Missing' : None},
                'HEAD_NUM' : {'#' :  3, 'Type' :  'U*1', 'Ref' : None, 'Value' : None, 'Text' : 'Test head number (255 = summary)      ', 'Missing' : 1   },
                'SITE_NUM' : {'#' :  4, 'Type' :  'U*1', 'Ref' : None, 'Value' : None, 'Text' : 'Test site number                      ', 'Missing' : 1   },
                'SBIN_NUM' : {'#' :  5, 'Type' :  'U*2', 'Ref' : None, 'Value' : None, 'Text' : 'Software bin number                   ', 'Missing' : 0   },
                'SBIN_CNT' : {'#' :  6, 'Type' :  'U*4', 'Ref' : None, 'Value' : None, 'Text' : 'Number of parts in bin                ', 'Missing' : 0   },
                'SBIN_PF'  : {'#' :  7, 'Type' :  'C*1', 'Ref' : None, 'Value' : None, 'Text' : 'Pass/fail indication (P/F)            ', 'Missing' : ' ' },
                'SBIN_NAM' : {'#' :  8, 'Type' :  'C*n', 'Ref' : None, 'Value' : None, 'Text' : 'Name of software bin                  ', 'Missing' : ''  }
            }
        else:
            raise STDFError(f"{self.id} object creation error: unsupported version '{self.version}'")
        self._default_init(endian, record)
