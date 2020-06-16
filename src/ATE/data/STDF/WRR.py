#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 15:59:23 2020

@author: nerohmot
"""

import STDR

from utils import STDFError
from utils import __latest_STDF_version__


class WRR(STDR):
    """
Wafer Results Record
--------------------

Function:
    Contains the result information relating to each wafer tested by the job plan. The WRR
    and the Wafer Information Record (WIR) bracket all the stored information pertaining
    to one tested wafer. This record is used only when testing at wafer probe time. A
    WIR/WRR pair will have the same HEAD_NUM and SITE_GRP values.

Frequency:
    * Obligatory for Wafer sort
    * One per wafer tested.

Location:
    Anywhere in the data stream after the corresponding WIR.
    Sent after testing each wafer.
"""

    def __init__(self, version=None, endian=None, record=None):
        self.id = 'WRR'
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
                'REC_LEN'  : {'#' :  0, 'Type' : 'U*2', 'Ref' : None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' : None      },
                'REC_TYP'  : {'#' :  1, 'Type' : 'U*1', 'Ref' : None, 'Value' :    2, 'Text' : 'Record type                           ', 'Missing' : None      },
                'REC_SUB'  : {'#' :  2, 'Type' : 'U*1', 'Ref' : None, 'Value' :   20, 'Text' : 'Record sub-type                       ', 'Missing' : None      },
                'HEAD_NUM' : {'#' :  3, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : 'Test head number                      ', 'Missing' : 255       },
                'SITE_GRP' : {'#' :  4, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : 'Site group number                     ', 'Missing' : 255       },
                'FINISH_T' : {'#' :  5, 'Type' : 'U*4', 'Ref' : None, 'Value' : None, 'Text' : 'Date and time last part tested        ', 'Missing' : 0         },
                'PART_CNT' : {'#' :  6, 'Type' : 'U*4', 'Ref' : None, 'Value' : None, 'Text' : 'Number of parts tested                ', 'Missing' : 0         },
                'RTST_CNT' : {'#' :  7, 'Type' : 'U*4', 'Ref' : None, 'Value' : None, 'Text' : 'Number of parts retested              ', 'Missing' : 4294967295},
                'ABRT_CNT' : {'#' :  8, 'Type' : 'U*4', 'Ref' : None, 'Value' : None, 'Text' : 'Number of aborts during testing       ', 'Missing' : 4294967295},
                'GOOD_CNT' : {'#' :  9, 'Type' : 'U*4', 'Ref' : None, 'Value' : None, 'Text' : 'Number of good (passed) parts tested  ', 'Missing' : 4294967295},
                'FUNC_CNT' : {'#' : 10, 'Type' : 'U*4', 'Ref' : None, 'Value' : None, 'Text' : 'Number of functional parts tested     ', 'Missing' : 4294967295},
                'WAFER_ID' : {'#' : 11, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : 'Wafer ID                              ', 'Missing' : ''        },
                'FABWF_ID' : {'#' : 12, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : 'Fab wafer ID                          ', 'Missing' : ''        },
                'FRAME_ID' : {'#' : 13, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : 'Wafer frame ID                        ', 'Missing' : ''        },
                'MASK_ID'  : {'#' : 14, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : 'Wafer mask ID                         ', 'Missing' : ''        },
                'USR_DESC' : {'#' : 15, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : 'Wafer description supplied by user    ', 'Missing' : ''        },
                'EXC_DESC' : {'#' : 16, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : 'Wafer description supplied by exec    ', 'Missing' : ''        }
            }
            # fmt: on
        else:
            raise STDFError(f"{self.id} object creation error: unsupported version '{self.version}'")
        self._default_init(endian, record)
