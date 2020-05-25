#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 23 12:43:51 2020

@author: tom
"""
import sys

__latest_STDF_version__ = 'V4'

FileNameDefinitions = {
    'V4' : r'[a-zA-Z][a-zA-Z0-9_]{0,38}\.[sS][tT][dD][a-zA-Z0-9_\.]{0,36}',
}

# fmt: off
RecordDefinitions = {
    # Information about the STDF file
    (0, 10)   : {'V4' : ['FAR', 'File Attributes Record',            [('', True)]]                                },  #
    (0, 20)   : {'V4' : ['ATR', 'Audit Trail Record',                [('', False)]]                               },  #
    (0, 30)   : {'V4' : ['VUR', 'Version Update Record',             [('V4-2007', True), ('Memory:2010.1', True)]]},  #
    # Data collected on a per lot basis
    (1, 10)   : {'V4' : ['MIR', 'Master Information Record',         [('', True)]]                                },  #
    (1, 20)   : {'V4' : ['MRR', 'Master Results Record',             [('', True)]]                                },  #
    (1, 30)   : {'V4' : ['PCR', 'Part Count Record',                 [('', True)]]                                },  #
    (1, 40)   : {'V4' : ['HBR', 'Hardware Bin Record',               [('', False)]]                               },  #
    (1, 50)   : {'V4' : ['SBR', 'Software Bin Record',               [('', False)]]                               },  #
    (1, 60)   : {'V4' : ['PMR', 'Pin Map Record',                    [('', False)]]                               },  #
    (1, 62)   : {'V4' : ['PGR', 'Pin Group Record',                  [('', False)]]                               },
    (1, 63)   : {'V4' : ['PLR', 'Pin List Record',                   [('', False)]]                               },
    (1, 70)   : {'V4' : ['RDR', 'Re-test Data Record',               [('', False)]]                               },
    (1, 80)   : {'V4' : ['SDR', 'Site Description Record',           [('', False)]]                               },
    (1, 90)   : {'V4' : ['PSR', 'Pattern Sequence Record',           [('V4-2007', False)]]                        },
    (1, 91)   : {'V4' : ['NMR', 'Name Map Record',                   [('V4-2007', False)]]                        },
    (1, 92)   : {'V4' : ['CNR', 'Cell Name Record',                  [('V4-2007', False)]]                        },
    (1, 93)   : {'V4' : ['SSR', 'Scan Structure Record',             [('V4-2007', False)]]                        },
    (1, 94)   : {'V4' : ['CDR', 'Chain Description Record',          [('V4-2007', False)]]                        },
    (1, 95)   : {'V4' : ['ASR', 'Algorithm Specification Record',    [('Memory:2010.1', False)]]                  },
    (1, 96)   : {'V4' : ['FSR', 'Frame Specification Record',        [('Memory:2010.1', False)]]                  },
    (1, 97)   : {'V4' : ['BSR', 'Bit stream Specification Record',   [('Memory:2010.1', False)]]                  },
    (1, 99)   : {'V4' : ['MSR', 'Memory Structure Record',           [('Memory:2010.1', False)]]                  },
    (1, 100)  : {'V4' : ['MCR', 'Memory Controller Record',          [('Memory:2010.1', False)]]                  },
    (1, 101)  : {'V4' : ['IDR', 'Instance Description Record',       [('Memory:2010.1', False)]]                  },
    (1, 102)  : {'V4' : ['MMR', 'Memory Model Record',               [('Memory:2010.1', False)]]                  },
    # Data collected per wafer
    (2, 10)   : {'V4' : ['WIR', 'Wafer Information Record',          [('', False)]]                               },
    (2, 20)   : {'V4' : ['WRR', 'Wafer Results Record',              [('', False)]]                               },
    (2, 30)   : {'V4' : ['WCR', 'Wafer Configuration Record',        [('', False)]]                               },
    # Data collected on a per part basis
    (5, 10)   : {'V4' : ['PIR', 'Part Information Record',           [('', False)]]                               },
    (5, 20)   : {'V4' : ['PRR', 'Part Results Record',               [('', False)]]                               },
    # Data collected per test in the test program
    (10, 30)  : {'V4' : ['TSR', 'Test Synopsis Record',              [('', False)]]                               },
    # Data collected per test execution
    (15, 10)  : {'V4' : ['PTR', 'Parametric Test Record',            [('', False)]]                               },
    (15, 15)  : {'V4' : ['MPR', 'Multiple-Result Parametric Record', [('', False)]]                               },
    (15, 20)  : {'V4' : ['FTR', 'Functional Test Record',            [('', False)]]                               },
    (15, 30)  : {'V4' : ['STR', 'Scan Test Record',                  [('V4-2007', False)]]                        },
    (15, 40)  : {'V4' : ['MTR', 'Memory Test Record',                [('Memory:2010.1', False)]]                  },
    # Data collected per program segment
    (20, 10)  : {'V4' : ['BPS', 'Begin Program Section Record',      [('', False)]]                               },
    (20, 20)  : {'V4' : ['EPS', 'End Program Section Record',        [('', False)]]                               },
    # Generic Data
    (50, 10)  : {'V4' : ['GDR', 'Generic Data Record',               [('', False)]]                               },
    (50, 30)  : {'V4' : ['DTR', 'Datalog Text Record',               [('', False)]]                               },
    # Teradyne extensions
    (180, -1) : {'V4' : ['RR1', 'Reserved for Image software',       [('', False)]]                               },
    (181, -1) : {'V4' : ['RR2', 'Reserved for IG900 software',       [('', False)]]                               },
}
# fmt: on


class STDFError(Exception):
    pass


class supported:
    def __init__(self):
        pass

    def versions(self):
        """This method will return a list of *ALL* suported versions."""
        retval = []
        for (REC_TYP, REC_SUB) in RecordDefinitions:
            for Version in RecordDefinitions[(REC_TYP, REC_SUB)]:
                if Version not in retval:
                    retval.append(Version)
        return retval

    def extensions_for_version(self, Version=__latest_STDF_version__):
        """This method will return a list of *ALL* supportd extensions for a given Version."""
        retval = []
        if Version in self.versions():
            for (Type, Sub) in RecordDefinitions:
                if Version in RecordDefinitions[(Type, Sub)]:
                    exts = RecordDefinitions[(Type, Sub)][Version][2]
                    for ext in exts:
                        if ext[0] != '' and ext[0] not in retval:
                            retval.append(ext[0])
        return retval

    def versions_and_extensions(self):
        """This method returns a dictionary of *ALL* supported versions and the supported extensions for them."""
        retval = {}
        for version in self.supported_versions():
            retval[version] = self.extensions_for_version(version)


def ts_to_id(Version=__latest_STDF_version__, Extensions=None):
    '''
    This function returns a dictionary of TS -> ID for the given STDF version and Extension(s)
    If Extensions==None, then all available extensions are used
    '''
    retval = {}
    if Version in supported().versions():
        if Extensions is None:
            Extensions = supported().extensions_for_version(Version) + ['']
        else:
            exts = ['']
            for Extension in Extensions:
                if Extension in supported().extensions(Version):
                    if Extension not in exts:
                        exts.append(Extension)
            Extensions = exts
        for (REC_TYP, REC_SUB) in RecordDefinitions:
            if Version in RecordDefinitions[(REC_TYP, REC_SUB)]:
                for ext, _obligatory_flag in RecordDefinitions[(REC_TYP, REC_SUB)][Version][2]:
                    if ext in Extensions:
                        retval[(REC_TYP, REC_SUB)] = RecordDefinitions[(REC_TYP, REC_SUB)][Version][0]
    return retval


def id_to_ts(Version=__latest_STDF_version__, Extensions=None):
    '''
    This function returns a dictionary ID -> TS for the given STDF version and Extension(s)
    If Extensions==None, then all available extensions are used
    '''
    retval = {}
    temp = ts_to_id(Version, Extensions)
    for item in temp:
        retval[temp[item]] = item
    return retval


def hexify(input):
    """This function returns the hexified version of input.

    The input can be a byte array or an UTF8 string
    The return value is always an UTF8 string.
    """
    retval = ""
    if isinstance(input, bytes):
        for b in range(len(input)):
            retval += hex(input[b]).upper().replace('0X', '0x')
    elif isinstance(input, str):
        for i in input:
            retval += hex(ord(i)).upper().replace('0X', '0x')
    else:
        raise Exception("input type needs to be bytes or str.")
    return retval


def sys_endian():
    """ This function determines the endian of the running system.

    < means little endian, as used by pack/unpack
    > means big endian, as used by pack/unpack
    """
    if sys.byteorder == 'little':
        return '<'
    return '>'


def sys_cpu():
    """This function determines the CPU Type.

    1 means a big endian CPU
    2 means a little endian CPU
    """
    if sys_endian() == '<':
        return 2
    return 1


def is_odd(value):
    """This function will return True if the 'value' is odd, False otherwise.

    Note: If 'value' is not an int-type, False is returned.
    """
    if isinstance(value, int):
        if ((value % 2) == 1):
            return True
    return False


def is_even(value):
    """This function will return True if the 'value' is EVEN, False otherwise.

    Note: If 'value' in not an int-type, False is returned.
    """
    return not is_odd(value)
