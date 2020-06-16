#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 16:08:17 2020

@author: nerohmot
"""

import STDR

from utils import STDFError
from utils import __latest_STDF_version__


class WCR(STDR):
    """
Wafer Configuration Record
--------------------------

Function:
    Contains the configuration information for the wafers tested by the job plan. The
    WCR provides the dimensions and orientation information for all wafers and dice
    in the lot. This record is used only when testing at wafer probe time.

Frequency:
    * Obligatory for Wafer sort
    * One per STDF file

Location:
    Anywhere in the data stream after the initial "FAR-(ATRs)-MIR-(RDR)-(SDRs)" sequence, and before the MRR.
"""

    def __init__(self, version=None, endian=None, record=None):
        self.id = 'WCR'
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
                'REC_LEN'  : {'#' :  0, 'Type' : 'U*2', 'Ref' : None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' : None  },
                'REC_TYP'  : {'#' :  1, 'Type' : 'U*1', 'Ref' : None, 'Value' :    2, 'Text' : 'Record type                           ', 'Missing' : None  },
                'REC_SUB'  : {'#' :  2, 'Type' : 'U*1', 'Ref' : None, 'Value' :   30, 'Text' : 'Record sub-type                       ', 'Missing' : None  },
                'WAFR_SIZ' : {'#' :  3, 'Type' : 'R*4', 'Ref' : None, 'Value' : None, 'Text' : 'Diameter of wafer in WF_UNITS         ', 'Missing' : 0.0   },
                'DIE_HT'   : {'#' :  4, 'Type' : 'R*4', 'Ref' : None, 'Value' : None, 'Text' : 'Height of die in WF_UNITS             ', 'Missing' : 0.0   },
                'DIE_WID'  : {'#' :  5, 'Type' : 'R*4', 'Ref' : None, 'Value' : None, 'Text' : 'Width of die in WF_UNITS              ', 'Missing' : 0.0   },
                'WF_UNITS' : {'#' :  6, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : 'Units for wafer and die dimensions    ', 'Missing' : 0     }, # 0=?/1=Inch/2=cm/3=mm/4=mils
                'WF_FLAT'  : {'#' :  7, 'Type' : 'C*1', 'Ref' : None, 'Value' : None, 'Text' : 'Orientation of wafer flat (U/D/L/R)   ', 'Missing' : ' '   },
                'CENTER_X' : {'#' :  8, 'Type' : 'I*2', 'Ref' : None, 'Value' : None, 'Text' : 'X coordinate of center die on wafer   ', 'Missing' : -32768},
                'CENTER_Y' : {'#' :  9, 'Type' : 'I*2', 'Ref' : None, 'Value' : None, 'Text' : 'Y coordinate of center die on wafer   ', 'Missing' : -32768},
                'POS_X'    : {'#' : 10, 'Type' : 'C*1', 'Ref' : None, 'Value' : None, 'Text' : 'Positive X direction of wafer (L/R)   ', 'Missing' : ' '   },
                'POS_Y'    : {'#' : 11, 'Type' : 'C*1', 'Ref' : None, 'Value' : None, 'Text' : 'Positive Y direction of wafer (U/D)   ', 'Missing' : ' '   }
            }
            # fmt: on
        else:
            raise STDFError(f"{self.id} object creation error: unsupported version '{self.version}'")
        self._default_init(endian, record)
