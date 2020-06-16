#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 15:48:37 2020

@author: nerohmot
"""

import STDR

from utils import STDFError
from utils import __latest_STDF_version__


class FTR(STDR):
    """
Functional Test Record
----------------------

Function:
    Contains the results of the single execution of a functional test in the test program. The
    first occurrence of this record also establishes the default values for all semi-static
    information about the test. The FTR is related to the Test Synopsis Record (TSR) by test
    number, head number, and site number.

Frequency:
    * Obligatory, one or more for each execution of a functional test.

Location:
    Anywhere in the data stream after the corresponding Part Information Record (PIR)
    and before the corresponding Part Result Record (PRR).
"""

    def __init__(self, version=None, endian=None, record=None):
        self.id = 'FTR'
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
                'REC_LEN'  : {'#' :  0, 'Type' : 'U*2',  'Ref' :       None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' :    None},
                'REC_TYP'  : {'#' :  1, 'Type' : 'U*1',  'Ref' :       None, 'Value' :   15, 'Text' : 'Record type                           ', 'Missing' :    None},
                'REC_SUB'  : {'#' :  2, 'Type' : 'U*1',  'Ref' :       None, 'Value' :   20, 'Text' : 'Record sub-type                       ', 'Missing' :    None},
                'TEST_NUM' : {'#' :  3, 'Type' : 'U*4',  'Ref' :       None, 'Value' : None, 'Text' : 'Test number                           ', 'Missing' :    None}, # Obligatory!
                'HEAD_NUM' : {'#' :  4, 'Type' : 'U*1',  'Ref' :       None, 'Value' : None, 'Text' : 'Test head number                      ', 'Missing' :       1},
                'SITE_NUM' : {'#' :  5, 'Type' : 'U*1',  'Ref' :       None, 'Value' : None, 'Text' : 'Test site number                      ', 'Missing' :       1},
                'TEST_FLG' : {'#' :  6, 'Type' : 'B*1',  'Ref' :       None, 'Value' : None, 'Text' : 'Test flags (fail, alarm, etc.)        ', 'Missing' : ['0']*8},
                'OPT_FLAG' : {'#' :  7, 'Type' : 'B*1',  'Ref' :       None, 'Value' : None, 'Text' : 'Optional data flag                    ', 'Missing' : ['1']*8},
                'CYCL_CNT' : {'#' :  8, 'Type' : 'U*4',  'Ref' :       None, 'Value' : None, 'Text' : 'Cycle count of vector                 ', 'Missing' :       0}, # OPT_FLAG bit0 = 1
                'REL_VADR' : {'#' :  9, 'Type' : 'U*4',  'Ref' :       None, 'Value' : None, 'Text' : 'Relative vector address               ', 'Missing' :       0}, # OPT_FLAG bit1 = 1
                'REPT_CNT' : {'#' : 10, 'Type' : 'U*4',  'Ref' :       None, 'Value' : None, 'Text' : 'Repeat count of vector                ', 'Missing' :       0}, # OPT_FLAG bit2 = 1
                'NUM_FAIL' : {'#' : 11, 'Type' : 'U*4',  'Ref' :       None, 'Value' : None, 'Text' : 'Number of pins with 1 or more failures', 'Missing' :       0}, # OPT_FLAG bit3 = 1
                'XFAIL_AD' : {'#' : 12, 'Type' : 'I*4',  'Ref' :       None, 'Value' : None, 'Text' : 'X logical device failure address      ', 'Missing' :       0}, # OPT_FLAG bit4 = 1
                'YFAIL_AD' : {'#' : 13, 'Type' : 'I*4',  'Ref' :       None, 'Value' : None, 'Text' : 'Y logical device failure address      ', 'Missing' :       0}, # OPT_FLAG bit4 = 1
                'VECT_OFF' : {'#' : 14, 'Type' : 'I*2',  'Ref' :       None, 'Value' : None, 'Text' : 'Offset from vector of interest        ', 'Missing' :       0}, # OPT_FLAG bit5 = 1
                'RTN_ICNT' : {'#' : 15, 'Type' : 'U*2',  'Ref' :       None, 'Value' : None, 'Text' : 'Count (j) of return data PMR indexes  ', 'Missing' :       0},
                'PGM_ICNT' : {'#' : 16, 'Type' : 'U*2',  'Ref' :       None, 'Value' : None, 'Text' : 'Count (k) of programmed state indexes ', 'Missing' :       0},
                'RTN_INDX' : {'#' : 17, 'Type' : 'xU*2', 'Ref' : 'RTN_ICNT', 'Value' : None, 'Text' : 'Array of j return data PMR indexes    ', 'Missing' :      []}, # RTN_ICNT = 0
                'RTN_STAT' : {'#' : 18, 'Type' : 'xN*1', 'Ref' : 'RTN_ICNT', 'Value' : None, 'Text' : 'Array of j returned states            ', 'Missing' :      []}, # RTN_ICNT = 0
                'PGM_INDX' : {'#' : 19, 'Type' : 'xU*2', 'Ref' : 'PGM_ICNT', 'Value' : None, 'Text' : 'Array of k programmed state indexes   ', 'Missing' :      []}, # PGM_ICNT = 0
                'PGM_STAT' : {'#' : 20, 'Type' : 'xN*1', 'Ref' : 'PGM_ICNT', 'Value' : None, 'Text' : 'Array of k programmed states          ', 'Missing' :      []}, # PGM_ICNT = 0
                'FAIL_PIN' : {'#' : 21, 'Type' : 'D*n',  'Ref' :       None, 'Value' : None, 'Text' : 'Failing pin bitfield                  ', 'Missing' :      []},
                'VECT_NAM' : {'#' : 22, 'Type' : 'C*n',  'Ref' :       None, 'Value' : None, 'Text' : 'Vector module pattern name            ', 'Missing' :      ''},
                'TIME_SET' : {'#' : 23, 'Type' : 'C*n',  'Ref' :       None, 'Value' : None, 'Text' : 'Time set name                         ', 'Missing' :      ''},
                'OP_CODE'  : {'#' : 24, 'Type' : 'C*n',  'Ref' :       None, 'Value' : None, 'Text' : 'Vector Op Code                        ', 'Missing' :      ''},
                'TEST_TXT' : {'#' : 25, 'Type' : 'C*n',  'Ref' :       None, 'Value' : None, 'Text' : 'Descriptive text or label             ', 'Missing' :      ''},
                'ALARM_ID' : {'#' : 26, 'Type' : 'C*n',  'Ref' :       None, 'Value' : None, 'Text' : 'Name of alarm                         ', 'Missing' :      ''},
                'PROG_TXT' : {'#' : 27, 'Type' : 'C*n',  'Ref' :       None, 'Value' : None, 'Text' : 'Additional programmed information     ', 'Missing' :      ''},
                'RSLT_TXT' : {'#' : 28, 'Type' : 'C*n',  'Ref' :       None, 'Value' : None, 'Text' : 'Additional result information         ', 'Missing' :      ''},
                'PATG_NUM' : {'#' : 29, 'Type' : 'U*1',  'Ref' :       None, 'Value' : None, 'Text' : 'Pattern generator number              ', 'Missing' :    0xFF},
                'SPIN_MAP' : {'#' : 30, 'Type' : 'D*n',  'Ref' :       None, 'Value' : None, 'Text' : 'Bit map of enabled comparators        ', 'Missing' :      []}
            }
            # fmt: on
            raise STDFError(f"{self.id} object creation error: unsupported version '{self.version}'")
        self._default_init(endian, record)
