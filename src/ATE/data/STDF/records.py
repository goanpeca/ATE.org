'''
Created on Jan 6, 2016

@author: $Author: horen.tom@gmail.com$

This module is part of the ATE.org (meta) package.
--------------------------------------------------
This library implements the STDF standard to the full extend (meaning including optional field presence) to read/modify/write STDF files.

Support:
    Endians: Little & Big
    Versions & Extensions:
        V3 : standard, +
        V4 : standard, V4-2007, Memory:2010.1
    Modes: read & write
    compressions: gzip (read & write)

Disclaimer:
    Although all aspects of the library are tested extensively with unit tests, the library could only be tested in real life using standard STDF V4 files.
    It has not been used with STDF V4 extensions (lack of sample files) or STDF V3 (lack of sample files and specification)

License : GPL

References:
    -

PEP8 and ignore E501, E241, E221, E203, E202, E201

'''

import bz2
import io
import os
import pickle
import struct
import sys

from mimetypes import guess_type
import time
import datetime

if sys.version_info[0] < 3:
    raise Exception("The STDF library is made for Python 3")


__version__ = '$Revision: 0.51 $'
__author__ = '$Author: tho $'





# Removal of dependency on ATE.utils.macignumber:
# The original implementation in ATE.utils.magicnumber.extension_from_magic_number_in_file(filename)
# returns '.stdf' if the two bytes at offset 2 of the given file are equal to b'\x00\x0A'.
# This checks that the data in the file looks a FAR record (REC_TYP is 0, REC_SUB is 10).
# Note that the REC_LEN field (first two bytes of the file) is probably ignored because it
# depends on the endianness, defined by CPU_TYPE (fifth byte).
def is_file_with_stdf_magicnumber(filename):
    try:
        with open(filename, 'rb') as f:
            f.seek(2)
            return f.read(2) == b'\x00\x0A'
    except OSError:
        # if it cannot be read it's not an stdf file
        return False


# Removal of dependency on ATE.utils.DT: DT().epoch and DT.__repr__
def _missing_stdf_time_field_value() -> int:
    return int(time.time())  # used to be DT().epoch, which returned time.time(). note that we need an 32bit unsigned integer to allow de-/serialization without data loss

# date and time format according to the STDF spec V4:
# number of seconds since midnight on January 1st, 1970, in the local time zone (32bit unsigned int)
# Note that DT() has a more detailed format but that is not relevant for now (e.g. we dont need Quarter)


def _stdf_time_field_value_to_string(seconds_since_1970_in_local_time: int):
    return datetime.datetime.fromtimestamp(seconds_since_1970_in_local_time).strftime('%Y-%m-%d %H:%M:%S')










###################################################################################################################################################
#TODO: change 'V4' and 'V3' in self.version to 4 and 3 respectively
#TODO: Implement the FPE (Field Present Expression) in all records
#TODO: Impleent support for the FPE in packing/unpacking
#TODO: Run trough all records and set the FPE correct

class ADR(STDR):
    def __init__(self, version=None, endian=None, record=None):
        self.id = ''
        self.local_debug = False
        # Version
        if version==None or version=='V3':
            self.version = 'V3'
            self.info=    '''
?!?
------------------

Function:
    ?!?

Frequency:
    *

Location:
'''
            self.fields = {
                'REC_LEN'  : {'#' :  0, 'Type' : 'U*2', 'Ref' :      None, 'Value' : None, 'Text' : 'Bytes of data following header                      ', 'Missing' :         None, 'Note' : ''},
                'REC_TYP'  : {'#' :  1, 'Type' : 'U*1', 'Ref' :      None, 'Value' :  220, 'Text' : 'Record type                                         ', 'Missing' :         None, 'Note' : ''},
                'REC_SUB'  : {'#' :  2, 'Type' : 'U*1', 'Ref' :      None, 'Value' :  205, 'Text' : 'Record sub-type                                     ', 'Missing' :         None, 'Note' : ''},
                'CPU_TYPE' : {'#' :  3, 'Type' : 'U1' , 'Ref' :      None, 'Value' : None, 'Text' : '                                                    ', 'Missing' :    sys_cpu(), 'Note' : ''},
                'STDF_VER' : {'#' :  4, 'Type' : 'Cn' , 'Ref' :      None, 'Value' : None, 'Text' : '                                                    ', 'Missing' : self.version, 'Note' : ''},
                'DB_ID'    : {'#' :  5, 'Type' : 'U1' , 'Ref' :      None, 'Value' : None, 'Text' : '                                                    ', 'Missing' :            0, 'Note' : ''},
                'PARA_CNT' : {'#' :  6, 'Type' : 'U2' , 'Ref' :      None, 'Value' : None, 'Text' : '                                                    ', 'Missing' :            0, 'Note' : ''},
                'LOT_FLG'  : {'#' :  7, 'Type' : 'U1' , 'Ref' :      None, 'Value' : None, 'Text' : '                                                    ', 'Missing' :            0, 'Note' : ''},
                'RTST_CNT' : {'#' :  8, 'Type' : 'U2' , 'Ref' :      None, 'Value' : None, 'Text' : '                                                    ', 'Missing' :            0, 'Note' : ''},
                'LOT_TYPE' : {'#' :  9, 'Type' : 'C1' , 'Ref' :      None, 'Value' : None, 'Text' : '                                                    ', 'Missing' :          ' ', 'Note' : ''},
                'RTST_WAF' : {'#' : 10, 'Type' : 'xCn', 'Ref' :'RTST_CNT', 'Value' : None, 'Text' : '                                                    ', 'Missing' :           [], 'Note' : ''},
                'RTST_BIN' : {'#' : 11, 'Type' : 'xU4', 'Ref' :'RTST_CNT', 'Value' : None, 'Text' : '                                                    ', 'Missing' :           [], 'Note' : ''},
            }
        else:
            raise STDFError("%s object creation error: unsupported version '%s'" % (self.id, version))
        self._default_init(endian, record)

class ASR(STDR):
    def __init__(self, version=None, endian=None, record=None):
        self.id = ''
        self.local_debug = False
        # Version
        if version==None or version=='V4':
            self.version = 'V4'
            self.info=    '''
Algorithm Specification Record (V4, Memory:2010.1)
--------------------------------------------------

Function:
    This record is used to store the algorithms that are applied during a memory test. Table 11 Algorithm Specification Record (ASR) Record

Frequency:
    * Once per unique memory test specification.

Location:
    It can occur after all the Memory Model Records(MMRs) and before any Test specific records
    e.g. Parametric Test Record (PTR), Functional Test Record (FTRs), Scan Test Record (STR) and Memory Test Record (MTRs).
'''
            self.fields = {
                'REC_LEN'  : {'#' :  0, 'Type' : 'U*2'  , 'Ref' :       None, 'Value' : None, 'Text' : 'Bytes of data following header                      ', 'Missing' : None, 'Note' : ''},
                'REC_TYP'  : {'#' :  1, 'Type' : 'U*1'  , 'Ref' :       None, 'Value' :    0, 'Text' : 'Record type                                         ', 'Missing' : None, 'Note' : ''},
                'REC_SUB'  : {'#' :  2, 'Type' : 'U*1'  , 'Ref' :       None, 'Value' :   20, 'Text' : 'Record sub-type                                     ', 'Missing' : None, 'Note' : ''},
                'ASR_IDX'  : {'#' :  3, 'Type' : 'U*2'  , 'Ref' :       None, 'Value' : None, 'Text' : 'Unique identifier for this ASR record               ', 'Missing' :    0, 'Note' : ''},
                'STRT_IDX' : {'#' :  4, 'Type' : 'U*1'  , 'Ref' :       None, 'Value' : None, 'Text' : 'Cycle Start index flag                              ', 'Missing' :    0, 'Note' : ''},
                'ALGO_CNT' : {'#' :  5, 'Type' : 'U*1'  , 'Ref' :       None, 'Value' : None, 'Text' : 'count (k) of Algorithms descriptions                ', 'Missing' :    0, 'Note' : ''},
                'ALGO_NAM' : {'#' :  6, 'Type' : 'xC*n' , 'Ref' : 'ALGO_CNT', 'Value' : None, 'Text' : 'Array of Names of the Algorithms                    ', 'Missing' :   [], 'Note' : ''},
                'ALGO_LEN' : {'#' :  7, 'Type' : 'xC*n' , 'Ref' : 'ALGO_CNT', 'Value' : None, 'Text' : 'Array of Complexity of algorithm  (e.g., 13N)       ', 'Missing' :   [], 'Note' : ''},
                'FILE_ID'  : {'#' :  8, 'Type' : 'xC*n' , 'Ref' : 'ALGO_CNT', 'Value' : None, 'Text' : 'Array of Name of the file with algorithm description', 'Missing' :   [], 'Note' : ''},
                'CYC_BGN'  : {'#' :  9, 'Type' : 'xU*8' , 'Ref' : 'ALGO_CNT', 'Value' : None, 'Text' : 'Array of Starting cycle number for the Algorithms   ', 'Missing' :   [], 'Note' : ''},
                'CYC_END'  : {'#' : 10, 'Type' : 'xU*8' , 'Ref' : 'ALGO_CNT', 'Value' : None, 'Text' : 'Array of End Cycle number for the algorithm         ', 'Missing' :   [], 'Note' : ''}
            }
        else:
            raise STDFError("%s object creation error: unsupported version '%s'" % (self.id, version))
        self._default_init(endian, record)


class BPS(STDR):
    def __init__(self, version=None, endian=None, record=None):
        self. id = 'BPS'
        self.local_debug = False
        # Version
        if version==None or version=='V4' or version=='V3':
            if version==None: self.verson = 'V4'
            else: self.version = version
            self.info = '''
Begin Program Section Record
----------------------------

Function:
    Marks the beginning of a new program section (or sequencer) in the job plan.

Frequency:
    * Optional on each entry into the program segment.

Location:
    Anywhere after the PIR and before the PRR.
'''
            self.fields = {
                'REC_LEN'  : {'#' :  0, 'Type' :  'U*2', 'Ref' : None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' : None, 'Note' : ''},
                'REC_TYP'  : {'#' :  1, 'Type' :  'U*1', 'Ref' : None, 'Value' :   20, 'Text' : 'Record type                           ', 'Missing' : None, 'Note' : ''},
                'REC_SUB'  : {'#' :  2, 'Type' :  'U*1', 'Ref' : None, 'Value' :   10, 'Text' : 'Record sub-type                       ', 'Missing' : None, 'Note' : ''},
                'SEQ_NAME' : {'#' :  3, 'Type' :  'C*n', 'Ref' : None, 'Value' : None, 'Text' : 'Sequence name                         ', 'Missing' :   '', 'Note' : ''}
            }
        else:
            raise STDFError("%s object creation error: unsupported version '%s'" % (self.id, version))
        self._default_init(endian, record)

class BRR(STDR):
    def __init__(self, version=None, endian=None, record=None):
        self. id = 'BRR'
        self.local_debug = False
        # Version
        if version==None or version=='V3':
            self.version = 'V3'
            self.info = '''
?!?
----------------------------

Function:


Frequency:


Location:

'''
            self.fields = {
                'REC_LEN'  : {'#' : 0, 'Type' : 'U*2', 'Ref' : None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' : None},
                'REC_TYP'  : {'#' : 1, 'Type' : 'U*1', 'Ref' : None, 'Value' :  220, 'Text' : 'Record type                           ', 'Missing' : None},
                'REC_SUB'  : {'#' : 2, 'Type' : 'U*1', 'Ref' : None, 'Value' :  201, 'Text' : 'Record sub-type                       ', 'Missing' : None},
                'RTST_COD' : {'#' : 3, 'Type' : 'C*1', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :  ' '},
                'BIN_CNT'  : {'#' : 4, 'Type' : 'U*2', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :    0},
                'BIN_NUM'  : {'#' : 5, 'Type' : 'U*2', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :    0}
            }
        else:
            raise STDFError("%s object creation error: unsupported version '%s'" % (self.id, version))
        self._default_init(endian, record)

class BSR(STDR):
    def __init__(self, version=None, endian=None, record = None):
        self.id = 'BSR'
        self.local_debug = False
        if version==None or version=='V4':
            self.version = 'V4'
            self.info=    '''
Bit stream Specification Record (V4, Memory:2010.1)
---------------------------------------------------

Function:
    This record is used to enable string bit stream data from the memories.
    This record defines the format of the bit stream in which the data can be recorded in Memory Test Record (MTR).
    The bit streams are stored as stream of clusters for compaction. i.e. only the data words that have meaningful
    information are stored in the stream. Each cluster is defined as the starting address where the meaningful
    information starts followed by the count of words with meaningful information followed by the words themselves.

Frequency:
    Once per memory Algorithm.

Location:
    It can occur after all the Memory Model Records(MMRs) and before any Test specific records e.g.
    Parametric Test Record (PTR), Functional Test Record (FTRs), Scan Test Record (STR) and Memory Test Record (MTRs).
'''
            self.fields = {
                'REC_LEN'  : {'#' : 0, 'Type' : 'U*2' , 'Ref' : None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' : None},
                'REC_TYP'  : {'#' : 1, 'Type' : 'U*1' , 'Ref' : None, 'Value' :    1, 'Text' : 'Record type                           ', 'Missing' : None},
                'REC_SUB'  : {'#' : 2, 'Type' : 'U*1' , 'Ref' : None, 'Value' :   97, 'Text' : 'Record sub-type                       ', 'Missing' : None},
                'BSR_IDX'  : {'#' : 3, 'Type' : 'U*2' , 'Ref' : None, 'Value' : None, 'Text' : 'Unique ID for this Bit stream         ', 'Missing' :    0},
                'BIT_TYP'  : {'#' : 4, 'Type' : 'U*1' , 'Ref' : None, 'Value' : None, 'Text' : 'Meaning of bits in the stream         ', 'Missing' :    0},
                'ADDR_SIZ' : {'#' : 5, 'Type' : 'U*1' , 'Ref' : None, 'Value' : None, 'Text' : 'Address field size [1,2,4 or 8]       ', 'Missing' :    0},
                'WC_SIZ'   : {'#' : 6, 'Type' : 'U*1' , 'Ref' : None, 'Value' : None, 'Text' : 'Word Count Field Size [1,2,4 or 8]    ', 'Missing' :    0},
                'WRD_SIZ'  : {'#' : 7, 'Type' : 'U*2' , 'Ref' : None, 'Value' : None, 'Text' : 'Number of bits used in the word field ', 'Missing' :    0}
            }
        else:
            raise STDFError("%s object creation error: unsupported version '%s'" % (self.id, version))
        self._default_init(endian, record)

class CDR(STDR):
    def __init__(self, version=None, endian=None, record = None):
        self.id = 'CDR'
        self.local_debug = False
        if version==None or version=='V4':
            self.version = 'V4'
            self.info=    '''
Chain Description Record (V4-2007)
----------------------------------

Function:
    This record contains the description of a scan chain in terms of its input, output, number of cell and clocks.
    Each CDR record contains description of exactly one scan chain. Each CDR is uniquely identified by an index.

Frequency:
    ?!?

Location:
    ?!?
'''
            self.fields = {
                'REC_LEN'  : {'#' :  0, 'Type' : 'U*2',  'Ref' : None,       'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' : None},
                'REC_TYP'  : {'#' :  1, 'Type' : 'U*1',  'Ref' : None,       'Value' :    1, 'Text' : 'Record type                           ', 'Missing' : None},
                'REC_SUB'  : {'#' :  2, 'Type' : 'U*1',  'Ref' : None,       'Value' :   94, 'Text' : 'Record sub-type                       ', 'Missing' : None},
                'CONT_FLG' : {'#' :  3, 'Type' : 'B*1',  'Ref' : None,       'Value' : None, 'Text' : 'Continuation CDR record follow (if!=0)', 'Missing' : 0},
                'CDR_INDX' : {'#' :  4, 'Type' : 'U*2',  'Ref' : None,       'Value' : None, 'Text' : 'SCR Index                             ', 'Missing' : 0},
                'CHN_NAM'  : {'#' :  5, 'Type' : 'C*n',  'Ref' : None,       'Value' : None, 'Text' : 'Chain Name                            ', 'Missing' : None},
                'CHN_LEN'  : {'#' :  6, 'Type' : 'U*4',  'Ref' : None,       'Value' : None, 'Text' : 'Chain Length (cells in chain)         ', 'Missing' : 0},
                'SIN_PIN'  : {'#' :  7, 'Type' : 'U*2',  'Ref' : None,       'Value' : None, 'Text' : "PMR index of the chain's Scan In Sig  ", 'Missing' : 0},
                'SOUT_PIN' : {'#' :  8, 'Type' : 'U*2',  'Ref' : None,       'Value' : None, 'Text' : "PMR index of the chain's Scan Out Sig ", 'Missing' : 0},
                'MSTR_CNT' : {'#' :  9, 'Type' : 'U*1',  'Ref' : None,       'Value' : None, 'Text' : 'Count (m) of master clock pins        ', 'Missing' : 0},
                'M_CLKS'   : {'#' : 10, 'Type' : 'xU*2', 'Ref' : 'MSTR_CNT', 'Value' : None, 'Text' : 'Arr of PMR indses for the master clks ', 'Missing' : []},
                'SLAV_CNT' : {'#' : 11, 'Type' : 'U*1',  'Ref' : None,       'Value' : None, 'Text' : 'Count (n) of slave clock pins         ', 'Missing' : 0},
                'S_CLKS'   : {'#' : 12, 'Type' : 'xU*2', 'Ref' : 'SLAV_CNT', 'Value' : None, 'Text' : 'Arr of PMR indxes for the slave clks  ', 'Missing' : []},
                'INV_VAL'  : {'#' : 13, 'Type' : 'U*1',  'Ref' : None,       'Value' : None, 'Text' : '0: No Inversion, 1: Inversion         ', 'Missing' : 0},
                'LST_CNT'  : {'#' : 14, 'Type' : 'U*2',  'Ref' : None,       'Value' : None, 'Text' : 'Count (k) of scan cells               ', 'Missing' : 0},
                'CELL_LST' : {'#' : 15, 'Type' : 'xS*n', 'Ref' : 'LST_CNT',  'Value' : None, 'Text' : 'Array of Scan Cell Names              ', 'Missing' : []},
            }
        else:
            raise STDFError("%s object creation error: unsupported version '%s'" % (self.id, version))
        self._default_init(endian, record)

class CNR(STDR):
    def __init__(self, version=None, endian=None, record = None):
        self.id = 'CNR'
        self.local_debug = False
        if version==None or version=='V4':
            self.version = 'V4'
            self.info=    '''
Cell Name Record (V4-2007)
--------------------------

Function:
    This record is used to store the mapping from Chain and Bit position to the Cell/FlipFlop name.
    A CNR record should be created for each Cell for which a name mapping is required.
    Typical usage would be to create a record for each failing cell/FlipFlop.
    A CNR with new mapping for a chain and bit position would override the previous mapping.

Frequency:

Location:
'''
            self.fields = {
                'REC_LEN'  : {'#' :  0, 'Type' : 'U*2' , 'Ref' : None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' : None},
                'REC_TYP'  : {'#' :  1, 'Type' : 'U*1' , 'Ref' : None, 'Value' :    1, 'Text' : 'Record type                           ', 'Missing' : None},
                'REC_SUB'  : {'#' :  2, 'Type' : 'U*1' , 'Ref' : None, 'Value' :   92, 'Text' : 'Record sub-type                       ', 'Missing' : None},
                'CHN_NUM'  : {'#' :  2, 'Type' : 'U*2' , 'Ref' : None, 'Value' : None, 'Text' : 'Chain number. (cfr STR:CHN_NUM)       ', 'Missing' :    0},
                'BIT_POS'  : {'#' :  2, 'Type' : 'U*4' , 'Ref' : None, 'Value' : None, 'Text' : 'Bit position in the chain             ', 'Missing' :    0},
                'CELL_NAM' : {'#' :  2, 'Type' : 'S*n' , 'Ref' : None, 'Value' : None, 'Text' : 'Scan Cell Name                        ', 'Missing' :   ''}
            }
        else:
            raise STDFError("%s object creation error: unsupported version '%s'" % (self.id, version))
        self._default_init(endian, record)

class DTR(STDR):
    def __init__(self, version=None, endian=None, record=None):
        self.id = 'DTR'
        self.local_debug = False
        # Version
        if version==None or version=='V4' or version=='V3':
            if version==None: self.version = 'V4'
            else: self.version = version
            self.info = '''
Datalog Text Record
-------------------

Function:
    Contains text information that is to be included in the datalog printout. DTRs may be
    written under the control of a job plan: for example, to highlight unexpected test
    results. They may also be generated by the tester executive software: for example, to
    indicate that the datalog sampling rate has changed. DTRs are placed as comments in
    the datalog listing.

Frequency:
    * Optional, a test data file may contain any number of DTRs.

Location:
    Anywhere in the data stream after the initial "FAR-(ATRs)-MIR-(RDR)-(SDRs)" sequence.
'''
            self.fields = {
                'REC_LEN'  : {'#' : 0, 'Type' : 'U*2', 'Ref' : None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' : None},
                'REC_TYP'  : {'#' : 1, 'Type' : 'U*1', 'Ref' : None, 'Value' :   50, 'Text' : 'Record type                           ', 'Missing' : None},
                'REC_SUB'  : {'#' : 2, 'Type' : 'U*1', 'Ref' : None, 'Value' :   30, 'Text' : 'Record sub-type                       ', 'Missing' : None},
                'TEXT_DAT' : {'#' : 3, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : 'Message                               ', 'Missing' :   ''}
            }
        else:
            raise STDFError("%s object creation error: unsupported version '%s'" % (self.id, version))
        self._default_init(endian, record)

class EPDR(STDR):
    def __init__(self, version=None, endian=None, record=None):
        self.id = 'EPDR'
        self.local_debug = False
        # Version
        if version==None or version=='V3':
            self.version = 'V3'
            self.info = '''
?!?
-------------------

Function:
    ?!?
Frequency:
    ?!?

Location:
    ?!?
'''
            self.fields = {
                'REC_LEN'  : {'#' : 0, 'Type' : 'U*2', 'Ref' : None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' :    None},
                'REC_TYP'  : {'#' : 1, 'Type' : 'U*1', 'Ref' : None, 'Value' :  220, 'Text' : 'Record type                           ', 'Missing' :    None},
                'REC_SUB'  : {'#' : 2, 'Type' : 'U*1', 'Ref' : None, 'Value' :  206, 'Text' : 'Record sub-type                       ', 'Missing' :    None},
                'TEST_NUM' : {'#' : 3, 'Type' : 'U*4', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :       0},
                'OPT_FLAG' : {'#' : 4, 'Type' : 'B*1', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' : ['0']*8},
                'CAT'      : {'#' : 5, 'Type' : 'C*2', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :    '  '},
                'TARGET'   : {'#' : 6, 'Type' : 'R*4', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :     0.0},
                'SPC_FLAG' : {'#' : 7, 'Type' : 'C*2', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :    '  '},
                'LVL'      : {'#' : 8, 'Type' : 'R*4', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :     0.0},
                'HVL'      : {'#' : 9, 'Type' : 'R*4', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :     0.0},
                'TEST_NAM' : {'#' :10, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :      ''}
            }
        else:
            raise STDFError("%s object creation error: unsupported version '%s'" % (self.id, version))
        self._default_init(endian, record)

class EPS(STDR):
    def __init__(self, version=None, endian=None, record=None):
        self.id = 'EPS'
        self.local_debug = False
        # Version
        if version==None or version=='V4' or version=='V3':
            self.version = version
            self.info = '''
End Program Section Record
--------------------------

Function:
    Marks the end of the current program section (or sequencer) in the job plan.

Frequency:
    * Optional on each exit from the program segment.

Location:
    Following the corresponding BPS and before the PRR in the data stream.
'''
            self.fields = {
                'REC_LEN'  : {'#' :  0, 'Type' :  'U*2', 'Ref' :         '', 'Value' :      0, 'Text' : 'Bytes of data following header        ', 'Missing' : 'N/A                    '},
                'REC_TYP'  : {'#' :  1, 'Type' :  'U*1', 'Ref' :         '', 'Value' :     20, 'Text' : 'Record type                           ', 'Missing' : '20                     '},
                'REC_SUB'  : {'#' :  2, 'Type' :  'U*1', 'Ref' :         '', 'Value' :     20, 'Text' : 'Record sub-type                       ', 'Missing' : '10                     '}
            }
        else:
            raise STDFError("%s object creation error: unsupported version '%s'" % (self.id, version))
        self._default_init(endian, record)

class ETSR(STDR):
    def __init__(self, version=None, endian=None, record=None):
        self.id = 'ETSR'
        self.local_debug = False
        # Version
        if version==None or version=='V3':
            self.version = 'V3'
            self.info = '''
?!?
-------------------

Function:
    ?!?
Frequency:
    ?!?

Location:
    ?!?
'''
            self.fields = {
                'REC_LEN'    : {'#' :  0, 'Type' : 'U*2', 'Ref' : None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' :    None},
                'REC_TYP'    : {'#' :  1, 'Type' : 'U*1', 'Ref' : None, 'Value' :  220, 'Text' : 'Record type                           ', 'Missing' :    None},
                'REC_SUB'    : {'#' :  2, 'Type' : 'U*1', 'Ref' : None, 'Value' :  203, 'Text' : 'Record sub-type                       ', 'Missing' :    None},
                'TEST_NUM'   : {'#' :  3, 'Type' : 'U*4', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :       0},
                'EXEC_CNT'   : {'#' :  4, 'Type' : 'I*4', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :       0},
                'FAIL_CNT'   : {'#' :  5, 'Type' : 'I*4', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :       0},
                'ALRM_CNT'   : {'#' :  6, 'Type' : 'I*4', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :       0},
                'OPT_FLAG_QU': {'#' :  7, 'Type' : 'B*1', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' : ['0']*8},
                'TEST_05'    : {'#' :  8, 'Type' : 'R*4', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :     0.0},
                'TEST_10'    : {'#' :  9, 'Type' : 'R*4', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :     0.0},
                'TEST_50'    : {'#' : 10, 'Type' : 'R*4', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :     0.0},
                'TEST_90'    : {'#' : 11, 'Type' : 'R*4', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :     0.0},
                'TEST_95'    : {'#' : 12, 'Type' : 'R*4', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :     0.0},
                'OPT_FLAG'   : {'#' : 13, 'Type' : 'B*1', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' : ['0']*8},
                'PAD_BYTE'   : {'#' : 14, 'Type' : 'B*1', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' : ['0']*8},
                'TEST_MIN'   : {'#' : 15, 'Type' : 'R*4', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :     0.0},
                'TEST_MAX'   : {'#' : 16, 'Type' : 'R*4', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :     0.0},
                'TST_MEAN'   : {'#' : 17, 'Type' : 'R*4', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :     0.0},
                'TST_SDEV'   : {'#' : 18, 'Type' : 'R*4', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :     0.0},
                'TST_SUMS'   : {'#' : 19, 'Type' : 'R*4', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :     0.0},
                'TST_SQRS'   : {'#' : 20, 'Type' : 'R*4', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :     0.0},
                'TEST_NAM'   : {'#' : 21, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :      ''},
                'SEQ_NAME'   : {'#' : 22, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :      ''}
            }
        else:
            raise STDFError("%s object creation error: unsupported version '%s'" % (self.id, version))
        self._default_init(endian, record)


class FDR(STDR):
    def __init__(self, version=None, endian=None, record = None):
        self.id = 'FDR'
        self.local_debug = False
        if version==None or version=='V3':
            self.version = 'V3'
            self.info=    '''
Functional Test Description Record
----------------------------------

Function:
    ?!?

Frequency:
    ?!?

Location:
    ?!?
'''
            self.fields = {
                'REC_LEN'  : {'#' : 0, 'Type' : 'U*2', 'Ref' : None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' :    None},
                'REC_TYP'  : {'#' : 1, 'Type' : 'U*1', 'Ref' : None, 'Value' :   10, 'Text' : 'Record type                           ', 'Missing' :    None},
                'REC_SUB'  : {'#' : 2, 'Type' : 'U*1', 'Ref' : None, 'Value' :   20, 'Text' : 'Record sub-type                       ', 'Missing' :    None},
                'TEST_NUM' : {'#' : 3, 'Type' : 'U*4', 'Ref' : None, 'Value' : None, 'Text' : 'Test number                           ', 'Missing' :       0},
                'DESC_FLG' : {'#' : 4, 'Type' : 'B*1', 'Ref' : None, 'Value' : None, 'Text' : 'Description flags                     ', 'Missing' : ['0']*8},
                'TEST_NAM' : {'#' : 5, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : 'Test name                             ', 'Missing' :      ''},
                'SEQ_NAME' : {'#' : 6, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : 'Sequencer (program segment/flow) name ', 'Missing' :      ''}
            }
        else:
            raise STDFError("%s object creation error: unsupported version '%s'" % (self.id, version))
        self._default_init(endian, record)

class FSR(STDR):
    def __init__(self, version=None, endian=None, record = None):
        self.id = 'FSR'
        self.local_debug = False
        if version==None or version == 'V4':
            self.version = 'V4'
            self.info=    '''
Frame Specification Record (V4, Memory:2010.1)
----------------------------------------------

Function:
    Frame Specification Record (FSR) is used to define a frame structure that can be used to store the fail data in a frame format.
    In most of the embedded memory test architecture available in the industry, the data is communicated from the BIST controllers
    to ATE in a serial frame format. Each vendor has its own frame format. So to deal with different frame format from various vendors
    the FSR allows encapsulating one or more specific frame definitions used within the STDF file.

Frequency:
    * Once per memory Algorithm

Location:
    It can occur after all the Memory Model Records(MMRs) and before any Test specific records e.g. Parametric Test Record (PTR),
    Functional Test Record (FTRs), Scan Test Record (STR) and Memory Test Record (MTRs).
'''
            self.fields = {
                'REC_LEN'  : {'#' :  0, 'Type' : 'U*2', 'Ref' : None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' : None},
                'REC_TYP'  : {'#' :  1, 'Type' : 'U*1', 'Ref' : None, 'Value' :    0, 'Text' : 'Record type                           ', 'Missing' : None},
                'REC_SUB'  : {'#' :  2, 'Type' : 'U*1', 'Ref' : None, 'Value' :   20, 'Text' : 'Record sub-type                       ', 'Missing' : None},
                'BSR_IDX'  : {'#' :  2, 'Type' : 'U*2', 'Ref' : None, 'Value' : None, 'Text' : 'Unique ID this Bit stream spec.       ', 'Missing' :    0},
                'BIT_TYP'  : {'#' :  2, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : 'Meaning of bits in the stream         ', 'Missing' :    0},
                'ADDR_SIZ' : {'#' :  2, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : 'Address field size [1,2,4 & 8] are ok ', 'Missing' :    0},
                'WC_SIZ'   : {'#' :  2, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : 'Word Count Field Size [1,2,4 & 8]     ', 'Missing' :    0},
                'WRD_SIZ'  : {'#' :  2, 'Type' : 'U*2', 'Ref' : None, 'Value' : None, 'Text' : 'Number of bits in word field          ', 'Missing' :    0}
            }
        else:
            raise STDFError("%s object creation error: unsupported version '%s'" % (self.id, version))
        self._default_init(endian, record)

class FTR(STDR):
    def __init__(self, version=None, endian=None, record=None):
        self.id = 'FTR'
        self.local_debug = False
        if version==None or version=='V4':
            self.version = 'V4'
            self.info = '''
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
'''
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
        elif version == 'V3':
            self.version = 'V3'
            self.info = '''
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
'''
            self.fields = {
                'REC_LEN'  : {'#' :  0, 'Type' : 'U*2', 'Ref' : None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' :    None},
                'REC_TYP'  : {'#' :  1, 'Type' : 'U*1', 'Ref' : None, 'Value' :   15, 'Text' : 'Record type                           ', 'Missing' :    None},
                'REC_SUB'  : {'#' :  2, 'Type' : 'U*1', 'Ref' : None, 'Value' :   20, 'Text' : 'Record sub-type                       ', 'Missing' :    None},
                'TEST_NUM' : {'#' :  3, 'Type' : 'U*4', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :    None}, # Obligatory
                'HEAD_NUM' : {'#' :  4, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :       0},
                'SITE_NUM' : {'#' :  5, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :       0},
                'TEST_FLG' : {'#' :  6, 'Type' : 'B*1', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' : ['0']*8},
                'DESC_FLG' : {'#' :  7, 'Type' : 'B*1', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' : ['0']*8},
                'OPT_FLAG' : {'#' :  8, 'Type' : 'B*1', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' : ['0']*8},
                'TIME_SET' : {'#' :  9, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :       0},
                'VECT_ADR' : {'#' : 10, 'Type' : 'U*4', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :       0},
                'CYCL_CNT' : {'#' : 11, 'Type' : 'U*4', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :       0},
                'REPT_CNT' : {'#' : 12, 'Type' : 'U*2', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :       0},
                'PCP_ADR'  : {'#' : 13, 'Type' : 'U*2', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :       0},
                'NUM_FAIL' : {'#' : 14, 'Type' : 'U*4', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :       0},
                'FAIL_PIN' : {'#' : 15, 'Type' : 'B*n', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :      []},
                'VECT_DAT' : {'#' : 16, 'Type' : 'B*n', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :      []},
                'DEV_DAT'  : {'#' : 17, 'Type' : 'B*n', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :      []},
                'RPIN_MAP' : {'#' : 18, 'Type' : 'B*n', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :      []},
                'TEST_NAM' : {'#' : 19, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :      ''},
                'SEQ_NAME' : {'#' : 20, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :      ''},
                'TEST_TXT' : {'#' : 21, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :      ''}
            }
        else:
            raise STDFError("%s object creation error: unsupported version '%s'" % (self.id, version))
        self._default_init(endian, record)

class GDR(STDR):
    def __init__(self, version=None, endian=None, record=None):
        self.id = 'GDR'
        self.local_debug = False
        if version==None or version=='V4' or version=='V3':
            if version==None: self.version='V4'
            else: self.version=version
            self.info = '''
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
'''
            self.fields = {
                'REC_LEN'  : {'#' : 0, 'Type' :  'U*2', 'Ref' :      None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' : None},
                'REC_TYP'  : {'#' : 1, 'Type' :  'U*1', 'Ref' :      None, 'Value' :   50, 'Text' : 'Record type                           ', 'Missing' : None},
                'REC_SUB'  : {'#' : 2, 'Type' :  'U*1', 'Ref' :      None, 'Value' :   10, 'Text' : 'Record sub-type                       ', 'Missing' : None},
                'FLD_CNT'  : {'#' : 3, 'Type' :  'U*2', 'Ref' :      None, 'Value' : None, 'Text' : 'Count of data fields in record        ', 'Missing' :    0},
                'GEN_DATA' : {'#' : 4, 'Type' : 'xV*n', 'Ref' : 'FLD_CNT', 'Value' : None, 'Text' : 'Data type code and data for one field ', 'Missing' :   []}
            }
        else:
            raise STDFError("%s object creation error: unsupported version '%s'" % (self.id, version))
        self._default_init(endian, record)

class GTR(STDR):
    def __init__(self, version=None, endian=None, record=None):
        self.id = 'GTR'
        self.local_debug = False
        if version==None or version=='V3':
            self.version='V3'
            self.info = '''
?!?
-------------------

Function:

Frequency:

Location:
'''
            self.fields = {
                'REC_LEN'   : {'#' : 0, 'Type' : 'U*2',  'Ref' : None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' :               None},
                'REC_TYP'   : {'#' : 1, 'Type' : 'U*1',  'Ref' : None, 'Value' :  220, 'Text' : 'Record type                           ', 'Missing' :               None},
                'REC_SUB'   : {'#' : 2, 'Type' : 'U*1',  'Ref' : None, 'Value' :  204, 'Text' : 'Record sub-type                       ', 'Missing' :               None},
                'TEXT_NAME' : {'#' : 3, 'Type' : 'C*16', 'Ref' : None, 'Value' : None, 'Text' : 'Count of data fields in record        ', 'Missing' : '                '},
                'TEXT_VAL'  : {'#' : 4, 'Type' : 'C*n',  'Ref' : None, 'Value' : None, 'Text' : 'Data type code and data for one field ', 'Missing' :                 ''}
            }
        else:
            raise STDFError("%s object creation error: unsupported version '%s'" % (self.id, version))
        self._default_init(endian, record)


class IDR(STDR):
    def __init__(self, version=None, endian=None, record = None):
        self.id = 'IDR'
        self.local_debug = False
        if version==None or version=='V4':
            self.version = 'V4'
            self.info=    '''
Instance Description Record (V4, Memory:2010.1)
-----------------------------------------------

Function:
    This record is used to store the information for a memory instance within a design. It contains a
    reference to the model records which define the design information for this specific memory instance.

Frequency:
    * Once per memory instance

Location:
    It can occur after all the Memory Controller Records(MCRs) and before Memory Model Records (MMRs)
'''
            self.fields = {
                'REC_LEN'  : {'#' :  0, 'Type' : 'U*2', 'Ref' : None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' : None},
                'REC_TYP'  : {'#' :  1, 'Type' : 'U*1', 'Ref' : None, 'Value' :    0, 'Text' : 'Record type                           ', 'Missing' : None},
                'REC_SUB'  : {'#' :  2, 'Type' : 'U*1', 'Ref' : None, 'Value' :   20, 'Text' : 'Record sub-type                       ', 'Missing' : None},
                'INST_IDX' : {'#' :  3, 'Type' : 'U*2', 'Ref' : None, 'Value' : None, 'Text' : 'Unique index of this IDR              ', 'Missing' : None}, # Obligatory
                'INST_NAM' : {'#' :  4, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : 'Name of the Instance                  ', 'Missing' :   ''},
                'REF_COD'  : {'#' :  5, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : '0=Wafer Notch based, 1=Pkg ref        ', 'Missing' : None},
                'ORNT_COD' : {'#' :  6, 'Type' : 'C*2', 'Ref' : None, 'Value' : None, 'Text' : 'Orientation of Instance               ', 'Missing' : '  '},
                'MDL_FILE' : {'#' :  7, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : 'Pointer to file describing model      ', 'Missing' :   ''},
                'MDL_REF'  : {'#' :  8, 'Type' : 'U*2', 'Ref' : None, 'Value' : None, 'Text' : 'Reference to the model record         ', 'Missing' : None}
            }
        else:
            raise STDFError("%s object creation error: unsupported version '%s'" % (self.id, version))
        self._default_init(endian, record)

class MCR(STDR):
    def __init__(self, version=None, endian=None, record = None):
        self.id = 'MCR'
        self.local_debug = False
        if version == 'V4':
            self.version = version
            self.info=    '''
Memory Controller Record (V4, Memory:2010.1)
--------------------------------------------

Function:
    This record is used to store information about an embedded memory controller in a design.
    There is one MCR record in an STDF file for each controller in a design.
    These records are referenced by the top level Memory Structure Record (MSR) through its CTRL_LST field.

Frequency:
    * Once per controller in the design.

Location:
    It can occur after all the Memory Structure Records(MSRs) and before Instance Description Records (IDRs)
'''
            self.fields = {
                'REC_LEN'  : {'#' :  0, 'Type' : 'U*2' , 'Ref' :       None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' : None},
                'REC_TYP'  : {'#' :  1, 'Type' : 'U*1' , 'Ref' :       None, 'Value' :    1, 'Text' : 'Record type                           ', 'Missing' : None},
                'REC_SUB'  : {'#' :  2, 'Type' : 'U*1' , 'Ref' :       None, 'Value' :  100, 'Text' : 'Record sub-type                       ', 'Missing' : None},
                'CTRL_IDX' : {'#' :  3, 'Type' : 'U*2' , 'Ref' :       None, 'Value' : None, 'Text' : 'Index of this memory controller record', 'Missing' : None},
                'CTRL_NAM' : {'#' :  4, 'Type' : 'C*n' , 'Ref' :       None, 'Value' : None, 'Text' : 'Name of the controller                ', 'Missing' :   ''},
                'MDL_FILE' : {'#' :  5, 'Type' : 'C*n' , 'Ref' :       None, 'Value' : None, 'Text' : 'Pointer to the file describing model  ', 'Missing' :   ''},
                'INST_CNT' : {'#' :  6, 'Type' : 'U*2' , 'Ref' :       None, 'Value' : None, 'Text' : 'Count of INST_INDX array              ', 'Missing' :    0},
                'INST_LST' : {'#' :  7, 'Type' : 'xU*2', 'Ref' : 'INST_CNT', 'Value' : None, 'Text' : 'Array of memory instance indexes      ', 'Missing' :   []}
            }
        else:
            raise STDFError("%s object creation error: unsupported version '%s'" % (self.id, version))
        self._default_init(endian, record)


class MMR(STDR):
    def __init__(self, version=None, endian=None, record = None):
        self.id = 'MMR'
        self.local_debug = False
        if version==None or version=='V4':
            self.version = 'V4'
            self.info=    '''
Memory Model Record (V4, Memory:2010.1)
---------------------------------------

Function:
    This record is used to store the memory model information in STDF.
    The record allows storing the logic level information of the model.
    It does not have any fields to store the physical information except height and width.
    The physical information can be optionally linked to the record through a reference to the file.

Frequency:
    Once per memory model.

Location:
    It can occur after all the Instance Description Records(IDRs) and before any Frame Specification Records (FSRs),
    Bit Stream Specification Records (BSRs) and any Test specific records e.g. Parametric Test Record (PTR),
    Functional Test Record (FTRs), Scan Test Record (STR) and Memory Test Record (MTRs).
'''
            self.fields = {
                'REC_LEN'  : {'#' :  0, 'Type' : 'U*2',  'Ref' :       None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' : None},
                'REC_TYP'  : {'#' :  1, 'Type' : 'U*1',  'Ref' :       None, 'Value' :    1, 'Text' : 'Record type                           ', 'Missing' : None},
                'REC_SUB'  : {'#' :  2, 'Type' : 'U*1',  'Ref' :       None, 'Value' :   95, 'Text' : 'Record sub-type                       ', 'Missing' : None},
                'ASR_IDX'  : {'#' :  3, 'Type' : 'U*2',  'Ref' :       None, 'Value' : None, 'Text' : 'Unique identifier for this ASR record ', 'Missing' : None},
                'STRT_IDX' : {'#' :  4, 'Type' : 'U*1',  'Ref' :       None, 'Value' : None, 'Text' : 'Cycle Start index flag                ', 'Missing' : None},
                'ALGO_CNT' : {'#' :  5, 'Type' : 'U*1',  'Ref' :       None, 'Value' : None, 'Text' : 'count (k) of Algorithms descriptions  ', 'Missing' :    0},
                'ALGO_NAM' : {'#' :  6, 'Type' : 'xC*n', 'Ref' : 'ALGO_CNT', 'Value' : None, 'Text' : 'Array of Names Name of the Algorithm  ', 'Missing' :   []},
                'ALGO_LEN' : {'#' :  7, 'Type' : 'xC*n', 'Ref' : 'ALGO_CNT', 'Value' : None, 'Text' : 'Array of Complexity of algorithm      ', 'Missing' :   []},
                'FILE_ID'  : {'#' :  8, 'Type' : 'xC*n', 'Ref' : 'ALGO_CNT', 'Value' : None, 'Text' : 'Array of Name of the file with descr. ', 'Missing' :   []},
                'CYC_BGN'  : {'#' :  9, 'Type' : 'xU*8', 'Ref' : 'ALGO_CNT', 'Value' : None, 'Text' : 'Array of Starting cycle number        ', 'Missing' :   []},
                'CYC_END'  : {'#' : 10, 'Type' : 'xU*8', 'Ref' : 'ALGO_CNT', 'Value' : None, 'Text' : 'Array of End Cycle number             ', 'Missing' :   []}
            }
        else:
            raise STDFError("%s object creation error: unsupported version '%s'" % (self.id, version))
        self._default_init(endian, record)

class MPR(STDR):
    def __init__(self, version=None, endian=None, record=None):
        self.id = 'MPR'
        self.local_debug = False
        if version==None or version == 'V4':
            self.version ='V4'
            self.info = '''
Multiple-Result Parametric Record
---------------------------------

Function:
    Contains the results of a single execution of a parametric test in the test program
    where that test returns multiple values. The first occurrence of this record also
    establishes the default values for all semi-static information about the test, such as
    limits, units, and scaling. The MPR is related to the Test Synopsis Record (TSR) by test
    number, head number, and site number.

Frequency:
    * Obligatory, one per multiple-result parametric test execution on each head/site

Location:
    Anywhere in the data stream after the corresponding Part Information Record (PIR)
    and before the corresponding Part Result Record (PRR).
'''
            self.fields = {
                'REC_LEN'  : {'#' :  0, 'Type' : 'U*2',  'Ref' :       None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' :                                     None},
                'REC_TYP'  : {'#' :  1, 'Type' : 'U*1',  'Ref' :       None, 'Value' :   15, 'Text' : 'Record type                           ', 'Missing' :                                     None},
                'REC_SUB'  : {'#' :  2, 'Type' : 'U*1',  'Ref' :       None, 'Value' :   15, 'Text' : 'Record sub-type                       ', 'Missing' :                                     None},
                'TEST_NUM' : {'#' :  3, 'Type' : 'U*4',  'Ref' :       None, 'Value' : None, 'Text' : 'Test number                           ', 'Missing' :                                     None},
                'HEAD_NUM' : {'#' :  4, 'Type' : 'U*1',  'Ref' :       None, 'Value' : None, 'Text' : 'Test head number                      ', 'Missing' :                                        1},
                'SITE_NUM' : {'#' :  5, 'Type' : 'U*1',  'Ref' :       None, 'Value' : None, 'Text' : 'Test site number                      ', 'Missing' :                                        1},
                'TEST_FLG' : {'#' :  6, 'Type' : 'B*1',  'Ref' :       None, 'Value' : None, 'Text' : 'Test flags (fail, alarm, etc.)        ', 'Missing' :                                  ['0']*8},
                'PARM_FLG' : {'#' :  7, 'Type' : 'B*1',  'Ref' :       None, 'Value' : None, 'Text' : 'Parametric test flags (drift, etc.)   ', 'Missing' : ['1', '1', '0', '0', '0', '0', '0', '0']}, # 0xC0
                'RTN_ICNT' : {'#' :  8, 'Type' : 'U*2',  'Ref' :       None, 'Value' : None, 'Text' : 'Count (j) of PMR indexes              ', 'Missing' :                                        0},
                'RSLT_CNT' : {'#' :  9, 'Type' : 'U*2',  'Ref' :       None, 'Value' : None, 'Text' : 'Count (k) of returned results         ', 'Missing' :                                        0},
                'RTN_STAT' : {'#' : 10, 'Type' : 'xN*1', 'Ref' : 'RTN_ICNT', 'Value' : None, 'Text' : 'Array of j returned states            ', 'Missing' :                                       []}, # RTN_ICNT = 0
                'RTN_RSLT' : {'#' : 11, 'Type' : 'xR*4', 'Ref' : 'RSLT_CNT', 'Value' : None, 'Text' : 'Array of k returned results           ', 'Missing' :                                       []}, # RSLT_CNT = 0
                'TEST_TXT' : {'#' : 12, 'Type' : 'C*n',  'Ref' :       None, 'Value' : None, 'Text' : 'Descriptive text or label             ', 'Missing' :                                       ''},
                'ALARM_ID' : {'#' : 13, 'Type' : 'C*n',  'Ref' :       None, 'Value' : None, 'Text' : 'Name of alarm                         ', 'Missing' :                                       ''},
                'OPT_FLAG' : {'#' : 14, 'Type' : 'B*1',  'Ref' :       None, 'Value' : None, 'Text' : 'Optional data flag See note           ', 'Missing' : ['0', '0', '0', '0', '0', '0', '1', '0']}, # 0x02
                'RES_SCAL' : {'#' : 15, 'Type' : 'I*1',  'Ref' :       None, 'Value' : None, 'Text' : 'Test result scaling exponent          ', 'Missing' :                                        0}, # OPT_FLAG bit 0 = 1
                'LLM_SCAL' : {'#' : 16, 'Type' : 'I*1',  'Ref' :       None, 'Value' : None, 'Text' : 'Test low limit scaling exponent       ', 'Missing' :                                        0}, # OPT_FLAG bit 4 or 6 = 1
                'HLM_SCAL' : {'#' : 17, 'Type' : 'I*1',  'Ref' :       None, 'Value' : None, 'Text' : 'Test high limit scaling exponent      ', 'Missing' :                                        0}, # OPT_FLAG bit 5 or 7 = 1
                'LO_LIMIT' : {'#' : 18, 'Type' : 'R*4',  'Ref' :       None, 'Value' : None, 'Text' : 'Test low limit value                  ', 'Missing' :                                      0.0}, # OPT_FLAG bit 4 or 6 = 1
                'HI_LIMIT' : {'#' : 19, 'Type' : 'R*4',  'Ref' :       None, 'Value' : None, 'Text' : 'Test high limit value                 ', 'Missing' :                                      0.0}, # OPT_FLAG bit 5 or 7 = 1
                'START_IN' : {'#' : 20, 'Type' : 'R*4',  'Ref' :       None, 'Value' : None, 'Text' : 'Starting input value [condition]      ', 'Missing' :                                      0.0}, # OPT_FLAG bit 1 = 1
                'INCR_IN'  : {'#' : 21, 'Type' : 'R*4',  'Ref' :       None, 'Value' : None, 'Text' : 'Increment of input condition          ', 'Missing' :                                       -1}, # OPT_FLAG bit 1 = 1
                'RTN_INDX' : {'#' : 22, 'Type' : 'xU*2', 'Ref' : 'RTN_ICNT', 'Value' : None, 'Text' : 'Array of j PMR indexes                ', 'Missing' :                                       []}, # RTN_ICNT = 0
                'UNITS'    : {'#' : 23, 'Type' : 'C*n',  'Ref' :       None, 'Value' : None, 'Text' : 'Units of returned results             ', 'Missing' :                                       ''},
                'UNITS_IN' : {'#' : 24, 'Type' : 'C*n',  'Ref' :       None, 'Value' : None, 'Text' : 'Input condition units                 ', 'Missing' :                                       ''},
                'C_RESFMT' : {'#' : 25, 'Type' : 'C*n',  'Ref' :       None, 'Value' : None, 'Text' : 'ANSI C result format string           ', 'Missing' :                                       ''},
                'C_LLMFMT' : {'#' : 26, 'Type' : 'C*n',  'Ref' :       None, 'Value' : None, 'Text' : 'ANSI C low limit format string        ', 'Missing' :                                       ''},
                'C_HLMFMT' : {'#' : 27, 'Type' : 'C*n',  'Ref' :       None, 'Value' : None, 'Text' : 'ANSI C high limit format string       ', 'Missing' :                                       ''},
                'LO_SPEC'  : {'#' : 28, 'Type' : 'R*4',  'Ref' :       None, 'Value' : None, 'Text' : 'Low specification limit value         ', 'Missing' :                                      0.0}, # OPT_FLAG bit 2 = 1
                'HI_SPEC'  : {'#' : 29, 'Type' : 'R*4',  'Ref' :       None, 'Value' : None, 'Text' : 'High specification limit value        ', 'Missing' :                                      0.0}  # OPT_FLAG bit 3 = 1
            }
        else:
            raise STDFError("%s object creation error: unsupported version '%s'" % (self.id, version))
        self._default_init(endian, record)


class MSR(STDR):
    def __init__(self, version=None, endian=None, record = None):
        self.id = 'MSR'
        self.local_debug = False
        if version == 'V4':
            self.version = 'V4'
            self.info=    '''
Memory Structure Record (V4, Memory:2010.1)
-------------------------------------------

Function:
    This record is the top level record for storing Memory design information.
    It supports both the direct access memories as well as the embedded memories controlled by
    embedded controllers. For embedded memories it contains the references to the controllers
    and for direct access memories it contains the references to the memory instances.

Frequency:
    * One for each STDF file for a design

Location:
    It can occur anytime after Retest Data Record (RDR) if no Site Description Record(s)
    are present, otherwise after all the SDRs. This record must occur before Memory Controller
    Records (MCRs) and Instance Description Records (IDRs)
'''
            self.fields = {
                'REC_LEN'  : {'#' : 0, 'Type' :  'U*2', 'Ref' :       None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' : None},
                'REC_TYP'  : {'#' : 1, 'Type' :  'U*1', 'Ref' :       None, 'Value' :    1, 'Text' : 'Record type                           ', 'Missing' : None},
                'REC_SUB'  : {'#' : 2, 'Type' :  'U*1', 'Ref' :       None, 'Value' :   99, 'Text' : 'Record sub-type                       ', 'Missing' : None},
                'NAME'     : {'#' : 3, 'Type' :  'C*n', 'Ref' :       None, 'Value' : None, 'Text' : 'Name of the design under test         ', 'Missing' :   ''},
                'FILE_NAM' : {'#' : 4, 'Type' :  'C*n', 'Ref' :       None, 'Value' : None, 'Text' : 'Filename containing design information', 'Missing' :   ''},
                'CTRL_CNT' : {'#' : 5, 'Type' :  'U*2', 'Ref' :       None, 'Value' : None, 'Text' : 'Count (k) of controllers in the design', 'Missing' :    0},
                'CTRL_LST' : {'#' : 6, 'Type' : 'xU*2', 'Ref' : 'CTRL_CNT', 'Value' : None, 'Text' : 'Array of controller record indexes    ', 'Missing' :   []},
                'INST_CNT' : {'#' : 7, 'Type' :  'U*2', 'Ref' :       None, 'Value' : None, 'Text' : 'Count(m) of Top level memory instances', 'Missing' :    0},
                'INST_LST' : {'#' : 8, 'Type' : 'xU*2', 'Ref' : 'INST_CNT', 'Value' : None, 'Text' : 'Array of Instance record indexes      ', 'Missing' :   []}
            }
        else:
            raise STDFError("%s object creation error: unsupported version '%s'" % (self.id, version))
        self._default_init(endian, record)

class MTR(STDR):
    def __init__(self, version=None, endian=None, record=None,  BSR__ADDR_SIZ=None, BSR__WC_SIZ=None):
        self.id = 'MTR'
        self.local_debug = False
        if version == 'V4':
            self.version = version
            self.info=    '''
Memory Test Record (V4, Memory:2010.1)
--------------------------------------

Function:
    This is the record is used to store fail data along with capture test conditions and references to test test descriptions.
    It allows the fail data to be stored in various formats describe below using the field highlighting

Frequency:
    Number of memory tests times records required to log the fails for the test (counting continuation record)

Location:
    It can occur after all the memory design specific records i.e. any Memory Structure Record (MSR),
    any Memory Controller Records (MCRs), any Memory Instance Records (IDRs), any Memory Model Records(MMRs),
    any Algorithms Specification Records (ASRs), any Frame Specification Records (FSRs) and any Bitstream Specificaion Records (BSRs)
'''
            #TODO: Implement "Field Presense Expression" (see PTR record on how)
            self.fields = {
                'REC_LEN'   : {'#' :  0, 'Type' :  'U*2', 'Ref' :                     None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' :    None},
                'REC_TYP'   : {'#' :  1, 'Type' :  'U*1', 'Ref' :                     None, 'Value' :   15, 'Text' : 'Record type                           ', 'Missing' :    None},
                'REC_SUB'   : {'#' :  2, 'Type' :  'U*1', 'Ref' :                     None, 'Value' :   40, 'Text' : 'Record sub-type                       ', 'Missing' :    None},
                'CONT_FLG'  : {'#' :  3, 'Type' :  'B*1', 'Ref' :                     None, 'Value' : None, 'Text' : 'Continuation flag                     ', 'Missing' :    None},
                'TEST_NUM'  : {'#' :  4, 'Type' :  'U*4', 'Ref' :                     None, 'Value' : None, 'Text' : 'Test number                           ', 'Missing' :    None},
                'HEAD_NUM'  : {'#' :  5, 'Type' :  'U*1', 'Ref' :                     None, 'Value' : None, 'Text' : 'Test head number                      ', 'Missing' :       1},
                'SITE_NUM'  : {'#' :  6, 'Type' :  'U*1', 'Ref' :                     None, 'Value' : None, 'Text' : 'Test site number                      ', 'Missing' :       1},
                'ASR_REF'   : {'#' :  7, 'Type' :  'U*2', 'Ref' :                     None, 'Value' : None, 'Text' : 'ASR Index                             ', 'Missing' :    None},
                'TEST_FLG'  : {'#' :  8, 'Type' :  'B*1', 'Ref' :                     None, 'Value' : None, 'Text' : 'Test flags (fail, alarm, etc.)        ', 'Missing' : ['0']*8},
                'LOG_TYP'   : {'#' :  9, 'Type' :  'C*n', 'Ref' :                     None, 'Value' : None, 'Text' : 'User defined description of datalog   ', 'Missing' :      ''},
                'TEST_TXT'  : {'#' : 10, 'Type' :  'C*n', 'Ref' :                     None, 'Value' : None, 'Text' : 'Descriptive text or label             ', 'Missing' :      ''},
                'ALARM_ID'  : {'#' : 11, 'Type' :  'C*n', 'Ref' :                     None, 'Value' : None, 'Text' : 'Name of alarm                         ', 'Missing' :      ''},
                'PROG_TXT'  : {'#' : 12, 'Type' :  'C*n', 'Ref' :                     None, 'Value' : None, 'Text' : 'Additional Programmed information     ', 'Missing' :      ''},
                'RSLT_TXT'  : {'#' : 13, 'Type' :  'C*n', 'Ref' :                     None, 'Value' : None, 'Text' : 'Additional result information         ', 'Missing' :      ''},
                'COND_CNT'  : {'#' : 14, 'Type' :  'U*2', 'Ref' :                     None, 'Value' : None, 'Text' : 'Count (k) of conditions               ', 'Missing' :       0},
                'COND_LST'  : {'#' : 15, 'Type' : 'xC*n', 'Ref' :               'COND_CNT', 'Value' : None, 'Text' : 'Array of Conditions                   ', 'Missing' :      []},
                'CYC_CNT'   : {'#' : 16, 'Type' :  'U*8', 'Ref' :                     None, 'Value' : None, 'Text' : 'Total cycles executed during the test ', 'Missing' :       0},
                'TOTF_CNT'  : {'#' : 17, 'Type' :  'U*8', 'Ref' :                     None, 'Value' : None, 'Text' : 'Total fails during the test           ', 'Missing' :       0},
                'TOTL_CNT'  : {'#' : 18, 'Type' :  'U*8', 'Ref' :                     None, 'Value' : None, 'Text' : 'Total fails during the complete MTR   ', 'Missing' :       0},
                'OVFL_FLG'  : {'#' : 19, 'Type' :  'B*1', 'Ref' :                     None, 'Value' : None, 'Text' : 'Failure Flag                          ', 'Missing' : ['0']*8},
                'FILE_INC'  : {'#' : 20, 'Type' :  'B*1', 'Ref' :                     None, 'Value' : None, 'Text' : 'File incomplete                       ', 'Missing' : ['0']*8},
                'LOG_TYPE'  : {'#' : 21, 'Type' :  'B*1', 'Ref' :                     None, 'Value' : None, 'Text' : 'Type of datalog                       ', 'Missing' : ['0']*8},
                'FDIM_CNT'  : {'#' : 22, 'Type' :  'U*1', 'Ref' :                     None, 'Value' : None, 'Text' : 'Count (m) of FDIM_FNAM and FDIM_FCNT  ', 'Missing' :       0},
                'FDIM_NAM'  : {'#' : 23, 'Type' : 'xC*n', 'Ref' :               'FDIM_CNT', 'Value' : None, 'Text' : 'Array of logged Dim names             ', 'Missing' :      []},
                'FDIM_FCNT' : {'#' : 24, 'Type' : 'xU*8', 'Ref' :               'FDIM_CNT', 'Value' : None, 'Text' : 'Array of failure counts               ', 'Missing' :      []},
                'CYC_BASE'  : {'#' : 25, 'Type' :  'U*8', 'Ref' :                     None, 'Value' : None, 'Text' : 'Cycle offset to CYC_OFST array        ', 'Missing' :       0},
                'CYC_SIZE'  : {'#' : 26, 'Type' :  'U*1', 'Ref' :                     None, 'Value' : None, 'Text' : 'Size (f) of CYC_OFST [1,2,4 or 8 byes]', 'Missing' :       1},
                'PMR_SIZE'  : {'#' : 27, 'Type' :  'U*1', 'Ref' :                     None, 'Value' : None, 'Text' : 'Size (f) of PMR_ARR [1 or 2 bytes]    ', 'Missing' :       1},
                'ROW_SIZE'  : {'#' : 28, 'Type' :  'U*1', 'Ref' :                     None, 'Value' : None, 'Text' : 'Size (f) of ROW_ARR [1,2,4 or 8 bytes]', 'Missing' :       1},
                'COL_SIZE'  : {'#' : 29, 'Type' :  'U*1', 'Ref' :                     None, 'Value' : None, 'Text' : 'Size (f) of COL_ARR [1,2,4 or 8 bytes]', 'Missing' :       1},
                'DLOG_MSK'  : {'#' : 30, 'Type' :  'U*1', 'Ref' :                     None, 'Value' : None, 'Text' : 'Presence indication mask              ', 'Missing' :       0},
                'PMR_CNT'   : {'#' : 31, 'Type' :  'U*4', 'Ref' :                     None, 'Value' : None, 'Text' : 'Count (n) of pins in PMN_ARR          ', 'Missing' :       0},
                'PMR_ARR'   : {'#' : 32, 'Type' : 'xU*f', 'Ref' :  ('PMR_CNT', 'PMR_SIZE'), 'Value' : None, 'Text' : 'Array of PMR indexes for pins         ', 'Missing' :      []},
                'CYCO_CNT'  : {'#' : 33, 'Type' :  'U*4', 'Ref' :                     None, 'Value' : None, 'Text' : 'Count (n) of CYC_OFST array           ', 'Missing' :       0},
                'CYC_OFST'  : {'#' : 34, 'Type' : 'xU*f', 'Ref' : ('CYCO_CNT', 'CYC_SIZE'), 'Value' : None, 'Text' : 'Array of cycle indexes for each fail  ', 'Missing' :      []},
                'ROW_CNT'   : {'#' : 35, 'Type' :  'U*4', 'Ref' :                     None, 'Value' : None, 'Text' : 'Count (d) of ROW_ARR array            ', 'Missing' :       0},
                'ROW_ARR'   : {'#' : 36, 'Type' : 'xU*f', 'Ref' :  ('ROW_CNT', 'ROW_SIZE'), 'Value' : None, 'Text' : 'Array of row addresses for each fail  ', 'Missing' :      []},
                'COL_CNT'   : {'#' : 37, 'Type' :  'U*4', 'Ref' :                     None, 'Value' : None, 'Text' : 'Count (d) of COL_ARR array            ', 'Missing' :       0},
                'COL_ARR'   : {'#' : 38, 'Type' : 'xU*f', 'Ref' :  ('COL_CNT', 'COL_SIZE'), 'Value' : None, 'Text' : 'Array of col addresses for each fail  ', 'Missing' :      []},
                'STEP_CNT'  : {'#' : 39, 'Type' :  'U*4', 'Ref' :                     None, 'Value' : None, 'Text' : 'Count (d) STEP_ARR array              ', 'Missing' :       0},
                'STEP_ARR'  : {'#' : 40, 'Type' : 'xU*1', 'Ref' :               'STEP_CNT', 'Value' : None, 'Text' : 'Array of march steps for each fail    ', 'Missing' :      []},
                'DIM_CNT'   : {'#' : 41, 'Type' :  'U*1', 'Ref' :                     None, 'Value' : None, 'Text' : 'Number (k) of dimensions              ', 'Missing' :       0},
                'DIM_NAMS'  : {'#' : 42, 'Type' : 'xC*n', 'Ref' :                'DIM_CNT', 'Value' : None, 'Text' : 'Names of the dimensions               ', 'Missing' :      []},
                'DIM_DCNT'  : {'#' : 43, 'Type' :  'U*4', 'Ref' :                     None, 'Value' : None, 'Text' : 'Count (n) of DIM_VALS                 ', 'Missing' :       0},
                'DIM_DSIZ'  : {'#' : 44, 'Type' :  'U*1', 'Ref' :                     None, 'Value' : None, 'Text' : 'Size (f) of DIM_VALS [1,2,4or 8 bytes]', 'Missing' :       1},
                'DIM_VALS'  : {'#' : 45, 'Type' : 'xU*f', 'Ref' : ('DIM_DCNT', 'DIM_DSIZ'), 'Value' : None, 'Text' : 'Array of data values for a dimension  ', 'Missing' :      []},
                'TFRM_CNT'  : {'#' : 46, 'Type' :  'U*8', 'Ref' :                     None, 'Value' : None, 'Text' : 'Total frames in frame based logging   ', 'Missing' :       0},
                'TFSG_CNT'  : {'#' : 47, 'Type' :  'U*8', 'Ref' :                     None, 'Value' : None, 'Text' : 'Total segments across all records     ', 'Missing' :       0},
                'LFSG_CNT'  : {'#' : 48, 'Type' :  'U*2', 'Ref' :                     None, 'Value' : None, 'Text' : 'Local number of frame segments        ', 'Missing' :       0},
                'FRM_IDX'   : {'#' : 49, 'Type' :  'U*2', 'Ref' :                     None, 'Value' : None, 'Text' : 'Index of the frame record             ', 'Missing' :       0},
                'FRM_MASK'  : {'#' : 50, 'Type' :  'D*n', 'Ref' :                     None, 'Value' : None, 'Text' : 'Frame presence mask                   ', 'Missing' :      []},
                'FRM_CNT'   : {'#' : 51, 'Type' :  'U*4', 'Ref' :                     None, 'Value' : None, 'Text' : 'Count (q) of frame (curr frame & maks)', 'Missing' :       0},
                'LFBT_CNT'  : {'#' : 52, 'Type' :  'U*4', 'Ref' :                     None, 'Value' : None, 'Text' : 'Count(q) of bits stored in this record', 'Missing' :       0},
                'FRAMES'    : {'#' : 53, 'Type' :  'D*n', 'Ref' :                     None, 'Value' : None, 'Text' : 'Bit encoded data (curr FSR)           ', 'Missing' :      []},
                'TBSG_CNT'  : {'#' : 54, 'Type' :  'U*8', 'Ref' :                     None, 'Value' : None, 'Text' : 'Number of logged bit stream segments  ', 'Missing' :       0},
                'LBSG_CNT'  : {'#' : 55, 'Type' :  'U*2', 'Ref' :                     None, 'Value' : None, 'Text' : '# of bit stream segmnts in this record', 'Missing' :       0},
                'BSR_IDX'   : {'#' : 56, 'Type' :  'U*2', 'Ref' :                     None, 'Value' : None, 'Text' : 'Index of the bit stream record        ', 'Missing' :       0},
                'STRT_ADR'  : {'#' : 57, 'Type' :  'U*f', 'Ref' :            BSR__ADDR_SIZ, 'Value' : None, 'Text' : 'Start row addr in the current segment ', 'Missing' :       1},
                'WORD_CNT'  : {'#' : 58, 'Type' :  'U*f', 'Ref' :              BSR__WC_SIZ, 'Value' : None, 'Text' : 'Word count in current stream segment  ', 'Missing' :       1},
                'WORDS'     : {'#' : 59, 'Type' :  'D*n', 'Ref' :                     None, 'Value' : None, 'Text' : 'Bit encoded data for one or words     ', 'Missing' :      []},
                'TBMP_SIZE' : {'#' : 60, 'Type' :  'U*8', 'Ref' :                     None, 'Value' : None, 'Text' : 'count (k) of CBIT_MAP                 ', 'Missing' :       0},
                'LBMP_SIZE' : {'#' : 61, 'Type' :  'U*2', 'Ref' :                     None, 'Value' : None, 'Text' : 'Bytes from map in the current record  ', 'Missing' :       0},
                'CBIT_MAP'  : {'#' : 62, 'Type' : 'xU*1', 'Ref' :              'TBMP_SIZE', 'Value' : None, 'Text' : 'Compressed bit map                    ', 'Missing' :      []}
            }
        else:
            raise STDFError("%s object creation error: unsupported version '%s'" % (self.id, version))
        self._default_init(endian, record)

class NMR(STDR):
    def __init__(self, version=None, endian=None, record = None):
        self.id = 'NMR'
        self.local_debug = False
        if version==None or version=='V4':
            self.version = 'V4'
            self.info=    '''
Name Map Record (V4-2007)
-------------------------

Function:
    This record contains a map of PMR indexes to ATPG signal names.
    This record is designed to allow preservation of ATPG signal names used in the ATPG files through the datalog output.
    This record is only required when the standard PMR records do not contain the ATPG signal name.

Frequency:
    ?!?

Location:
    ?!?

'''
            self.fields = {
                'REC_LEN'  : {'#' : 0, 'Type' :  'U*2', 'Ref' :       None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' : None},
                'REC_TYP'  : {'#' : 1, 'Type' :  'U*1', 'Ref' :       None, 'Value' :    1, 'Text' : 'Record type                           ', 'Missing' : None},
                'REC_SUB'  : {'#' : 2, 'Type' :  'U*1', 'Ref' :       None, 'Value' :   91, 'Text' : 'Record sub-type                       ', 'Missing' : None},
                'CONT_FLG' : {'#' : 3, 'Type' :  'B*1', 'Ref' :       None, 'Value' : None, 'Text' : 'NMR record(s) following if not 0      ', 'Missing' :    0},
                'TOTM_CNT' : {'#' : 4, 'Type' :  'U*2', 'Ref' :       None, 'Value' : None, 'Text' : 'Count of PMR indexes (=ATPG_NAMes)    ', 'Missing' :    0},
                'LOCM_CNT' : {'#' : 5, 'Type' :  'U*2', 'Ref' :       None, 'Value' : None, 'Text' : 'Count of (k) PMR indexes              ', 'Missing' :    0},
                'PMR_INDX' : {'#' : 6, 'Type' : 'xU*2', 'Ref' : 'LOCM_CNT', 'Value' : None, 'Text' : 'Array of PMR indexes                  ', 'Missing' :   []},
                'ATPG_NAM' : {'#' : 7, 'Type' : 'xC*n', 'Ref' : 'LOCM_CNT', 'Value' : None, 'Text' : 'Array of ATPG signal names            ', 'Missing' :   []}
            }
        else:
            raise STDFError("%s object creation error: unsupported version '%s'" % (self.id, version))
        self._default_init(endian, record)


class PDR(STDR):
    def __init__(self, version=None, endian=None, record = None):
        self.id = 'PDR'
        self.local_debug = False
        if version==None or version=='V3':
            self.version = 'V3'
            self.info=    '''
Parametric test Description Record
----------------------------------

Function:
    ?!?

Frequency:
    ?!?

Location:
    ?!?
'''
            self.fields = {
                'REC_LEN'  : {'#' :  0, 'Type' : 'U*2', 'Ref' : None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' :      None},
                'REC_TYP'  : {'#' :  1, 'Type' : 'U*1', 'Ref' : None, 'Value' :   10, 'Text' : 'Record type                           ', 'Missing' :      None},
                'REC_SUB'  : {'#' :  2, 'Type' : 'U*1', 'Ref' : None, 'Value' :   10, 'Text' : 'Record sub-type                       ', 'Missing' :      None},
                'TEST_NUM' : {'#' :  3, 'Type' : 'U*4', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :      None},
                'DESC_FLG' : {'#' :  4, 'Type' : 'B*1', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :   ['0']*8},
                'OPT_FLAG' : {'#' :  5, 'Type' : 'B*1', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :   ['0']*8},
                'RES_SCAL' : {'#' :  6, 'Type' : 'I*1', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :         0},
                'UNITS'    : {'#' :  7, 'Type' : 'C*7', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' : '       '},
                'RES_LDIG' : {'#' :  8, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :         0},
                'RES_RDIG' : {'#' :  9, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :         0},
                'LLM_SCAL' : {'#' : 10, 'Type' : 'I*1', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :         0},
                'HLM_SCAL' : {'#' : 11, 'Type' : 'I*1', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :         0},
                'LLM_LDIG' : {'#' : 12, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :         0},
                'LLM_RDIG' : {'#' : 13, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :         0},
                'HLM_LDIG' : {'#' : 14, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :         0},
                'HLM_RDIG' : {'#' : 15, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :         0},
                'LO_LIMIT' : {'#' : 16, 'Type' : 'R*4', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :       0.0},
                'HI_LIMIT' : {'#' : 17, 'Type' : 'R*4', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :       0.0},
                'TEST_NAM' : {'#' : 18, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :        ''},
                'SEQ_NAME' : {'#' : 19, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'Missing' :        ''}
            }
        else:
            raise STDFError("%s object creation error: unsupported version '%s'" % (self.id, version))
        self._default_init(endian, record)

class PGR(STDR):
    def __init__(self, version=None, endian=None, record = None):
        self.id = 'PGR'
        self.local_debug = False
        if version==None or version=='V4':
            self.version = 'V4'
            self.info = '''
Pin Group Record
----------------

Function:
    Associates a name with a group of pins.

Frequency:
    * Optional
    * One per pin group defined in the test program.

Location:
    After all the PMRs whose PMR index values are listed in the PMR_INDX array of this
    record; and before the first PLR that uses this record's GRP_INDX value.
'''
            self.fields = {
                'REC_LEN'  : {'#' : 0, 'Type' :  'U*2', 'Ref' :       None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' : None},
                'REC_TYP'  : {'#' : 1, 'Type' :  'U*1', 'Ref' :       None, 'Value' :    1, 'Text' : 'Record type                           ', 'Missing' : None},
                'REC_SUB'  : {'#' : 2, 'Type' :  'U*1', 'Ref' :       None, 'Value' :   62, 'Text' : 'Record sub-type                       ', 'Missing' : None},
                'GRP_INDX' : {'#' : 3, 'Type' :  'U*2', 'Ref' :       None, 'Value' : None, 'Text' : 'Unique index associated with pin group', 'Missing' :    0},
                'GRP_NAM'  : {'#' : 4, 'Type' :  'C*n', 'Ref' :       None, 'Value' : None, 'Text' : 'Name of pin group                     ', 'Missing' :   ''},
                'INDX_CNT' : {'#' : 5, 'Type' :  'U*2', 'Ref' :       None, 'Value' : None, 'Text' : 'Count (k) of PMR indexes              ', 'Missing' :    0},
                'PMR_INDX' : {'#' : 6, 'Type' : 'xU*2', 'Ref' : 'INDX_CNT', 'Value' : None, 'Text' : 'Array of indexes for pins in the group', 'Missing' :   []}
            }
        else:
            raise STDFError("%s object creation error: unsupported version '%s'" % (self.id, version))
        self._default_init(endian, record)

class PIR(STDR):
    def __init__(self, version=None, endian=None, record = None):
        self.id = 'PIR'
        self.local_debug = False
        if version==None or version=='V4':
            self.version = 'V4'
            self.info = '''
Part Information Record
-----------------------

Function:
    Acts as a marker to indicate where testing of a particular part begins for each part
    tested by the test program. The PIR and the Part Results Record (PRR) bracket all the
    stored information pertaining to one tested part.

Frequency:
    * Obligatory
    * One per part tested.

Location:
    Anywhere in the data stream after the initial sequence "FAR-(ATRs)-MIR-(RDR)-(SDRs)", and before the corresponding PRR.
    Sent before testing each part.
'''
            self.fields = {
                'REC_LEN'  : {'#' : 0, 'Type' : 'U*2', 'Ref' : None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' : None},
                'REC_TYP'  : {'#' : 1, 'Type' : 'U*1', 'Ref' : None, 'Value' :    5, 'Text' : 'Record type                           ', 'Missing' : None},
                'REC_SUB'  : {'#' : 2, 'Type' : 'U*1', 'Ref' : None, 'Value' :   10, 'Text' : 'Record sub-type                       ', 'Missing' : None},
                'HEAD_NUM' : {'#' : 3, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : 'Test head number                      ', 'Missing' :    1},
                'SITE_NUM' : {'#' : 4, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : 'Test site number                      ', 'Missing' :    1}
            }
        elif version=='V3':
            self.version = 'V3'
            self.info = '''
Part Information Record
-----------------------

Function:
    Acts as a marker to indicate where testing of a particular part begins for each part
    tested by the test program. The PIR and the Part Results Record (PRR) bracket all the
    stored information pertaining to one tested part.

Frequency:
    * Obligatory
    * One per part tested.

Location:
    Anywhere in the data stream after the initial sequence "FAR-(ATRs)-MIR-(RDR)-(SDRs)", and before the corresponding PRR.
    Sent before testing each part.
'''
            self.fields = {
                'REC_LEN'  : {'#' : 0, 'Type' : 'U*2', 'Ref' : None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' : None},
                'REC_TYP'  : {'#' : 1, 'Type' : 'U*1', 'Ref' : None, 'Value' :    5, 'Text' : 'Record type                           ', 'Missing' : None},
                'REC_SUB'  : {'#' : 2, 'Type' : 'U*1', 'Ref' : None, 'Value' :   10, 'Text' : 'Record sub-type                       ', 'Missing' : None},
                'HEAD_NUM' : {'#' : 3, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : 'Test head number                      ', 'Missing' :    1},
                'SITE_NUM' : {'#' : 4, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : 'Test site number                      ', 'Missing' :    1},
                'X_COORD'  : {'#' : 5, 'Type' : 'I*2', 'Ref' : None, 'Value' : None, 'Text' : 'Wafer X coordinate                    ', 'Missing' :    0},
                'Y_COORD'  : {'#' : 6, 'Type' : 'I*2', 'Ref' : None, 'Value' : None, 'Text' : 'Wafer Y coordinate                    ', 'Missing' :    0},
                'PART_ID'  : {'#' : 7, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : 'Part Identification                   ', 'Missing' :   ''},
            }
        else:
            raise STDFError("%s object creation error: unsupported version '%s'" % (self.id, version))
        self._default_init(endian, record)

class PLR(STDR):
    def __init__(self, version=None, endian=None, record = None):
        self.id = 'PLR'
        self.local_debug = False
        if version==None or version=='V4':
            self.version = 'V4'
            self.info = '''
Pin List Record
---------------

Function:
    Defines the current display radix and operating mode for a pin or pin group.

Frequency:
    * Optional
    * One or more whenever the usage of a pin or pin group changes in the test program.

Location:
    After all the PMRs and PGRs whose PMR index values and pin group index values are
    listed in the GRP_INDX array of this record; and before the first FTR that references pins
    or pin groups whose modes are defined in this record.
'''
            self.fields = {
                'REC_LEN'  : {'#' :  0, 'Type' :  'U*2', 'Ref' :       None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' : None},
                'REC_TYP'  : {'#' :  1, 'Type' :  'U*1', 'Ref' :       None, 'Value' :    1, 'Text' : 'Record type                           ', 'Missing' : None},
                'REC_SUB'  : {'#' :  2, 'Type' :  'U*1', 'Ref' :       None, 'Value' :   63, 'Text' : 'Record sub-type                       ', 'Missing' : None},
                'GRP_CNT'  : {'#' :  3, 'Type' :  'U*2', 'Ref' :       None, 'Value' : None, 'Text' : 'Count (k) of pins or pin groups       ', 'Missing' :    0},
                'GRP_INDX' : {'#' :  4, 'Type' : 'xU*2', 'Ref' :  'GRP_CNT', 'Value' : None, 'Text' : 'Array of pin or pin group indexes     ', 'Missing' :   []},
                'GRP_MODE' : {'#' :  5, 'Type' : 'xU*2', 'Ref' :  'GRP_CNT', 'Value' : None, 'Text' : 'Operating mode of pin group           ', 'Missing' :   []},
                'GRP_RADX' : {'#' :  6, 'Type' : 'xU*1', 'Ref' :  'GRP_CNT', 'Value' : None, 'Text' : 'Display radix of pin group            ', 'Missing' :   []},
                'PGM_CHAR' : {'#' :  7, 'Type' : 'xC*n', 'Ref' :  'GRP_CNT', 'Value' : None, 'Text' : 'Program state encoding characters     ', 'Missing' :   []},
                'RTN_CHAR' : {'#' :  8, 'Type' : 'xC*n', 'Ref' :  'GRP_CNT', 'Value' : None, 'Text' : 'Return state encoding characters      ', 'Missing' :   []},
                'PGM_CHAL' : {'#' :  9, 'Type' : 'xC*n', 'Ref' :  'GRP_CNT', 'Value' : None, 'Text' : 'Program state encoding characters     ', 'Missing' :   []},
                'RTN_CHAL' : {'#' : 10, 'Type' : 'xC*n', 'Ref' :  'GRP_CNT', 'Value' : None, 'Text' : 'Return state encoding characters      ', 'Missing' :   []}
            }
        else:
            raise STDFError("%s object creation error: unsupported version '%s'" % (self.id, version))
        self._default_init(endian, record)


class PRR(STDR):
    def __init__(self, version=None, endian=None, record=None):
        self.id = 'PRR'
        self.local_debug = False
        if version==None or version=='V4':
            self.version = 'V4'
            self.info = '''
Part Results Record
-------------------

Function:
    Contains the result information relating to each part tested by the test program. The
    PRR and the Part Information Record (PIR) bracket all the stored information
    pertaining to one tested part.

Frequency:
    * Obligatory
    * One per part tested.

Location:
    Anywhere in the data stream after the corresponding PIR and before the MRR.
    Sent after completion of testing each part.
'''
            self.fields = {
                'REC_LEN'  : {'#' :  0, 'Type' : 'U*2', 'Ref' : None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' :                                     None},
                'REC_TYP'  : {'#' :  1, 'Type' : 'U*1', 'Ref' : None, 'Value' :    5, 'Text' : 'Record type                           ', 'Missing' :                                     None},
                'REC_SUB'  : {'#' :  2, 'Type' : 'U*1', 'Ref' : None, 'Value' :   20, 'Text' : 'Record sub-type                       ', 'Missing' :                                     None},
                'HEAD_NUM' : {'#' :  3, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : 'Test head number                      ', 'Missing' :                                        1},
                'SITE_NUM' : {'#' :  4, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : 'Test site number                      ', 'Missing' :                                        1},
                'PART_FLG' : {'#' :  5, 'Type' : 'B*1', 'Ref' : None, 'Value' : None, 'Text' : 'Part information flag                 ', 'Missing' : ['0', '0', '0', '1', '0', '0', '0', '1']},
                'NUM_TEST' : {'#' :  6, 'Type' : 'U*2', 'Ref' : None, 'Value' : None, 'Text' : 'Number of tests executed              ', 'Missing' :                                        0},
                'HARD_BIN' : {'#' :  7, 'Type' : 'U*2', 'Ref' : None, 'Value' : None, 'Text' : 'Hardware bin number                   ', 'Missing' :                                        0},
                'SOFT_BIN' : {'#' :  8, 'Type' : 'U*2', 'Ref' : None, 'Value' : None, 'Text' : 'Software bin number                   ', 'Missing' :                                    65535},
                'X_COORD'  : {'#' :  9, 'Type' : 'I*2', 'Ref' : None, 'Value' : None, 'Text' : '(Wafer) X coordinate                  ', 'Missing' :                                   -32768},
                'Y_COORD'  : {'#' : 10, 'Type' : 'I*2', 'Ref' : None, 'Value' : None, 'Text' : '(Wafer) Y coordinate                  ', 'Missing' :                                   -32768},
                'TEST_T'   : {'#' : 11, 'Type' : 'U*4', 'Ref' : None, 'Value' : None, 'Text' : 'Elapsed test time in milliseconds     ', 'Missing' :                                        0},
                'PART_ID'  : {'#' : 12, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : 'Part identification                   ', 'Missing' :                                       ''},
                'PART_TXT' : {'#' : 13, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : 'Part description text                 ', 'Missing' :                                       ''},
                'PART_FIX' : {'#' : 14, 'Type' : 'B*n', 'Ref' : None, 'Value' : None, 'Text' : 'Part repair information               ', 'Missing' :                                       []}
            }
        elif version == 'V3':
            self.version = 'V3'
            self.info = '''
Part Results Record
-------------------

Function:
    Contains the result information relating to each part tested by the test program. The
    PRR and the Part Information Record (PIR) bracket all the stored information
    pertaining to one tested part.

Frequency:
    * Obligatory
    * One per part tested.

Location:
    Anywhere in the data stream after the corresponding PIR and before the MRR.
    Sent after completion of testing each part.
'''
            self.fields = {
                'REC_LEN'  : {'#' :  0, 'Type' : 'U*2', 'Ref' : None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' :                                     None},
                'REC_TYP'  : {'#' :  1, 'Type' : 'U*1', 'Ref' : None, 'Value' :    5, 'Text' : 'Record type                           ', 'Missing' :                                     None},
                'REC_SUB'  : {'#' :  2, 'Type' : 'U*1', 'Ref' : None, 'Value' :   20, 'Text' : 'Record sub-type                       ', 'Missing' :                                     None},
                'HEAD_NUM' : {'#' :  3, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : 'Test head number                      ', 'Missing' :                                        1},
                'SITE_NUM' : {'#' :  4, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : 'Test site number                      ', 'Missing' :                                        1},
                'NUM_TEST' : {'#' :  5, 'Type' : 'U*2', 'Ref' : None, 'Value' : None, 'Text' : 'Number of tests executed              ', 'Missing' :                                        0},
                'HARD_BIN' : {'#' :  6, 'Type' : 'U*2', 'Ref' : None, 'Value' : None, 'Text' : 'Hardware bin number                   ', 'Missing' :                                        0},
                'SOFT_BIN' : {'#' :  7, 'Type' : 'U*2', 'Ref' : None, 'Value' : None, 'Text' : 'Software bin number                   ', 'Missing' :                                    65535},
                'PART_FLG' : {'#' :  8, 'Type' : 'B*1', 'Ref' : None, 'Value' : None, 'Text' : 'Part information flag                 ', 'Missing' : ['0', '0', '0', '0', '0', '0', '0', '1']},
                'PAD_BYTE' : {'#' :  9, 'Type' : 'B*1', 'Ref' : None, 'Value' : None, 'Text' : 'pad byte                              ', 'Missing' :                                  ['0']*8},
                'X_COORD'  : {'#' : 10, 'Type' : 'I*2', 'Ref' : None, 'Value' : None, 'Text' : '(Wafer) X coordinate                  ', 'Missing' :                                   -32768},
                'Y_COORD'  : {'#' : 11, 'Type' : 'I*2', 'Ref' : None, 'Value' : None, 'Text' : '(Wafer) Y coordinate                  ', 'Missing' :                                   -32768},
                'PART_ID'  : {'#' : 12, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : 'Part identification                   ', 'Missing' :                                       ''},
                'PART_TXT' : {'#' : 13, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : 'Part description text                 ', 'Missing' :                                       ''},
                'PART_FIX' : {'#' : 14, 'Type' : 'B*n', 'Ref' : None, 'Value' : None, 'Text' : 'Part repair information               ', 'Missing' :                                       []}
            }
        else:
            raise STDFError("%s object creation error: unsupported version '%s'" % (self.id, version))
        self._default_init(endian, record)

class PSR(STDR):
    def __init__(self, version=None, endian=None, record = None):
        self.id = 'PSR'
        self.local_debug = False
        if version==None or version=='V4':
            self.version = 'V4'
            self.info=    '''
Pattern Sequence Record (V4-2007)
---------------------------------

Function:
    PSR record contains the information on the pattern profile for a specific executed scan test
    as part of the Test Identification information. In particular it implements the Test Pattern
    Map data object in the data model. It specifies how the patterns for that test were constructed.
    There will be a PSR record for each scan test in a test program. A PSR is referenced by the STR
    (Scan Test Record) using its PSR_INDX field

Frequency:
    ?!?

Location:
    ?!?
'''
            self.fields = {
                'REC_LEN'  : {'#' :  0, 'Type' : 'U*2', 'Ref' :       None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' :    None},
                'REC_TYP'  : {'#' :  1, 'Type' : 'U*1', 'Ref' :       None, 'Value' :    1, 'Text' : 'Record type                           ', 'Missing' :    None},
                'REC_SUB'  : {'#' :  2, 'Type' : 'U*1', 'Ref' :       None, 'Value' :   90, 'Text' : 'Record sub-type                       ', 'Missing' :    None},
                'CONT_FLG' : {'#' :  3, 'Type' : 'B*1', 'Ref' :       None, 'Value' : None, 'Text' : 'PSR record(s) to follow if not 0      ', 'Missing' : ['0']*8},
                'PSR_INDX' : {'#' :  4, 'Type' : 'U*2', 'Ref' :       None, 'Value' : None, 'Text' : 'PSR Record Index (used by STR records)', 'Missing' :    None},
                'PSR_NAM'  : {'#' :  5, 'Type' : 'C*n', 'Ref' :       None, 'Value' : None, 'Text' : 'Symbolic name of PSR record           ', 'Missing' :      ''},
                'OPT_FLG'  : {'#' :  6, 'Type' : 'B*1', 'Ref' :       None, 'Value' : None, 'Text' : 'Options Flag                          ', 'Missing' :    None},
                'TOTP_CNT' : {'#' :  7, 'Type' : 'U*2', 'Ref' :       None, 'Value' : None, 'Text' : 'Count of sets in the complete data set', 'Missing' :       1},
                'LOCP_CNT' : {'#' :  8, 'Type' : 'U*2', 'Ref' :       None, 'Value' : None, 'Text' : 'Count (k) of sets in this record      ', 'Missing' :       0},
                'PAT_BGN'  : {'#' :  9, 'Type' :'xU*8', 'Ref' : 'LOCP_CNT', 'Value' : None, 'Text' : "Array of Cycle #'s patterns begins on ", 'Missing' :      []},
                'PAT_END'  : {'#' : 10, 'Type' :'xU*8', 'Ref' : 'LOCP_CNT', 'Value' : None, 'Text' : "Array of Cycle #'s patterns stops at  ", 'Missing' :      []},
                'PAT_FILE' : {'#' : 11, 'Type' :'xC*n', 'Ref' : 'LOCP_CNT', 'Value' : None, 'Text' : 'Array of Pattern File Names           ', 'Missing' :      []},
                'PAT_LBL'  : {'#' : 12, 'Type' :'xC*n', 'Ref' : 'LOCP_CNT', 'Value' : None, 'Text' : 'Optional pattern symbolic name        ', 'Missing' :      []},
                'FILE_UID' : {'#' : 13, 'Type' :'xC*n', 'Ref' : 'LOCP_CNT', 'Value' : None, 'Text' : 'Optional array of file identifier code', 'Missing' :      []},
                'ATPG_DSC' : {'#' : 14, 'Type' :'xC*n', 'Ref' : 'LOCP_CNT', 'Value' : None, 'Text' : 'Optional array of ATPG information    ', 'Missing' :      []},
                'SRC_ID'   : {'#' : 15, 'Type' :'xC*n', 'Ref' : 'LOCP_CNT', 'Value' : None, 'Text' : 'Optional array of PatternInSrcFileID  ', 'Missing' :      []}
            }
        else:
            raise STDFError("%s object creation error: unsupported version '%s'" % (self.id, version))
        self._default_init(endian, record)

class PTR(STDR):
    def __init__(self, version=None, endian=None, record=None):
        self.id = 'PTR'
        self.local_debug = False
        if version==None or version == 'V4':
            self.version = 'V4'
            self.info = '''
Parametric Test Record
----------------------

Function:
    Contains the results of a single execution of a parametric test in the test program. The
    first occurrence of this record also establishes the default values for all semi-static
    information about the test, such as limits, units, and scaling. The PTR is related to the
    Test Synopsis Record (TSR) by test number, head number, and site number.

Frequency:
    * Obligatory, one per parametric test execution on each head/site

Location:
    Under normal circumstances, the PTR can appear anywhere in the data stream after
    the corresponding Part Information Record (PIR) and before the corresponding Part
    Result Record (PRR).
    In addition, to facilitate conversion from STDF V3, if the first PTR for a test contains
    default information only (no test results), it may appear anywhere after the initial
    "FAR-(ATRs)-MIR-(RDR)-(SDRs)" sequence, and before the first corresponding PTR, but need not appear
    between a PIR and PRR.
'''
            self.fields = {
                'REC_LEN'  : {'#' :  0, 'Type' : 'U*2', 'Ref' : None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'FPE' : None,                                     'Missing' : None   },
                'REC_TYP'  : {'#' :  1, 'Type' : 'U*1', 'Ref' : None, 'Value' :   15, 'Text' : 'Record type                           ', 'FPE' : None,                                     'Missing' : None   },
                'REC_SUB'  : {'#' :  2, 'Type' : 'U*1', 'Ref' : None, 'Value' :   10, 'Text' : 'Record sub-type                       ', 'FPE' : None,                                     'Missing' : None   },
                'TEST_NUM' : {'#' :  3, 'Type' : 'U*4', 'Ref' : None, 'Value' : None, 'Text' : 'Test number                           ', 'FPE' : None,                                     'Missing' : None   },
                'HEAD_NUM' : {'#' :  4, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : 'Test head number                      ', 'FPE' : None,                                     'Missing' : 1      },
                'SITE_NUM' : {'#' :  5, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : 'Test site number                      ', 'FPE' : None,                                     'Missing' : 1      },
                'TEST_FLG' : {'#' :  6, 'Type' : 'B*1', 'Ref' : None, 'Value' : None, 'Text' : 'Test flags (fail, alarm, etc.)        ', 'FPE' : None,                                     'Missing' : ['0']*8},
                'PARM_FLG' : {'#' :  7, 'Type' : 'B*1', 'Ref' : None, 'Value' : None, 'Text' : 'Parametric test flags (drift, etc.)   ', 'FPE' : None,                                     'Missing' : ['0']*8},
                'RESULT'   : {'#' :  8, 'Type' : 'R*4', 'Ref' : None, 'Value' : None, 'Text' : 'Test result                           ', 'FPE' : None,                                     'Missing' : 0.0    },
                'TEST_TXT' : {'#' :  9, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : 'Test description text or label        ', 'FPE' : None,                                     'Missing' : ''     },
                'ALARM_ID' : {'#' : 10, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : 'Name of alarm                         ', 'FPE' : None,                                     'Missing' : ''     },
                'OPT_FLAG' : {'#' : 11, 'Type' : 'B*1', 'Ref' : None, 'Value' : None, 'Text' : 'Optional data flag                    ', 'FPE' : "self.fields['OPT_FLAG']['Value']!=None", 'Missing' : 255    }, #TODO: Needs some more work
                'RES_SCAL' : {'#' : 12, 'Type' : 'I*1', 'Ref' : None, 'Value' : None, 'Text' : 'Test results scaling exponent         ', 'FPE' : "self.fields['OPT_FLAG']['Value']!=None", 'Missing' : 0      },
                'LLM_SCAL' : {'#' : 13, 'Type' : 'I*1', 'Ref' : None, 'Value' : None, 'Text' : 'Low limit scaling exponent            ', 'FPE' : "self.fields['OPT_FLAG']['Value']!=None", 'Missing' : 0      },
                'HLM_SCAL' : {'#' : 14, 'Type' : 'I*1', 'Ref' : None, 'Value' : None, 'Text' : 'High limit scaling exponent           ', 'FPE' : "self.fields['OPT_FLAG']['Value']!=None", 'Missing' : 0      },
                'LO_LIMIT' : {'#' : 15, 'Type' : 'R*4', 'Ref' : None, 'Value' : None, 'Text' : 'Low test limit value                  ', 'FPE' : "self.fields['OPT_FLAG']['Value']!=None", 'Missing' : 0.0    },
                'HI_LIMIT' : {'#' : 16, 'Type' : 'R*4', 'Ref' : None, 'Value' : None, 'Text' : 'High test limit value                 ', 'FPE' : "self.fields['OPT_FLAG']['Value']!=None", 'Missing' : 0.0    },
                'UNITS'    : {'#' : 17, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : 'Test units                            ', 'FPE' : "self.fields['OPT_FLAG']['Value']!=None", 'Missing' : ''     },
                'C_RESFMT' : {'#' : 18, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : 'ANSI C result format string           ', 'FPE' : "self.fields['OPT_FLAG']['Value']!=None", 'Missing' : ''     },
                'C_LLMFMT' : {'#' : 19, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : 'ANSI C low limit format string        ', 'FPE' : "self.fields['OPT_FLAG']['Value']!=None", 'Missing' : ''     },
                'C_HLMFMT' : {'#' : 20, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : 'ANSI C high limit format string       ', 'FPE' : "self.fields['OPT_FLAG']['Value']!=None", 'Missing' : ''     },
                'LO_SPEC'  : {'#' : 21, 'Type' : 'R*4', 'Ref' : None, 'Value' : None, 'Text' : 'Low specification limit value         ', 'FPE' : "self.fields['OPT_FLAG']['Value']!=None", 'Missing' : 0.0    },
                'HI_SPEC'  : {'#' : 22, 'Type' : 'R*4', 'Ref' : None, 'Value' : None, 'Text' : 'High specification limit value        ', 'FPE' : "self.fields['OPT_FLAG']['Value']!=None", 'Missing' : 0.0    }
            }
        elif version == 'V3':
            self.version ='V3'
            self.info = '''
Parametric Test Record
----------------------

Function:
    Contains the results of a single execution of a parametric test in the test program. The
    first occurrence of this record also establishes the default values for all semi-static
    information about the test, such as limits, units, and scaling. The PTR is related to the
    Test Synopsis Record (TSR) by test number, head number, and site number.

Frequency:
    * Obligatory, one per parametric test execution on each head/site

Location:
    Under normal circumstances, the PTR can appear anywhere in the data stream after
    the corresponding Part Information Record (PIR) and before the corresponding Part
    Result Record (PRR).
    In addition, to facilitate conversion from STDF V3, if the first PTR for a test contains
    default information only (no test results), it may appear anywhere after the initial
    "FAR-(ATRs)-MIR-(RDR)-(SDRs)" sequence, and before the first corresponding PTR, but need not appear
    between a PIR and PRR.
'''
            self.fields = {
                'REC_LEN'  : {'#' :  0, 'Type' : 'U*2', 'Ref' : None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'FPE' : None, 'Missing' : None     },
                'REC_TYP'  : {'#' :  1, 'Type' : 'U*1', 'Ref' : None, 'Value' :   15, 'Text' : 'Record type                           ', 'FPE' : None, 'Missing' : None     },
                'REC_SUB'  : {'#' :  2, 'Type' : 'U*1', 'Ref' : None, 'Value' :   10, 'Text' : 'Record sub-type                       ', 'FPE' : None, 'Missing' : None     },
                'TEST_NUM' : {'#' :  3, 'Type' : 'U*4', 'Ref' : None, 'Value' : None, 'Text' : 'Test number                           ', 'FPE' : None, 'Missing' : None     },
                'HEAD_NUM' : {'#' :  4, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : 'Test head number                      ', 'FPE' : None, 'Missing' : 1        },
                'SITE_NUM' : {'#' :  5, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : 'Test site number                      ', 'FPE' : None, 'Missing' : 1        },
                'TEST_FLG' : {'#' :  6, 'Type' : 'B*1', 'Ref' : None, 'Value' : None, 'Text' : 'Test flags (fail, alarm, etc.)        ', 'FPE' : None, 'Missing' : ['0']*8  },
                'PARM_FLG' : {'#' :  7, 'Type' : 'B*1', 'Ref' : None, 'Value' : None, 'Text' : 'Parametric test flags (drift, etc.)   ', 'FPE' : None, 'Missing' : ['0']*8  },
                'RESULT'   : {'#' :  8, 'Type' : 'R*4', 'Ref' : None, 'Value' : None, 'Text' : 'Test result                           ', 'FPE' : None, 'Missing' : 0.0      },
                'OPT_FLAG' : {'#' :  9, 'Type' : 'B*1', 'Ref' : None, 'Value' : None, 'Text' : 'Optional data flag                    ', 'FPE' : None, 'Missing' : ['0']*8  },
                'RES_SCAL' : {'#' : 10, 'Type' : 'I*1', 'Ref' : None, 'Value' : None, 'Text' : 'Test results scaling exponent         ', 'FPE' : None, 'Missing' : 0        },
                'RES_LDIG' : {'#' : 11, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'FPE' : None, 'Missing' : 0        },
                'RES_RDIG' : {'#' : 12, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'FPE' : None, 'Missing' : 0        },
                'DESC_FLG' : {'#' : 13, 'Type' : 'B*1', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'FPE' : None, 'Missing' : ['0']*8  },
                'UNITS'    : {'#' : 14, 'Type' : 'C*7', 'Ref' : None, 'Value' : None, 'Text' : 'Test units                            ', 'FPE' : None, 'Missing' : '       '},
                'LLM_SCAL' : {'#' : 15, 'Type' : 'I*1', 'Ref' : None, 'Value' : None, 'Text' : 'Low limit scaling exponent            ', 'FPE' : None, 'Missing' : 0        },
                'HLM_SCAL' : {'#' : 16, 'Type' : 'I*1', 'Ref' : None, 'Value' : None, 'Text' : 'High limit scaling exponent           ', 'FPE' : None, 'Missing' : 0        },
                'LLM_LDIG' : {'#' : 17, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'FPE' : None, 'Missing' : 0        },
                'LLM_RDIG' : {'#' : 18, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'FPE' : None, 'Missing' : 0        },
                'HLM_LDIG' : {'#' : 19, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'FPE' : None, 'Missing' : 0        },
                'HLM_RDIG' : {'#' : 20, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'FPE' : None, 'Missing' : 0        },
                'LO_LIMIT' : {'#' : 21, 'Type' : 'R*4', 'Ref' : None, 'Value' : None, 'Text' : 'Low test limit value                  ', 'FPE' : None, 'Missing' : 0.0      },
                'HI_LIMIT' : {'#' : 22, 'Type' : 'R*4', 'Ref' : None, 'Value' : None, 'Text' : 'High test limit value                 ', 'FPE' : None, 'Missing' : 0.0      },
                'TEST_NAM' : {'#' : 23, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'FPE' : None, 'Missing' : ''       },
                'SEQ_NAME' : {'#' : 24, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : '                                      ', 'FPE' : None, 'Missing' : ''       },
                'TEST_TXT' : {'#' : 25, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : 'Test description text or label        ', 'FPE' : None, 'Missing' : ''       }
            }
        else:
            raise STDFError("%s object creation error: unsupported version '%s'" % (self.id, version))
        self._default_init(endian, record)

class RDR(STDR):
    def __init__(self, version=None, endian=None, record=None):
        self.id = 'RDR'
        self.local_debug = False
        if version==None or version == 'V4':
            self.version = 'V4'
            self.info = '''
Retest Data Record
------------------

Function:
    Signals that the data in this STDF file is for retested parts. The data in this record,
    combined with information in the MIR, tells data filtering programs what data to
    replace when processing retest data.

Frequency:
    * Obligatory if a lot is retested. (not if a device is binned in the reteset bin)
    * One per data stream.

Location:
    If this record is used, it must appear immediately after theMaster Information Record (MIR).
'''
            self.fields = {
                'REC_LEN'  : {'#' : 0, 'Type' :  'U*2', 'Ref' : None,       'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' : None},
                'REC_TYP'  : {'#' : 1, 'Type' :  'U*1', 'Ref' : None,       'Value' :    1, 'Text' : 'Record type                           ', 'Missing' : None},
                'REC_SUB'  : {'#' : 2, 'Type' :  'U*1', 'Ref' : None,       'Value' :   70, 'Text' : 'Record sub-type                       ', 'Missing' : None},
                'NUM_BINS' : {'#' : 3, 'Type' :  'U*2', 'Ref' : None,       'Value' : None, 'Text' : 'Number (k) of bins being retested     ', 'Missing' : 0   },
                'RTST_BIN' : {'#' : 4, 'Type' : 'xU*2', 'Ref' : 'NUM_BINS', 'Value' : None, 'Text' : 'Array of retest bin numbers           ', 'Missing' : []  }
            }
        else:
            raise STDFError("%s object creation error: unsupported version '%s'" % (self.id, version))
        self._default_init(endian, record)


class RR1(STDR):
    def __init__(self, version=None, endian=None, record=None):
        self.id = 'RR1'
        raise STDFError("%s object creation error : reserved object", self.id)


class RR2(STDR):
    def __init__(self, version=None, endian=None, record=None):
        self.id = 'RR2'
        raise STDFError("%s object creation error : reserved object", self.id)



class SCR(STDR):
    def __init__(self, version=None, endian=None, record = None):
        self.id = 'SCR'
        self.local_debug = False
        if version == 'V3':
            self.version = 'V3'
            self.info=    '''
Site specific part Count Record (V3+)
-------------------------------------

Function:
    ?!?

Frequency:
    ?!?

Location:
    ?!?
'''
            self.fields = {
                'REC_LEN'  : {'#' :  0, 'Type' : 'U*2', 'Ref' : None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' : None},
                'REC_TYP'  : {'#' :  1, 'Type' : 'U*1', 'Ref' : None, 'Value' :   25, 'Text' : 'Record type                           ', 'Missing' : None},
                'REC_SUB'  : {'#' :  2, 'Type' : 'U*1', 'Ref' : None, 'Value' :   40, 'Text' : 'Record sub-type                       ', 'Missing' : None},
                'REC_LEN'  : {'#' :  2, 'Type' : 'U*2', 'Ref' : None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' : None},
                'REC_TYP'  : {'#' :  2, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : 'Record type (25)                      ', 'Missing' : None},
                'REC_SUB'  : {'#' :  2, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : 'Record sub-type (40)                  ', 'Missing' : None},
                'HEAD_NUM' : {'#' :  2, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : 'Test head number                      ', 'Missing' : None},
                'SITE_NUM' : {'#' :  2, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : 'Test site number                      ', 'Missing' : None},
                'FINISH_T' : {'#' :  2, 'Type' : 'U*4', 'Ref' : None, 'Value' : None, 'Text' : 'Date/time last part tested at site    ', 'Missing' : 0   },
                'PART_CNT' : {'#' :  2, 'Type' : 'U*4', 'Ref' : None, 'Value' : None, 'Text' : 'Number of parts tested                ', 'Missing' : 0   },
                'RTST_CNT' : {'#' :  2, 'Type' : 'I*4', 'Ref' : None, 'Value' : None, 'Text' : 'Number of parts retested              ', 'Missing' : -1  },
                'ABRT_CNT' : {'#' :  2, 'Type' : 'I*4', 'Ref' : None, 'Value' : None, 'Text' : 'Number of aborts during testing       ', 'Missing' : -1  },
                'GOOD_CNT' : {'#' :  2, 'Type' : 'I*4', 'Ref' : None, 'Value' : None, 'Text' : 'Number of good (passed) parts tested  ', 'Missing' : -1  },
                'FUNC_CNT' : {'#' :  2, 'Type' : 'I*4', 'Ref' : None, 'Value' : None, 'Text' : 'Number of functional parts tested     ', 'Missing' : -1  }
            }
        else:
            raise STDFError("%s object creation error: unsupported version '%s'" % (self.id, version))
        self._default_init(endian, record)


class SDR(STDR):
    def __init__(self, version=None, endian=None, record = None):
        self.id = 'SDR'
        self.local_debug = False
        if version==None or version == 'V4':
            self.version = 'V4'
            self.info = '''
Site Description Record
-----------------------

Function:
    Contains the configuration information for one or more test sites, connected to one test
    head, that compose a site group.

Frequency:
    * Optional
    * One for each site or group of sites that is differently configured.

Location:
    Immediately after the MIR and RDR (if an RDR is used).
'''
            self.fields = {
                'REC_LEN'  : {'#' :  0, 'Type' : 'U*2',  'Ref' : None,       'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' : None},
                'REC_TYP'  : {'#' :  1, 'Type' : 'U*1',  'Ref' : None,       'Value' :    1, 'Text' : 'Record type                           ', 'Missing' : None},
                'REC_SUB'  : {'#' :  2, 'Type' : 'U*1',  'Ref' : None,       'Value' :   80, 'Text' : 'Record sub-type                       ', 'Missing' : None},
                'HEAD_NUM' : {'#' :  3, 'Type' : 'U*1',  'Ref' : None,       'Value' : None, 'Text' : 'Test head number                      ', 'Missing' : 1   },
                'SITE_GRP' : {'#' :  4, 'Type' : 'U*1',  'Ref' : None,       'Value' : None, 'Text' : 'Site group number                     ', 'Missing' : 1   },
                'SITE_CNT' : {'#' :  5, 'Type' : 'U*1',  'Ref' : None,       'Value' : None, 'Text' : 'Number (k) of test sites in site group', 'Missing' : 1   },
                'SITE_NUM' : {'#' :  6, 'Type' : 'xU*1', 'Ref' : 'SITE_CNT', 'Value' : None, 'Text' : 'Array of k test site numbers          ', 'Missing' : [1] },
                'HAND_TYP' : {'#' :  7, 'Type' : 'C*n',  'Ref' : None,       'Value' : None, 'Text' : 'Handler or prober type                ', 'Missing' : ''  },
                'HAND_ID'  : {'#' :  8, 'Type' : 'C*n',  'Ref' : None,       'Value' : None, 'Text' : 'Handler or prober ID                  ', 'Missing' : ''  },
                'CARD_TYP' : {'#' :  9, 'Type' : 'C*n',  'Ref' : None,       'Value' : None, 'Text' : 'Probe card type                       ', 'Missing' : ''  },
                'CARD_ID'  : {'#' : 10, 'Type' : 'C*n',  'Ref' : None,       'Value' : None, 'Text' : 'Probe card ID                         ', 'Missing' : ''  },
                'LOAD_TYP' : {'#' : 11, 'Type' : 'C*n',  'Ref' : None,       'Value' : None, 'Text' : 'Load board type                       ', 'Missing' : ''  },
                'LOAD_ID'  : {'#' : 12, 'Type' : 'C*n',  'Ref' : None,       'Value' : None, 'Text' : 'Load board ID                         ', 'Missing' : ''  },
                'DIB_TYP'  : {'#' : 13, 'Type' : 'C*n',  'Ref' : None,       'Value' : None, 'Text' : 'DIB (aka load-) board type            ', 'Missing' : ''  },
                'DIB_ID'   : {'#' : 14, 'Type' : 'C*n',  'Ref' : None,       'Value' : None, 'Text' : 'DIB (aka load-) board ID              ', 'Missing' : ''  },
                'CABL_TYP' : {'#' : 15, 'Type' : 'C*n',  'Ref' : None,       'Value' : None, 'Text' : 'Interface cable type                  ', 'Missing' : ''  },
                'CABL_ID'  : {'#' : 16, 'Type' : 'C*n',  'Ref' : None,       'Value' : None, 'Text' : 'Interface cable ID                    ', 'Missing' : ''  },
                'CONT_TYP' : {'#' : 17, 'Type' : 'C*n',  'Ref' : None,       'Value' : None, 'Text' : 'Handler contactor type                ', 'Missing' : ''  },
                'CONT_ID'  : {'#' : 18, 'Type' : 'C*n',  'Ref' : None,       'Value' : None, 'Text' : 'Handler contactor ID                  ', 'Missing' : ''  },
                'LASR_TYP' : {'#' : 19, 'Type' : 'C*n',  'Ref' : None,       'Value' : None, 'Text' : 'Laser type                            ', 'Missing' : ''  },
                'LASR_ID'  : {'#' : 20, 'Type' : 'C*n',  'Ref' : None,       'Value' : None, 'Text' : 'Laser ID                              ', 'Missing' : ''  },
                'EXTR_TYP' : {'#' : 21, 'Type' : 'C*n',  'Ref' : None,       'Value' : None, 'Text' : 'Extra equipment type                  ', 'Missing' : ''  },
                'EXTR_ID'  : {'#' : 22, 'Type' : 'C*n',  'Ref' : None,       'Value' : None, 'Text' : 'Extra equipment ID                    ', 'Missing' : ''  }
            }
        else:
            raise STDFError("%s object creation error: unsupported version '%s'" % (self.id, version))
        self._default_init(endian, record)


class SHB(STDR):
    def __init__(self, version=None, endian=None, record=None):
        self.id = 'SHB'
        self.local_debug = False
        if version is None or version == 'V3':
            self.version = 'V3'
            self.info = '''
Site specific Hardware bin Record (V3+)
---------------------------------------

Function:
    Stores a count of the parts tested at one test site that are physically placed in a particular bin after testing.
    The SHB stores site specific information, that is, information generated at one site of the tester.
    It is therefore a subset of the Hardware Bin Record (HBR), which collects information from all the sites of a tester.
    The STDF specification also supports a site specific Software Bin Record (SSB), for logical binning categories.
    The part is actually placed in a hardware bin after testing. A part can be logically associated with a software bin during or after testing.

Frequency:
    ?!?

Location:
    ?!?
'''
            self.fields = {
                'REC_LEN'  : {'#' :  0, 'Type' : 'U*2',  'Ref' : None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' : None},
                'REC_TYP'  : {'#' :  1, 'Type' : 'U*1',  'Ref' : None, 'Value' :   25, 'Text' : 'Record type                           ', 'Missing' : None},
                'REC_SUB'  : {'#' :  2, 'Type' : 'U*1',  'Ref' : None, 'Value' :   10, 'Text' : 'Record sub-type                       ', 'Missing' : None},
                'HEAD_NUM' : {'#' :  3, 'Type' : 'U*1',  'Ref' : None, 'Value' : None, 'Text' : 'Test head number                      ', 'Missing' : 1   },
                'SITE_NUM' : {'#' :  4, 'Type' : 'U*1',  'Ref' : None, 'Value' : None, 'Text' : 'Test site number                      ', 'Missing' : 1   },
                'HBIN_NUM' : {'#' :  5, 'Type' : 'U*2',  'Ref' : None, 'Value' : None, 'Text' : 'Hardware bin number                   ', 'Missing' : None},
                'HBIN_CNT' : {'#' :  6, 'Type' : 'U*4',  'Ref' : None, 'Value' : None, 'Text' : 'Number of parts in bin                ', 'Missing' : 0   },
                'HBIN_NAM' : {'#' :  7, 'Type' : 'C*n',  'Ref' : None, 'Value' : None, 'Text' : 'Name of hardware bin                  ', 'Missing' : ''  }
            }
        else:
            raise STDFError("%s object creation error: unsupported version '%s'" % (self.id, version))
        self._default_init(endian, record)


class SSB(STDR):
    def __init__(self, version=None, endian=None, record=None):
        self.id = 'SSB'
        self.local_debug = False
        if version is None or version == 'V3':
            self.version = 'V3'
            self.info = '''
Site specific Software Bin record (V3+)
---------------------------------------

Function:
    Stores a count of the parts tested at one test site that are associated with a particular logical bin after testing.
    The SSB stores site specific information, that is, information generated at one site of the tester.
    It is therefore a subset of the Software Bin Record (SBR), which collects information from all the sites of a tester.
    The STDF specification also supports a site specific Hardware Bin Record (SHB), for physical binning categories.
    The part is actually placed in a hardware bin after testing. A part can be logically associated with a software bin during or after testing.

Frequency:
    ?!?

Location:
    ?!?
'''
            self.fields = {
                'REC_LEN'  : {'#' :  0, 'Type' : 'U*2',  'Ref' : None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' : None},
                'REC_TYP'  : {'#' :  1, 'Type' : 'U*1',  'Ref' : None, 'Value' :   25, 'Text' : 'Record type                           ', 'Missing' : None},
                'REC_SUB'  : {'#' :  2, 'Type' : 'U*1',  'Ref' : None, 'Value' :   20, 'Text' : 'Record sub-type                       ', 'Missing' : None},
                'HEAD_NUM' : {'#' :  3, 'Type' : 'U*1',  'Ref' : None, 'Value' : None, 'Text' : 'Test head number                      ', 'Missing' : 1   },
                'SITE_NUM' : {'#' :  4, 'Type' : 'U*1',  'Ref' : None, 'Value' : None, 'Text' : 'Test site number                      ', 'Missing' : 1   },
                'SBIN_NUM' : {'#' :  5, 'Type' : 'U*2',  'Ref' : None, 'Value' : None, 'Text' : 'Hardware bin number                   ', 'Missing' : None},
                'SBIN_CNT' : {'#' :  6, 'Type' : 'U*4',  'Ref' : None, 'Value' : None, 'Text' : 'Number of parts in bin                ', 'Missing' : 0   },
                'SBIN_NAM' : {'#' :  7, 'Type' : 'C*n',  'Ref' : None, 'Value' : None, 'Text' : 'Name of hardware bin                  ', 'Missing' : ''  }
            }
        else:
            raise STDFError("%s object creation error: unsupported version '%s'" % (self.id, version))
        self._default_init(endian, record)


class SSR(STDR):
    def __init__(self, version=None, endian=None, record=None):
        self.id = 'SSR'
        self.local_debug = False
        if version is None or version == 'V4':
            self.version = 'V4'
            self.info = '''
Scan Structure Record
---------------------

Function:
    This record contains the Scan Structure information normally found in a STIL file.
    The SSR is a top level Scan Structure record that contains an array of indexes to CDR
    (Chain Description Record) records which contain the chain information.

Frequency:
    ?!?

Location:
    ?!?
'''
            self.fields = {
                'REC_LEN'  : {'#' :  0, 'Type' : 'U*2',  'Ref' : None,      'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' : None},
                'REC_TYP'  : {'#' :  1, 'Type' : 'U*1',  'Ref' : None,      'Value' :    1, 'Text' : 'Record type                           ', 'Missing' : None},
                'REC_SUB'  : {'#' :  2, 'Type' : 'U*1',  'Ref' : None,      'Value' :   93, 'Text' : 'Record sub-type                       ', 'Missing' : None},
                'SSR_NAM'  : {'#' :  3, 'Type' : 'C*n',  'Ref' : None,      'Value' : None, 'Text' : 'Name of the STIL Scan Structure       ', 'Missing' : ''  },
                'CHN_CNT'  : {'#' :  4, 'Type' : 'U*2',  'Ref' : None,      'Value' : None, 'Text' : 'Count (k) of number of Chains         ', 'Missing' : 0   },
                'CHN_LIST' : {'#' :  5, 'Type' : 'xU*2', 'Ref' : 'CHN_CNT', 'Value' : None, 'Text' : 'Array of CDR Indexes                  ', 'Missing' : []  }
            }
        else:
            raise STDFError("%s object creation error: unsupported version '%s'" % (self.id, version))
        self._default_init(endian, record)


class STR(STDR):
    def __init__(self, version=None, endian=None, record=None):
        self.id = 'STR'
        self.local_debug = False
        if version is None or version=='V4':
            self.version = 'V4'
            self.info = '''
Record
------------------

Function:
    It contains all or some of the results of the single execution of a scan test in the test program.
    It is intended to contain all of the individual pin/cycle failures that are detected in a single test execution.
    If there are more failures than can be contained in a single record, then the record may be followed by additional continuation STR records.

Frequency:
    ?!?

Location:
    ?!?
'''
            self.fields = {
                'REC_LEN'  : {'#' :  0, 'Type' : 'U*2',  'Ref' : None,                     'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' : None     },
                'REC_TYP'  : {'#' :  1, 'Type' : 'U*1',  'Ref' : None,                     'Value' :   15, 'Text' : 'Record type                           ', 'Missing' : None     },
                'REC_SUB'  : {'#' :  2, 'Type' : 'U*1',  'Ref' : None,                     'Value' :   30, 'Text' : 'Record sub-type                       ', 'Missing' : None     },
                'CONT_FLG' : {'#' :  3, 'Type' : 'B*1',  'Ref' : None,                     'Value' : None, 'Text' : 'Continuation STRs follow (if not 0)   ', 'Missing' : 0        },
                'TEST_NUM' : {'#' :  4, 'Type' : 'U*4',  'Ref' : None,                     'Value' : None, 'Text' : 'Test number                           ', 'Missing' : None     },
                'HEAD_NUM' : {'#' :  5, 'Type' : 'U*1',  'Ref' : None,                     'Value' : None, 'Text' : 'Test head number                      ', 'Missing' : 1        },
                'SITE_NUM' : {'#' :  6, 'Type' : 'U*1',  'Ref' : None,                     'Value' : None, 'Text' : 'Test site number                      ', 'Missing' : 1        },
                'PSR_REF'  : {'#' :  7, 'Type' : 'U*2',  'Ref' : None,                     'Value' : None, 'Text' : 'PSR Index (Pattern Sequence Record)   ', 'Missing' : 0        },
                'TEST_FLG' : {'#' :  8, 'Type' : 'B*1',  'Ref' : None,                     'Value' : None, 'Text' : 'Test flags (fail, alarm, etc.)        ', 'Missing' : ['0'] * 8},
                'LOG_TYP'  : {'#' :  9, 'Type' : 'C*n',  'Ref' : None,                     'Value' : None, 'Text' : 'User defined description of datalog   ', 'Missing' : ''       },
                'TEST_TXT' : {'#' : 10, 'Type' : 'C*n',  'Ref' : None,                     'Value' : None, 'Text' : 'Descriptive text or label             ', 'Missing' : ''       },
                'ALARM_ID' : {'#' : 11, 'Type' : 'C*n',  'Ref' : None,                     'Value' : None, 'Text' : 'Name of alarm                         ', 'Missing' : ''       },
                'PROG_TXT' : {'#' : 12, 'Type' : 'C*n',  'Ref' : None,                     'Value' : None, 'Text' : 'Additional Programmed information     ', 'Missing' : ''       },
                'RSLT_TXT' : {'#' : 13, 'Type' : 'C*n',  'Ref' : None,                     'Value' : None, 'Text' : 'Additional result information         ', 'Missing' : ''       },
                'Z_VAL'    : {'#' : 14, 'Type' : 'U*1',  'Ref' : None,                     'Value' : None, 'Text' : 'Z Handling Flag                       ', 'Missing' : 0        },
                'FMU_FLG'  : {'#' : 15, 'Type' : 'B*1',  'Ref' : None,                     'Value' : None, 'Text' : 'MASK_MAP & FAL_MAP field status       ', 'Missing' : ['0'] * 8},
                'MASK_MAP' : {'#' : 16, 'Type' : 'D*n',  'Ref' : None,                     'Value' : None, 'Text' : 'Bit map of Globally Masked Pins       ', 'Missing' : []       },
                'FAL_MAP'  : {'#' : 17, 'Type' : 'D*n',  'Ref' : None,                     'Value' : None, 'Text' : 'Bit map of failures after buffer full ', 'Missing' : []       },
                'CYC_CNT'  : {'#' : 18, 'Type' : 'U*8',  'Ref' : None,                     'Value' : None, 'Text' : 'Total cycles executed in test         ', 'Missing' : 0        },
                'TOTF_CNT' : {'#' : 19, 'Type' : 'U*4',  'Ref' : None,                     'Value' : None, 'Text' : 'Total failures (pin x cycle) detected ', 'Missing' : 0        },
                'TOTL_CNT' : {'#' : 20, 'Type' : 'U*4',  'Ref' : None,                     'Value' : None, 'Text' : "Total fails logged across all STR's   ", 'Missing' : 0        },
                'CYC_BASE' : {'#' : 21, 'Type' : 'U*8',  'Ref' : None,                     'Value' : None, 'Text' : 'Cycle offset to apply to CYCL_NUM arr ', 'Missing' : 0        },
                'BIT_BASE' : {'#' : 22, 'Type' : 'U*4',  'Ref' : None,                     'Value' : None, 'Text' : 'Offset to apply to BIT_POS array      ', 'Missing' : 0        },
                'COND_CNT' : {'#' : 23, 'Type' : 'U*2',  'Ref' : None,                     'Value' : None, 'Text' : 'Count (g) of Test Conditions+opt spec ', 'Missing' : 0        },
                'LIM_CNT'  : {'#' : 24, 'Type' : 'U*2',  'Ref' : None,                     'Value' : None, 'Text' : 'Count (j) of LIM Arrays in cur. rec.  ', 'Missing' : 0        },  # 1 = global
                'CYC_SIZE' : {'#' : 25, 'Type' : 'U*1',  'Ref' : None,                     'Value' : None, 'Text' : 'Size (f) [1,2,4 or 8] of  CYC_OFST    ', 'Missing' : 1        },
                'PMR_SIZE' : {'#' : 26, 'Type' : 'U*1',  'Ref' : None,                     'Value' : None, 'Text' : 'Size (f) [1 or 2] of PMR_INDX         ', 'Missing' : 1        },
                'CHN_SIZE' : {'#' : 27, 'Type' : 'U*1',  'Ref' : None,                     'Value' : None, 'Text' : 'Size (f) [1, 2 or 4] of CHN_NUM       ', 'Missing' : 1        },
                'PAT_SIZE' : {'#' : 28, 'Type' : 'U*1',  'Ref' : None,                     'Value' : None, 'Text' : 'Size (f) [1,2, or 4] of PAT_NUM       ', 'Missing' : 1        },
                'BIT_SIZE' : {'#' : 29, 'Type' : 'U*1',  'Ref' : None,                     'Value' : None, 'Text' : 'Size (f) [1,2, or 4] of BIT_POS       ', 'Missing' : 1        },
                'U1_SIZE'  : {'#' : 30, 'Type' : 'U*1',  'Ref' : None,                     'Value' : None, 'Text' : 'Size (f) [1,2,4 or 8] of USR1         ', 'Missing' : 1        },
                'U2_SIZE'  : {'#' : 31, 'Type' : 'U*1',  'Ref' : None,                     'Value' : None, 'Text' : 'Size (f) [1,2,4 or 8] of USR2         ', 'Missing' : 1        },
                'U3_SIZE'  : {'#' : 32, 'Type' : 'U*1',  'Ref' : None,                     'Value' : None, 'Text' : 'Size (f) [1,2,4 or 8] of USR3         ', 'Missing' : 1        },
                'UTX_SIZE' : {'#' : 33, 'Type' : 'U*1',  'Ref' : None,                     'Value' : None, 'Text' : 'Size (f) of each string in USER_TXT   ', 'Missing' : 0        },
                'CAP_BGN'  : {'#' : 34, 'Type' : 'U*2',  'Ref' : None,                     'Value' : None, 'Text' : 'Offset to BIT_POS to get capture cycls', 'Missing' : 0        },
                'LIM_INDX' : {'#' : 35, 'Type' : 'xU*2', 'Ref' : 'LIM_CNT',                'Value' : None, 'Text' : 'Array of PMR unique limit specs       ', 'Missing' : []       },
                'LIM_SPEC' : {'#' : 36, 'Type' : 'xU*4', 'Ref' : 'LIM_CNT',                'Value' : None, 'Text' : "Array of fail datalog limits for PMR's", 'Missing' : []       },
                'COND_LST' : {'#' : 37, 'Type' : 'xC*n', 'Ref' : 'COND_CNT',               'Value' : None, 'Text' : 'Array of test condition (Name=value)  ', 'Missing' : []       },
                'CYC_CNT'  : {'#' : 38, 'Type' : 'U*2',  'Ref' : None,                     'Value' : None, 'Text' : 'Count (k) of entries in CYC_OFST array', 'Missing' : 0        },
                'CYC_OFST' : {'#' : 39, 'Type' : 'xU*f', 'Ref' : ('CYC_CNT', 'CYC_SIZE'),  'Value' : None, 'Text' : 'Array of cycle nrs relat to CYC_BASE  ', 'Missing' : []       },
                'PMR_CNT'  : {'#' : 40, 'Type' : 'U*2',  'Ref' : None,                     'Value' : None, 'Text' : 'Count (k) of entries in the PMR_INDX  ', 'Missing' : 0        },
                'PMR_INDX' : {'#' : 41, 'Type' : 'xU*f', 'Ref' : ('PMR_CNT', 'PMR_SIZE'),  'Value' : None, 'Text' : 'Array of PMR Indexes (All Formats)    ', 'Missing' : []       },
                'CHN_CNT'  : {'#' : 42, 'Type' : 'U*2',  'Ref' : None,                     'Value' : None, 'Text' : 'Count (k) of entries in the CHN_NUM   ', 'Missing' : 0        },
                'CHN_NUM'  : {'#' : 43, 'Type' : 'xU*f', 'Ref' : ('CHN_CNT', 'CHN_SIZE'),  'Value' : None, 'Text' : 'Array of Chain No for FF Name Mapping ', 'Missing' : []       },
                'EXP_CNT'  : {'#' : 44, 'Type' : 'U*2',  'Ref' : None,                     'Value' : None, 'Text' : 'Count (k) of EXP_DATA array entries   ', 'Missing' : 0        },
                'EXP_DATA' : {'#' : 45, 'Type' : 'xU*1', 'Ref' : 'EXP_CNT',                'Value' : None, 'Text' : 'Array of expected vector data         ', 'Missing' : []       },
                'CAP_CNT'  : {'#' : 46, 'Type' : 'U*2',  'Ref' : None,                     'Value' : None, 'Text' : 'Count (k) of CAP_DATA array entries   ', 'Missing' : 0        },
                'CAP_DATA' : {'#' : 47, 'Type' : 'xU*1', 'Ref' : 'CAP_CNT',                'Value' : None, 'Text' : 'Array of captured data                ', 'Missing' : []       },
                'NEW_CNT'  : {'#' : 48, 'Type' : 'U*2',  'Ref' : None,                     'Value' : None, 'Text' : 'Count (k) of NEW_DATA array entries   ', 'Missing' : 0        },
                'NEW_DATA' : {'#' : 49, 'Type' : 'xU*1', 'Ref' : 'NEW_CNT',                'Value' : None, 'Text' : 'Array of new vector data              ', 'Missing' : []       },
                'PAT_CNT'  : {'#' : 50, 'Type' : 'U*2',  'Ref' : None,                     'Value' : None, 'Text' : 'Count (k) of PAT_NUM array entries    ', 'Missing' : 0        },
                'PAT_NUM'  : {'#' : 51, 'Type' : 'xU*f', 'Ref' : ('PAT_CNT', 'PAT_SIZE'),  'Value' : None, 'Text' : 'Array of pattern # (Ptn/Chn/Bit fmt)  ', 'Missing' : []       },
                'BPOS_CNT' : {'#' : 52, 'Type' : 'U*2',  'Ref' : None,                     'Value' : None, 'Text' : 'Count (k) of BIT_POS array entries    ', 'Missing' : 0        },
                'BIT_POS'  : {'#' : 53, 'Type' : 'xU*f', 'Ref' : ('BPOS_CNT', 'BIT_SIZE'), 'Value' : None, 'Text' : 'Array of chain bit (Ptn/Chn/Bit fmt)  ', 'Missing' : []       },
                'USR1_CNT' : {'#' : 54, 'Type' : 'U*2',  'Ref' : None,                     'Value' : None, 'Text' : 'Count (k) of USR1 array entries       ', 'Missing' : 0        },
                'USR1'     : {'#' : 55, 'Type' : 'xU*f', 'Ref' : ('USR1_CNT', 'U1_SIZE'),  'Value' : None, 'Text' : 'Array of logged fail                  ', 'Missing' : []       },
                'USR2_CNT' : {'#' : 56, 'Type' : 'U*2',  'Ref' : None,                     'Value' : None, 'Text' : 'Count (k) of USR2 array entries       ', 'Missing' : 0        },
                'USR2'     : {'#' : 57, 'Type' : 'xU*f', 'Ref' : ('USR2_CNT', 'U2_SIZE'),  'Value' : None, 'Text' : 'Array of logged fail                  ', 'Missing' : []       },
                'USR3_CNT' : {'#' : 58, 'Type' : 'U*2',  'Ref' : None,                     'Value' : None, 'Text' : 'Count (k) of USR3 array entries       ', 'Missing' : 0        },
                'USR3'     : {'#' : 59, 'Type' : 'xU*f', 'Ref' : ('USR3_CNT', 'U3_SIZE'),  'Value' : None, 'Text' : 'Array of logged fail                  ', 'Missing' : []       },
                'TXT_CNT'  : {'#' : 60, 'Type' : 'U*2',  'Ref' : None,                     'Value' : None, 'Text' : 'Count (k) of USER_TXT array entries   ', 'Missing' : 0        },
                'USER_TXT' : {'#' : 61, 'Type' : 'xC*f', 'Ref' : ('TXT_CNT', 'UTX_SIZE'),  'Value' : None, 'Text' : 'Array of logged fail                  ', 'Missing' : []       }
            }
        else:
            raise STDFError("%s object creation error: unsupported version '%s'" % (self.id, version))
        self._default_init(endian, record)

class STS(STDR):
    def __init__(self, version=None, endian=None, record = None):
        self.id = 'STS'
        self.local_debug = False
        if version==None or version=='V3':
            self.version = 'V3'
            self.info=    '''
Site specific Test Synopsis record (V3+)
----------------------------------------

Function:
    Contains the test execution and failure counts at one test site for one parametric or functional test in the test plan.
    The STS stores site specific information, that is, information generated at one site of the tester.
    It is therefore a subset of the Test Synopsis Record (TSR), which collects information from all the sites of a tester.

Frequency:
    ?!?

Location:
    ?!?
'''
            self.fields = {
                'REC_LEN'  : {'#' :  0, 'Type' : 'U*2',  'Ref' : None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' : None   },
                'REC_TYP'  : {'#' :  1, 'Type' : 'U*1',  'Ref' : None, 'Value' :   25, 'Text' : 'Record type                           ', 'Missing' : None   },
                'REC_SUB'  : {'#' :  2, 'Type' : 'U*1',  'Ref' : None, 'Value' :   30, 'Text' : 'Record sub-type                       ', 'Missing' : None   },
                'HEAD_NUM' : {'#' :  3, 'Type' : 'U*1',  'Ref' : None, 'Value' : None, 'Text' : 'Test head number                      ', 'Missing' : 1      },
                'SITE_NUM' : {'#' :  4, 'Type' : 'U*1',  'Ref' : None, 'Value' : None, 'Text' : 'Test site number                      ', 'Missing' : 1      },
                'TEST_NUM' : {'#' :  5, 'Type' : 'U*4',  'Ref' : None, 'Value' : None, 'Text' : 'Test number                           ', 'Missing' : None   },
                'EXEC_CNT' : {'#' :  6, 'Type' : 'I*4',  'Ref' : None, 'Value' : None, 'Text' : 'Number of test executions             ', 'Missing' : -1     },
                'FAIL_CNT' : {'#' :  7, 'Type' : 'I*4',  'Ref' : None, 'Value' : None, 'Text' : 'Number of test failures               ', 'Missing' : -1     },
                'ALRM_CNT' : {'#' :  8, 'Type' : 'I*4',  'Ref' : None, 'Value' : None, 'Text' : 'Number of alarmed tests               ', 'Missing' : -1     },
                'OPT_FLAG' : {'#' :  9, 'Type' : 'B*1',  'Ref' : None, 'Value' : None, 'Text' : 'Optional Data Flag                    ', 'Missing' : ['1']*8},
                'PAD_BYTE' : {'#' : 10, 'Type' : 'B*1',  'Ref' : None, 'Value' : None, 'Text' : 'Reserved for future use               ', 'Missing' : ['0']*8},
                'TEST_MIN' : {'#' : 11, 'Type' : 'R*4',  'Ref' : None, 'Value' : None, 'Text' : 'Lowest test result value              ', 'Missing' : 0.0    },
                'TEST_MAX' : {'#' : 12, 'Type' : 'R*4',  'Ref' : None, 'Value' : None, 'Text' : 'Highest test result value             ', 'Missing' : 0.0    },
                'TST_MEAN' : {'#' : 13, 'Type' : 'R*4',  'Ref' : None, 'Value' : None, 'Text' : 'Mean of test result values            ', 'Missing' : 0.0    },
                'TST_SDEV' : {'#' : 14, 'Type' : 'R*4',  'Ref' : None, 'Value' : None, 'Text' : 'Standard Deviation of test values     ', 'Missing' : 0.0    },
                'TST_SUMS' : {'#' : 15, 'Type' : 'R*4',  'Ref' : None, 'Value' : None, 'Text' : 'Sum of test result values             ', 'Missing' : 0.0    },
                'TST_SQRS' : {'#' : 16, 'Type' : 'R*4',  'Ref' : None, 'Value' : None, 'Text' : 'Sum of Squares of test result values  ', 'Missing' : 0.0    },
                'TEST_NAM' : {'#' : 17, 'Type' : 'C*n',  'Ref' : None, 'Value' : None, 'Text' : 'Test Name length                      ', 'Missing' : ''     },
                'SEQ_NAME' : {'#' : 18, 'Type' : 'C*n',  'Ref' : None, 'Value' : None, 'Text' : 'Sequencer (program segment) name      ', 'Missing' : ''     },
                'TEST_LBL' : {'#' : 19, 'Type' : 'C*n',  'Ref' : None, 'Value' : None, 'Text' : 'Test text or label                    ', 'Missing' : ''     }
            }
        else:
            raise STDFError("%s object creation error: unsupported version '%s'" % (self.id, version))
        self._default_init(endian, record)

class TSR(STDR):
    def __init__(self, version=None, endian=None, record=None):
        self.id = 'TSR'
        self.local_debug = False
        if version==None or version=='V4':
            self.version = 'V4'
            self.info = '''
Test Synopsis Record
--------------------

Function:
    Contains the test execution and failure counts for one parametric or functional test in
    the test program. Also contains static information, such as test name. The TSR is
    related to the Functional Test Record (FTR), the Parametric Test Record (PTR), and the
    Multiple Parametric Test Record (MPR) by test number, head number, and site
    number.

Frequency:
    * Obligatory, one for each test executed in the test program per Head and site.
    * Optional summary per test head and/or test site.
    * May optionally be used to identify unexecuted tests.

Location:
    Anywhere in the data stream after the initial sequence (see page 14) and before the MRR.
    When test data is being generated in real-time, these records will appear after the last PRR.
'''
            self.fields = {
                'REC_LEN'  : {'#' :  0, 'Type' : 'U*2', 'Ref' : None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' : None       },
                'REC_TYP'  : {'#' :  1, 'Type' : 'U*1', 'Ref' : None, 'Value' :   10, 'Text' : 'Record type                           ', 'Missing' : None       },
                'REC_SUB'  : {'#' :  2, 'Type' : 'U*1', 'Ref' : None, 'Value' :   30, 'Text' : 'Record sub-type                       ', 'Missing' : None       },
                'HEAD_NUM' : {'#' :  3, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : 'Test head number                      ', 'Missing' : 255        },
                'SITE_NUM' : {'#' :  4, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : 'Test site number                      ', 'Missing' : 255        },
                'TEST_TYP' : {'#' :  5, 'Type' : 'C*1', 'Ref' : None, 'Value' : None, 'Text' : 'Test type [P/F/space]                 ', 'Missing' : ' '        },
                'TEST_NUM' : {'#' :  6, 'Type' : 'U*4', 'Ref' : None, 'Value' : None, 'Text' : 'Test number                           ', 'Missing' : None       },
                'EXEC_CNT' : {'#' :  7, 'Type' : 'U*4', 'Ref' : None, 'Value' : None, 'Text' : 'Number of test executions             ', 'Missing' : 4294967295},
                'FAIL_CNT' : {'#' :  8, 'Type' : 'U*4', 'Ref' : None, 'Value' : None, 'Text' : 'Number of test failures               ', 'Missing' : 4294967295},
                'ALRM_CNT' : {'#' :  9, 'Type' : 'U*4', 'Ref' : None, 'Value' : None, 'Text' : 'Number of alarmed tests               ', 'Missing' : 4294967295},
                'TEST_NAM' : {'#' : 10, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : 'Test name                             ', 'Missing' : ''         },
                'SEQ_NAME' : {'#' : 11, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : 'Sequencer (program segment/flow) name ', 'Missing' : ''         },
                'TEST_LBL' : {'#' : 12, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : 'Test label or text                    ', 'Missing' : ''         },
                'OPT_FLAG' : {'#' : 13, 'Type' : 'B*1', 'Ref' : None, 'Value' : None, 'Text' : 'Optional data flag See note           ', 'Missing' : ['1']*8    },
                'TEST_TIM' : {'#' : 14, 'Type' : 'R*4', 'Ref' : None, 'Value' : None, 'Text' : 'Average test execution time in seconds', 'Missing' : 0.0        },
                'TEST_MIN' : {'#' : 15, 'Type' : 'R*4', 'Ref' : None, 'Value' : None, 'Text' : 'Lowest test result value              ', 'Missing' : 0.0        },
                'TEST_MAX' : {'#' : 16, 'Type' : 'R*4', 'Ref' : None, 'Value' : None, 'Text' : 'Highest test result value             ', 'Missing' : 0.0        },
                'TST_SUMS' : {'#' : 17, 'Type' : 'R*4', 'Ref' : None, 'Value' : None, 'Text' : 'Sum of test result values             ', 'Missing' : 0.0        },
                'TST_SQRS' : {'#' : 18, 'Type' : 'R*4', 'Ref' : None, 'Value' : None, 'Text' : 'Sum of squares of test result values  ', 'Missing' : 0.0        }
            }
        elif version == 'V3':
            self.version = 'V3'
            self.info = '''
Test Synopsis Record
--------------------

Function:
    Contains the test execution and failure counts for one parametric or functional test in
    the test program. Also contains static information, such as test name. The TSR is
    related to the Functional Test Record (FTR), the Parametric Test Record (PTR), and the
    Multiple Parametric Test Record (MPR) by test number, head number, and site
    number.

Frequency:
    * Obligatory, one for each test executed in the test program per Head and site.
    * Optional summary per test head and/or test site.
    * May optionally be used to identify unexecuted tests.

Location:
    Anywhere in the data stream after the initial sequence (see page 14) and before the MRR.
    When test data is being generated in real-time, these records will appear after the last PRR.
'''
            self.fields = {
                'REC_LEN'  : {'#' :  0, 'Type' : 'U*2', 'Ref' : None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' : None       },
                'REC_TYP'  : {'#' :  1, 'Type' : 'U*1', 'Ref' : None, 'Value' :   10, 'Text' : 'Record type                           ', 'Missing' : None       },
                'REC_SUB'  : {'#' :  2, 'Type' : 'U*1', 'Ref' : None, 'Value' :   30, 'Text' : 'Record sub-type                       ', 'Missing' : None       },
                'TEST_NUM' : {'#' :  3, 'Type' : 'U*4', 'Ref' : None, 'Value' : None, 'Text' : 'Test number                           ', 'Missing' : None       },
                'EXEC_CNT' : {'#' :  4, 'Type' : 'I*4', 'Ref' : None, 'Value' : None, 'Text' : 'Number of test executions             ', 'Missing' : 4294967295},
                'FAIL_CNT' : {'#' :  5, 'Type' : 'I*4', 'Ref' : None, 'Value' : None, 'Text' : 'Number of test failures               ', 'Missing' : 4294967295},
                'ALRM_CNT' : {'#' :  6, 'Type' : 'I*4', 'Ref' : None, 'Value' : None, 'Text' : 'Number of alarmed tests               ', 'Missing' : 4294967295},
                'OPT_FLAG' : {'#' :  7, 'Type' : 'B*1', 'Ref' : None, 'Value' : None, 'Text' : 'Optional data flag See note           ', 'Missing' : ['1']*8    },
                'PAD_BYTE' : {'#' :  8, 'Type' : 'B*1', 'Ref' : None, 'Value' : None, 'Text' : 'Padding byte                          ', 'Missing' : ['0']*8    },
                'TEST_MIN' : {'#' :  9, 'Type' : 'R*4', 'Ref' : None, 'Value' : None, 'Text' : 'Lowest test result value              ', 'Missing' : 0.0        },
                'TEST_MAX' : {'#' : 10, 'Type' : 'R*4', 'Ref' : None, 'Value' : None, 'Text' : 'Highest test result value             ', 'Missing' : 0.0        },
                'TST_MEAN' : {'#' : 11, 'Type' : 'R*4', 'Ref' : None, 'Value' : None, 'Text' : 'Mean of test result values            ', 'Missing' : 0.0        },
                'TST_SDEV' : {'#' : 12, 'Type' : 'R*4', 'Ref' : None, 'Value' : None, 'Text' : 'Standard Deviation of test results    ', 'Missing' : 0.0        },
                'TST_SUMS' : {'#' : 13, 'Type' : 'R*4', 'Ref' : None, 'Value' : None, 'Text' : 'Sum of test result values             ', 'Missing' : 0.0        },
                'TST_SQRS' : {'#' : 14, 'Type' : 'R*4', 'Ref' : None, 'Value' : None, 'Text' : 'Sum of squares of test result values  ', 'Missing' : 0.0        },
                'TEST_NAM' : {'#' : 15, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : 'Test name                             ', 'Missing' : ''         },
                'SEQ_NAME' : {'#' : 16, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : 'Sequence name                         ', 'Missing' : ''         },
            }
        else:
            raise STDFError("%s object creation error: unsupported version '%s'" % (self.id, version))
        self._default_init(endian, record)


class WCR(STDR):
    def __init__(self, version=None, endian=None, record=None):
        self.id = 'WCR'
        self.local_debug = False
        if version==None or version=='V4' or version=='V3':
            if version==None: self.version='V4'
            else: self.version = version
            self.info = '''
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
'''
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
        else:
            raise STDFError("%s object creation error: unsupported version '%s'" % (self.id, version))
        self._default_init(endian, record)

class WIR(STDR):
    def __init__(self, version=None, endian=None, record=None):
        self.id = 'WIR'
        self.local_debug = False
        if version==None or version=='V4':
            self.version = 'V4'
            self.info = '''
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
'''
            self.fields = {
                'REC_LEN'  : {'#' :  0, 'Type' : 'U*2', 'Ref' : None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' : None},
                'REC_TYP'  : {'#' :  1, 'Type' : 'U*1', 'Ref' : None, 'Value' :    2, 'Text' : 'Record type                           ', 'Missing' : None},
                'REC_SUB'  : {'#' :  2, 'Type' : 'U*1', 'Ref' : None, 'Value' :   10, 'Text' : 'Record sub-type                       ', 'Missing' : None},
                'HEAD_NUM' : {'#' :  3, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : 'Test head number                      ', 'Missing' : 1   },
                'SITE_GRP' : {'#' :  4, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : 'Site group number                     ', 'Missing' : 255 },
                'START_T'  : {'#' :  5, 'Type' : 'U*4', 'Ref' : None, 'Value' : None, 'Text' : 'Date and time first part tested       ', 'Missing' : 0   },
                'WAFER_ID' : {'#' :  6, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : 'Wafer ID                              ', 'Missing' : ''  }
            }
        elif version == 'V3':
            self.version = 'V3'
            self.info = '''
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
'''
            self.fields = {
                'REC_LEN'  : {'#' :  0, 'Type' : 'U*2', 'Ref' : None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' : None   },
                'REC_TYP'  : {'#' :  1, 'Type' : 'U*1', 'Ref' : None, 'Value' :    2, 'Text' : 'Record type                           ', 'Missing' : None   },
                'REC_SUB'  : {'#' :  2, 'Type' : 'U*1', 'Ref' : None, 'Value' :   10, 'Text' : 'Record sub-type                       ', 'Missing' : None   },
                'HEAD_NUM' : {'#' :  3, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : 'Test head number                      ', 'Missing' : 1      },
                'PAD_BYTE' : {'#' :  4, 'Type' : 'B*1', 'Ref' : None, 'Value' : None, 'Text' : 'Pad byte                              ', 'Missing' : ['0']*8},
                'START_T'  : {'#' :  5, 'Type' : 'U*4', 'Ref' : None, 'Value' : None, 'Text' : 'Date and time first part tested       ', 'Missing' : 0      },
                'WAFER_ID' : {'#' :  6, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : 'Wafer ID                              ', 'Missing' : ''     }
            }
        else:
            raise STDFError("%s object creation error: unsupported version '%s'" % (self.id, version))
        self._default_init(endian, record)

class WRR(STDR):
    def __init__(self, version=None, endian=None, record=None):
        self.id = 'WRR'
        self.local_debug = False
        if version==None or version=='V4':
            self.version = 'V4'
            self.info = '''
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
'''
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
        elif version == 'V3':
            self.version = 'V3'
            self.info = '''
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
'''
            self.fields = {
                'REC_LEN'  : {'#' :  0, 'Type' : 'U*2', 'Ref' : None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' : None      },
                'REC_TYP'  : {'#' :  1, 'Type' : 'U*1', 'Ref' : None, 'Value' :    2, 'Text' : 'Record type                           ', 'Missing' : None      },
                'REC_SUB'  : {'#' :  2, 'Type' : 'U*1', 'Ref' : None, 'Value' :   20, 'Text' : 'Record sub-type                       ', 'Missing' : None      },
                'FINISH_T' : {'#' :  3, 'Type' : 'U*4', 'Ref' : None, 'Value' : None, 'Text' : 'Date and time last part tested        ', 'Missing' : 0         },
                'HEAD_NUM' : {'#' :  4, 'Type' : 'U*1', 'Ref' : None, 'Value' : None, 'Text' : 'Test head number                      ', 'Missing' : 255       },
                'PAD_BYTE' : {'#' :  5, 'Type' : 'B*1', 'Ref' : None, 'Value' : None, 'Text' : 'Test head number                      ', 'Missing' : ['0']*8   },
                'PART_CNT' : {'#' :  6, 'Type' : 'U*4', 'Ref' : None, 'Value' : None, 'Text' : 'Number of parts tested                ', 'Missing' : 0         },
                'RTST_CNT' : {'#' :  7, 'Type' : 'I*4', 'Ref' : None, 'Value' : None, 'Text' : 'Number of retests done                ', 'Missing' : 0         },
                'ABRT_CNT' : {'#' :  8, 'Type' : 'I*4', 'Ref' : None, 'Value' : None, 'Text' : 'Number of aborts during testing       ', 'Missing' : 0         },
                'GOOD_CNT' : {'#' :  9, 'Type' : 'I*4', 'Ref' : None, 'Value' : None, 'Text' : 'Number of good (passed) parts tested  ', 'Missing' : 0         },
                'FUNC_CNT' : {'#' : 10, 'Type' : 'I*4', 'Ref' : None, 'Value' : None, 'Text' : 'Number of functional parts tested     ', 'Missing' : 0         },
                'WAFER_ID' : {'#' : 11, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : 'Wafer ID                              ', 'Missing' : ''        },
                'HAND_ID'  : {'#' : 12, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : 'Handler (Prober) ID                   ', 'Missing' : ''        },
                'PRB_CARD' : {'#' : 13, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : 'Probe Card ID                         ', 'Missing' : ''        },
                'USR_DESC' : {'#' : 14, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : 'Wafer description supplied by user    ', 'Missing' : ''        },
                'EXC_DESC' : {'#' : 15, 'Type' : 'C*n', 'Ref' : None, 'Value' : None, 'Text' : 'Wafer description supplied by exec    ', 'Missing' : ''        }
            }
        else:
            raise STDFError("%s object creation error: unsupported version '%s'" % (self.id, version))
        self._default_init(endian, record)

class WTR(STDR):
    def __init__(self, version=None, endian=None, record = None):
        self.id = 'WTR'
        self.local_debug = False
        if version==None or version=='V3':
            self.version = 'V3'
            self.info=    '''
?!?
----------------------------------------

Function:
    ?!?

Frequency:
    ?!?

Location:
    ?!?
'''
            self.fields = {
                'REC_LEN'   : {'#' : 0, 'Type' : 'U*2', 'Ref' : None, 'Value' : None, 'Text' : 'Bytes of data following header        ', 'Missing' : None},
                'REC_TYP'   : {'#' : 1, 'Type' : 'U*1', 'Ref' : None, 'Value' :  220, 'Text' : 'Record type                           ', 'Missing' : None},
                'REC_SUB'   : {'#' : 2, 'Type' : 'U*1', 'Ref' : None, 'Value' :  202, 'Text' : 'Record sub-type                       ', 'Missing' : None},
                'TEST_TYPE' : {'#' : 3, 'Type' : 'C*1', 'Ref' : None, 'value' : None, 'Text' : '                                      ', 'Missing' : ' ' }
            }
        else:
            raise STDFError("%s object creation error: unsupported version '%s'" % (self.id, version))
        self._default_init(endian, record)



def read_record(fd, RHF):
    '''
    This method will read one record from fd (at the current fp) with record header format RHF, and return the raw record
    '''
    header = fd.read(4)
    REC_LEN, REC_TYP, REC_SUB = struct.unpack(RHF, header)
    footer = fd.read(REC_LEN)
    return REC_LEN, REC_TYP, REC_SUB, header+footer

def read_indexed_record(fd, fp, RHF):
    fd.seek(fp)
    header = fd.read(4)
    REC_LEN, REC_TYP, REC_SUB = struct.unpack(RHF, header)
    footer = fd.read(REC_LEN)
    return REC_LEN, REC_TYP, REC_SUB, header+footer

class records_from_file(object):
    '''
    Generator class to run over the records in FileName.
    The return values are 4-fold : REC_LEN, REC_TYP, REC_SUB and REC
    REC is the complete record (including REC_LEN, REC_TYP & REC_SUB)
    if unpack indicates if REC is to be the raw record or the unpacked object.
    of_interest can be a list of records to return. By default of_interest is void
    meaning all records (of FileName's STDF Version) are used.
    '''
    debug = False

    def __init__(self, FileName, unpack=False, of_interest=None):
        if self.debug: print("initializing 'records_from_file")
        if isinstance(FileName, str):
            self.keep_open = False
            if not os.path.exists(FileName):
                raise STDFError("'%s' does not exist")
            self.endian = get_STDF_setup_from_file(FileName)[0]
            self.version = 'V%s' % struct.unpack('B', get_bytes_from_file(FileName, 5, 1))
            self.fd = open(FileName, 'rb')
        elif isinstance(FileName, io.IOBase):
            self.keep_open = True
            self.fd = FileName
            ptr = self.fd.tell()
            self.fd.seek(4)
            buff = self.fd.read(2)
            CPU_TYPE, STDF_VER = struct.unpack('BB', buff)
            if CPU_TYPE == 1: self.endian = '>'
            elif CPU_TYPE == 2: self.endian = '<'
            else: self.endian = '?'
            self.version = 'V%s' % STDF_VER
            self.fd.seek(ptr)
        else:
            raise STDFError("'%s' is not a string or an open file descriptor")
        self.unpack = unpack
        self.fmt = '%sHBB' % self.endian
        TS2ID = ts_to_id(self.version)
        if of_interest==None:
            self.records_of_interest = TS2ID
        elif isinstance(of_interest, list):
            ID2TS = id_to_ts(self.version)
            tmp_list = []
            for item in of_interest:
                if isinstance(item, str):
                    if item in ID2TS:
                        if ID2TS[item] not in tmp_list:
                            tmp_list.append(ID2TS[item])
                elif isinstance(item, tuple) and len(item)==2:
                    if item in TS2ID:
                        if item not in tmp_list:
                            tmp_list.append(item)
            self.records_of_interest = tmp_list
        else:
            raise STDFError("objects_from_file(%s, %s) : Unsupported of_interest" % (FileName, of_interest))

    def __del__(self):
        if not self.keep_open:
            self.fd.close()

    def __iter__(self):
        return self

    def __next__(self):
        while self.fd!=None:
            header = self.fd.read(4)
            if len(header)!=4:
                raise StopIteration
            else:
                REC_LEN, REC_TYP, REC_SUB = struct.unpack(self.fmt, header)
                footer = self.fd.read(REC_LEN)
                if (REC_TYP, REC_SUB) in self.records_of_interest:
                    if len(footer)!=REC_LEN:
                        raise StopIteration()
                    else:
                        if self.unpack:
                            return REC_LEN, REC_TYP, REC_SUB, create_record_object(self.version, self.endian, (REC_TYP, REC_SUB), header+footer)
                        else:
                            return REC_LEN, REC_TYP, REC_SUB, header+footer

def objects_from_indexed_file(FileName, index, records_of_interest=None):
    '''
     This is a Generator of records (not in order!)
    '''
    if not isinstance(FileName, str): raise STDFError("'%s' is not a string.")
    if not os.path.exists(FileName): raise STDFError("'%s' does not exist")
    endian = get_STDF_setup_from_file(FileName)[0]
    RLF = '%sH' % endian
    version = 'V%s' % struct.unpack('B', get_bytes_from_file(FileName, 5, 1))
    fd = open(FileName, 'rb')

    ALL = list(id_to_ts(version).keys())
    if records_of_interest==None:
        roi = ALL
    elif isinstance(records_of_interest, list):
        roi = []
        for item in records_of_interest:
            if isinstance(item, str):
                if (item in ALL) and (item not in roi):
                    roi.append(item)
    else:
        raise STDFError("objects_from_indexed_file(%s, index, records_of_interest) : Unsupported records_of_interest" % (FileName, records_of_interest))
    for REC_ID in roi:
        if REC_ID in index:
            for fp in index[REC_ID]:
                OBJ = create_record_object(version, endian, REC_ID, get_record_from_file_at_position(fd, fp, RLF))
                yield OBJ

# class xrecords_from_file(object):
#     '''
#     This is a *FAST* iterator class that returns the next record from an STDF file each time it is called.
#     It is fast because it doesn't check versions, extensions and it doesn't unpack the record and skips unknown records.
#     '''
#
#     def __init__(self, FileName, of_interest=None):
#         #TODO: add a record_list of records to return
#         if isinstance(FileName, str):
#             try:
#                 stdf_file = File(FileName)
#             except:
#                 raise StopIteration
#             self.fd = stdf_file.open()
#         elif isinstance(FileName, File):
#             stdf_file = FileName
#             self.fd = FileName.open()
#         else:
#             raise STDFError("records_from_file(%s) : Unsupported 'FileName'" % FileName)
#         self.endian = stdf_file.endian
#         self.version = stdf_file.version
#         TS2ID = ts_to_id(self.version)
#         if of_interest==None:
#             self.of_interest = list(TS2ID.keys())
#         elif isinstance(of_interest, list):
#             ID2TS = id_to_ts(self.version)
#             tmp_list = []
#             for item in of_interest:
#                 if isinstance(item, str):
#                     if item in ID2TS:
#                         if ID2TS[item] not in tmp_list:
#                             tmp_list.append(ID2TS[item])
#                 elif isinstance(item, tuple) and len(item)==2:
#                     if item in TS2ID:
#                         if item not in tmp_list:
#                             tmp_list.append(item)
#             self.of_interest = tmp_list
#         else:
#             raise STDFError("records_from_file(%s, %s) : Unsupported of_interest" % (FileName, of_interest))
#
#     def __del__(self):
#         self.fd.close()
#
#     def __iter__(self):
#         return self
#
#     def __next__(self):
#         while self.fd!=None:
#             while True:
#                 header = self.fd.read(4)
#                 if len(header)!=4:
#                     raise StopIteration
#                 REC_LEN, REC_TYP, REC_SUB = struct.unpack('HBB', header)
#                 footer = self.fd.read(REC_LEN)
#                 if len(footer)!=REC_LEN:
#                     raise StopIteration
#                 if (REC_TYP, REC_SUB) in self.of_interest:
#                     return REC_LEN, REC_TYP, REC_SUB, header+footer
#
# class xobjects_from_file(object):
#     '''
#     This is an iterator class that returns the next object (unpacked) from an STDF file.
#     It will take care of versions and extensions, and unrecognized records will simply be skipped.
#     '''
#     def __init__(self, FileName, of_interest=None):
#         if isinstance(FileName, str):
#             try:
#                 stdf_file = File(FileName)
#             except:
#                 raise STDFError("objects_from_file(%s, %s) : File doesn't exist" % (FileName, of_interest))
#             self.fd = stdf_file.open()
#         elif isinstance(FileName, File):
#             self.fd = FileName.open()
#         else:
#             raise STDFError("objects_from_file(%s) : Unsupported 'FileName'" % FileName)
#         self.endian = stdf_file.endian
#         self.version = stdf_file.version
#         TS2ID = ts_to_id(self.version)
#         if of_interest==None:
#             of_interest = TS2ID
#         elif isinstance(of_interest, list):
#             ID2TS = id_to_ts(self.version)
#             tmp_list = []
#             for item in of_interest:
#                 if isinstance(item, str):
#                     if item in ID2TS:
#                         if ID2TS[item] not in tmp_list:
#                             tmp_list.append(ID2TS[item])
#                 elif isinstance(item, tuple) and len(item)==2:
#                     if item in TS2ID:
#                         if item not in tmp_list:
#                             tmp_list.append(item)
#             of_interest = tmp_list
#         else:
#             raise STDFError("objects_from_file(%s, %s) : Unsupported of_interest" % (FileName, of_interest))
#         self.of_interest = of_interest
#         self.fmt = '%sHBB' % self.endian
#
#     def __del__(self):
#         self.fd.close()
#
#     def __iter__(self):
#         return self
#
#     def __next__(self):
#         while True:
#             header = self.fd.read(4)
#             if len(header)!=4:
#                 raise StopIteration
#             else:
#                 REC_LEN, REC_TYP, REC_SUB = struct.unpack(self.fmt, header)
#                 footer = self.fd.read(REC_LEN)
#                 if len(footer)!=REC_LEN:
#                     raise StopIteration
#                 else:
#                     record = header + footer
#                     if (REC_TYP, REC_SUB) in self.of_interest:
#                         recobj = create_record_object(self.version, self.endian, (REC_TYP, REC_SUB), record)
#                         return (recobj)


# class open(object):
#     '''
#     file opener that opens an STDF file transparently (gzipped or not)
#     '''
#     def __init__(self, fname):
#         f = open(fname)
#         # Read magic number (the first 2 bytes) and rewind.
#         magic_number = f.read(2)
#         f.seek(0)
#         # Encapsulated 'self.f' is a file or a GzipFile.
#         if magic_number == '\x1f\x8b':
#             self.f = gzip.GzipFile(fileobj=f)
#         else:
#             self.f = f
#
#         # Define '__enter__' and '__exit__' to use in 'with' blocks.
#         def __enter__(self):
#             return self
#         def __exit__(self, type, value, traceback):
#             try:
#                 self.f.fileobj.close()
#             except AttributeError:
#                 pass
#             finally:
#                 self.f.close()
#
#         # Reproduce the interface of an open file by encapsulation.
#         def __getattr__(self, name):
#             return getattr(self.f, name)
#         def __iter__(self):
#             return iter(self.f)
#         def next(self):
#             return next(self.f)



def create_record_object(Version, Endian, REC_ID, REC=None):
    '''
    This function will create and return the appropriate Object for REC
    based on REC_ID. REC_ID can be a 2-element tuple or a string.
    If REC is not None, then the record will also be unpacked.
    '''
    retval = None
    REC_TYP=-1
    REC_SUB=-1
    if Version not in supported().versions():
        raise STDFError("Unsupported STDF Version : %s" % Version)
    if Endian not in ['<', '>']:
        raise STDFError("Unsupported Endian : '%s'" % Endian)
    if isinstance(REC_ID, tuple) and len(REC_ID)==2:
        TS2ID = ts_to_id(Version)
        if (REC_ID[0], REC_ID[1]) in TS2ID:
            REC_TYP = REC_ID[0]
            REC_SUB = REC_ID[1]
            REC_ID = TS2ID[(REC_TYP, REC_SUB)]
    elif isinstance(REC_ID, str):
        ID2TS = id_to_ts(Version)
        if REC_ID in ID2TS:
            (REC_TYP, REC_SUB) = ID2TS[REC_ID]
    else:
        raise STDFError("Unsupported REC_ID : %s" % REC_ID)

    if REC_TYP!=-1 and REC_SUB!=-1:
        if REC_ID == 'PTR': retval = PTR(Version, Endian, REC)
        elif REC_ID == 'FTR': retval = FTR(Version, Endian, REC)
        elif REC_ID == 'MPR': retval = MPR(Version, Endian, REC)
        elif REC_ID == 'STR': retval = STR(Version, Endian, REC)
        elif REC_ID == 'MTR': retval = MTR(Version, Endian, REC)
        elif REC_ID == 'PIR': retval = PIR(Version, Endian, REC)
        elif REC_ID == 'PRR': retval = PRR(Version, Endian, REC)
        elif REC_ID == 'FAR': retval = FAR(Version, Endian, REC)
        elif REC_ID == 'ATR': retval = ATR(Version, Endian, REC)
        elif REC_ID == 'VUR': retval = VUR(Version, Endian, REC)
        elif REC_ID == 'MIR': retval = MIR(Version, Endian, REC)
        elif REC_ID == 'MRR': retval = MRR(Version, Endian, REC)
        elif REC_ID == 'WCR': retval = WCR(Version, Endian, REC)
        elif REC_ID == 'WIR': retval = WIR(Version, Endian, REC)
        elif REC_ID == 'WRR': retval = WRR(Version, Endian, REC)
        elif REC_ID == 'ADR': retval = ADR(Version, Endian, REC)
        elif REC_ID == 'ASR': retval = ASR(Version, Endian, REC)
        elif REC_ID == 'BPS': retval = BPS(Version, Endian, REC)
        elif REC_ID == 'BRR': retval = BRR(Version, Endian, REC)
        elif REC_ID == 'BSR': retval = BSR(Version, Endian, REC)
        elif REC_ID == 'CNR': retval = CNR(Version, Endian, REC)
        elif REC_ID == 'DTR': retval = DTR(Version, Endian, REC)
        elif REC_ID == 'EPDR': retval = EPDR(Version, Endian, REC)
        elif REC_ID == 'EPS': retval = EPS(Version, Endian, REC)
        elif REC_ID == 'ETSR': retval = ETSR(Version, Endian, REC)
        elif REC_ID == 'FDR': retval = FDR(Version, Endian, REC)
        elif REC_ID == 'FSR': retval = FSR(Version, Endian, REC)
        elif REC_ID == 'GDR': retval = GDR(Version, Endian, REC)
        elif REC_ID == 'GTR': retval = GTR(Version, Endian, REC)
        elif REC_ID == 'HBR': retval = HBR(Version, Endian, REC)
        elif REC_ID == 'IDR': retval = IDR(Version, Endian, REC)
        elif REC_ID == 'MCR': retval = MCR(Version, Endian, REC)
        elif REC_ID == 'MMR': retval = MMR(Version, Endian, REC)
        elif REC_ID == 'MSR': retval = MSR(Version, Endian, REC)
        elif REC_ID == 'NMR': retval = NMR(Version, Endian, REC)
        elif REC_ID == 'PCR': retval = PCR(Version, Endian, REC)
        elif REC_ID == 'PDR': retval = PDR(Version, Endian, REC)
        elif REC_ID == 'PGR': retval = PGR(Version, Endian, REC)
        elif REC_ID == 'PLR': retval = PLR(Version, Endian, REC)
        elif REC_ID == 'PMR': retval = PMR(Version, Endian, REC)
        elif REC_ID == 'PSR': retval = PSR(Version, Endian, REC)
        elif REC_ID == 'RDR': retval = RDR(Version, Endian, REC)
        elif REC_ID == 'SBR': retval = SBR(Version, Endian, REC)
        elif REC_ID == 'SCR': retval = SCR(Version, Endian, REC)
        elif REC_ID == 'SDR': retval = SDR(Version, Endian, REC)
        elif REC_ID == 'SHB': retval = SHB(Version, Endian, REC)
        elif REC_ID == 'SSB': retval = SSB(Version, Endian, REC)
        elif REC_ID == 'SSR': retval = SSR(Version, Endian, REC)
        elif REC_ID == 'STS': retval = STS(Version, Endian, REC)
        elif REC_ID == 'TSR': retval = TSR(Version, Endian, REC)
        elif REC_ID == 'WTR': retval = WTR(Version, Endian, REC)
        elif REC_ID == 'RR1': retval = RR1(Version, Endian, REC) # can not be reached because of -1
        elif REC_ID == 'RR2': retval = RR2(Version, Endian, REC) # can not be reached because of -1
    return retval

def wafer_map(data, parameter=None):
    '''
    data is a pandas data frame, it has at least 5 columns ('X_COORD', 'Y_COORD', 'LOT_ID', 'WAFER_ID' and the parameter)
    If the parameter is not named the following order of 'parameters' will be used :
        'HARD_BIN'
        'SOFT_BIN'
        'PART_PF'

    '''
    pass



def get_bytes_from_file(FileName, Offset, Number):
    '''
    This function will return 'Number' bytes starting after 'Offset' from 'FileName'
    '''
    if not isinstance(FileName, str): raise STDFError("'%s' is not a string")
    if not isinstance(Offset, int): raise STDFError("Offset is not an integer")
    if not isinstance(Number, int): raise STDFError("Number is not an integer")
    if not os.path.exists(FileName): raise STDFError("'%s' does not exist")
    if guess_type(FileName)[1]=='gzip':
        raise NotImplemented("Not yet implemented")
    else:
        with open(FileName, 'rb') as fd:
            fd.seek(Offset)
            retval = fd.read(Number)
    return retval

def get_record_from_file_at_position(fd, offset, REC_LEN_FMT):
    fd.seek(offset)
    header = fd.read(4)
    REC_LEN = struct.unpack(REC_LEN_FMT, header[:2])[0]
    footer = fd.read(REC_LEN)
    return header+footer

def get_STDF_setup_from_file(FileName):
    '''
    This function will determine the endian and the version of a given STDF file
    it must *NOT* be guaranteed that FileName exists or is an STDF File.
    '''
    endian = None
    version = None
    if os.path.exists(FileName) and os.path.isfile(FileName):
        if is_file_with_stdf_magicnumber(FileName):
            CPU_TYP, STDF_VER = struct.unpack('BB', get_bytes_from_file(FileName, 4, 2))
            if CPU_TYP == 1: endian = '>'
            elif CPU_TYP == 2: endian = '<'
            else: endian = '?'
            version = "V%s" % STDF_VER
    return endian, version

def get_MIR_from_file(FileName):
    '''
    This function will just get the MIR (near the start of the file) from the FileName and return it.
    it must *NOT* be guaranteed that FileName exists or is an STDF File.
    '''
    endian, version = get_STDF_setup_from_file(FileName)
    mir = None
    if endian!=None and version!=None: # file exists and is an STDF file
        for record in xrecords_from_file(FileName):
            _, REC_TYP, REC_SUB, REC = record
            if (REC_TYP, REC_SUB) == (1, 10):
                mir = MIR(version, endian, REC)
                break
    return mir

def get_partcount_from_file(FileName):
    '''
    This function will return the number of parts contained in FileName.
    it must *NOT* be guaranteed that FileName exists or is an STDF File.
    '''

def save_STDF_index(FileName, index):
    '''
    '''
    if os.path.exists(FileName) and os.path.isfile(FileName):
        Path, Name = os.path.split(FileName)
        Base, Ext = os.path.splitext(Name)
        if Ext in ['.stdf', '.pbz2']:
            pickle_file = os.path.join(Path, "%s.pbz2" % Base)
        else:
            raise Exception("FileName should have '.stdf' or '.pbz2' extension")
        with bz2.open(pickle_file, 'wb') as fd:
            pickle.dump(index, fd)










if __name__ == '__main__':
    endian = '<'
    version = 'V4'
    rec = b'\x1b\x00\x01P\x00\x00\x08\x00\x01\x02\x03\x04\x05\x06\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

    sdr = SDR(version, endian, rec)

    print(sdr)
