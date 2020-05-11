"""
Created on Mon Apr  6 11:37:12 2020

@author: hoeren

References:
    PEP8 : https://www.python.org/dev/peps/pep-0008/
    numpy doc style : https://numpydoc.readthedocs.io/en/latest/format.html
"""

import os
import getpass
import numpy as np

from ATE.utils import DT

indent = '    '  # 4 spaces (tab will not do for PEP257)


def generator(project_path, definition):
    """This function will generate the actual python test based on the supplied info.
        - project_path : the absolute path to the project root
        - definition : a dictionary as follows
                {'name' : str, # holding the test name
                 'type' : str, # holding the strin 'custom' or 'standard'
                 'hardware' : str,
                 'base' : str,
                 'docstring' : [], # list of lines
                 'input_parameters' : {
                     'name' : {'Shmoo' : bool,
                               'Min' : float,
                               'Default' : float,
                               'Max' : float,
                               '10ᵡ' : str,
                               'Unit' : str,
                               'fmt' : str},
                     ...},
                 'output_parameters' : {
                     'name' : {'LSL': float,
                               'LTL': float,
                               'Nom': float,
                               'UTL': float,
                               'USL': float,
                               '10ᵡ': str,
                               'Unit': str,
                               'fmt': str},
                     ...},
                 'dependencies' : {'Name' : bool, # only one bool enabled, this indicates what test (name) is **IMMEDIATELY** before the current test, all others are somewhere before.
                                   ...}
                 }

    This function will return the RELATIVE path to the generated file upon
    success, and '' upon fail

    If the target file already exists, then an Exception is raised, as this
    should not be possible!
    """

    print(definition)
    rel_path_to_file = os.path.join('src', definition['hardware'], definition['base'], f"{definition['name']}.py")
    abs_path_to_file = os.path.join(project_path, rel_path_to_file)
    abs_dir = os.path.dirname(abs_path_to_file)

    if not os.path.exists(abs_dir):
        os.makedirs(abs_dir)

    if os.path.exists(abs_path_to_file):  # overwrite
        print("asked to generate a test that already exists ... hence 'overwrite'!")  # TODO: implement
    else:  # create new
        with open(abs_path_to_file, 'w', encoding='utf-8') as tf:
            # reference : https://stackoverflow.com/questions/41914739/how-do-i-activate-a-conda-env-in-a-subshell
            cw(tf, f"#!/usr/bin/env conda run -n ATE python")
            cw(tf, "# -*- coding: utf-8 -*-\n")  # not sure if in python 3 this is still necessary, but just in case

            cw(tf, "'''")
            now = DT()
            cw(tf, f"Created on {now}")

            user = getpass.getuser()
            domain = str(os.environ.get('USERDNSDOMAIN'))  # TODO: maybe move this to 'company specific stuff' later on ?
            if domain == 'None':
                user_email = ''
            else:
                user_email = f"({user}@{domain})".lower()
            cw(tf, f"By @author: {user} {user_email}")
            cw(tf, f"'''")
            cw(tf, '')

            cw(tf, f"from ATE.org.abc import testABC  # TODO: Move it up to the hardware common.py")
            cw(tf, f"import . common")
            cw(tf, f"\n")
        # class definition
            cw(tf, f"class {definition['name']}(testABC):")
        # docstring
            if 'docstring' in definition:
                for line_nr, line in enumerate(definition['docstring']):
                    if line_nr == 0:
                        if len(definition['docstring']) == 1:
                            if line.endswith('.'):
                                cw(tf, f'{indent}""""{line}"""')
                            else:
                                cw(tf, f'{indent}"""{line}."""')
                        else:
                            if line.endswith('.'):
                                cw(tf, f'{indent}""""{line}')
                            else:
                                cw(tf, f'{indent}"""{line}.')
                    else:
                        if line_nr + 1 == len(definition['docstring']):
                            cw(tf, f'{indent}{line}\n{indent}"""')
                        else:
                            cw(tf, f"{indent}{line}")
            else:
                cw(tf, '{indent}"""ADD A DOCSTRING."""')
            cw(tf, f"")
        # class variables
            cw(tf, f"{indent}hardware = '{definition['hardware']}'")
            cw(tf, f"{indent}base = '{definition['base']}'")
            cw(tf, f"{indent}Type = '{definition['type']}'")
            cw(tf, f"")
            tippprint(tf, definition['input_parameters'])
            cw(tf, f"")
            toppprint(tf, definition['output_parameters'])
            cw(tf, f"")
        # do-function
            cw(tf, f"{indent}def do(ip, op):")
            cw(tf, f"{indent}{indent}pass")  # TODO: add random variable !!!
            cw(tf, f'')
        # main
            cw(tf, f"if __name__ == '__main__':")
            cw(tf, f"{indent}import os")
            cw(tf, f"{indent}tester = os.environ.get('TESTER')")
            cw(tf, f"{indent}tester_mode = os.environ.get('TESTERMODE')")
            cw(tf, f"{indent}if tester_mode == 'DIRECT':")
            cw(tf, f"{indent}{indent}pass  # TODO: implement")
            cw(tf, f"{indent}else:  # 'INTERACTIVE'")
            cw(tf, f"{indent}{indent}from ATE.org import TestRunner")
            cw(tf, f"{indent}{indent}testRunner = TestRunner(__file__)")
    return rel_path_to_file


def cw(fd, line):
    """Code Write line to fd, and add **ONE** newline to the line."""
    if fd is None:
        print(line)
    else:
        fd.write(line + '\n')


def tippprint(fd, ip):
    '''
    Test Input Parameters Pretty PRINT

    This function will be given a file descriptor of an open test file,
    and the input parameters (dictionary).
    The function will print the dictionary nicely aligned to the file descriptor.
    '''
    name_ = 0
    min_ = 0
    default_ = 0
    max_ = 0
    mul_ = 0
    unit_ = 0
    fmt_ = 0
    for param in ip:
        if len(f"{param}: ") > name_:
            name_ = len(param)

        if np.isinf(ip[param]['Min']):
            if 4 > min_:
                min_ = 4
        else:
            if len(f"{ip[param]['Min']:{ip[param]['fmt']}}") > min_:
                min_ = len(f"{ip[param]['Min']:{ip[param]['fmt']}}")

        if len(f"{ip[param]['Default']:{ip[param]['fmt']}}") > default_:
            default_ = len(f"{ip[param]['Default']:{ip[param]['fmt']}}")

        if len(f"{ip[param]['Max']:{ip[param]['fmt']}}") > max_:
            max_ = len(f"{ip[param]['Max']:{ip[param]['fmt']}}")

        if len(f"{ip[param]['10ᵡ']}") > mul_:
            mul_ = len(f"{ip[param]['10ᵡ']}")

        if len(f"{ip[param]['Unit']}") > unit_:
            unit_ = len(f"{ip[param]['Unit']}")

        if len(f"{ip[param]['fmt']}") > fmt_:
            fmt_ = len(f"{ip[param]['fmt']}")

    name_ += 2
    mul_ += 2
    unit_ += 2
    fmt_ += 2

    cw(fd, f"{indent}input_parameters = {{")
    for index, param in enumerate(ip):
        ind = f"{indent}{indent}"

        name = f"'{param}':"
        Name = f"{name:{name_}}{{"

        if ip[param]['Shmoo'] is True:
            Shmoo = "'Shmoo':  True, "
        else:
            Shmoo = "'Shmoo': False, "

        Min = f"'Min': {ip[param]['Min']:{min_}{ip[param]['fmt']}}, "

        Default = f"'Default': {ip[param]['Default']:{default_}{ip[param]['fmt']}}, "

        Max = f"'Max': {ip[param]['Max']:{max_}{ip[param]['fmt']}}, "

        mul__ = f"'{ip[param]['10ᵡ']}'"
        Mul = f"'10ᵡ': {mul__:>{mul_}}, "

        unit__ = f"'{ip[param]['Unit']}'"
        Unit = f"'Unit': {unit__:>{unit_}}, "

        fmt__ = f"'{ip[param]['fmt']}'"
        if index + 1 == len(ip):  # last line
            Fmt = f"'fmt': {fmt__:>{fmt_}}}}}}"
        else:
            Fmt = f"'fmt': {fmt__:>{fmt_}}}},"

        line = ind + Name + Shmoo + Min + Default + Max + Mul + Unit + Fmt
        cw(fd, line)


def toppprint(fd, op):
    '''
    Test Output Parameters Pretty PRINT

    same as tippprint but for output parameters to a test file.
    '''
    name_ = 0
    LSL_ = 0
    LTL_ = 0
    Nom_ = 0
    UTL_ = 0
    USL_ = 0
    mul_ = 0
    unit_ = 0
    fmt_ = 0
    for param in op:
        if len(f"{param}: ") > name_:
            name_ = len(param)

        if np.isinf(op[param]['LSL']):
            if 4 > LSL_:
                LSL_ = 4
        else:
            length = len(f"{op[param]['LSL']:{op[param]['fmt']}}")
            if length > LSL_:
                LSL_ = length

        if np.isinf(op[param]['LTL']):
            if 4 > LTL_:
                LTL_ = 4
        elif np.isnan(op[param]['LTL']):
            if 3 > LTL_:
                LTL_ = 3
        else:
            length = len(f"{op[param]['LTL']:{op[param]['fmt']}}")
            if length > LTL_:
                LTL_ = length

        length = len(f"{op[param]['Nom']:{op[param]['fmt']}}")
        if length > Nom_:
            Nom_ = length

        if np.isinf(op[param]['UTL']):
            if 4 > UTL_:
                UTL_ = 4
        elif np.isnan(op[param]['UTL']):
            if 3 > UTL_:
                UTL_ = 3
        else:
            length = len(f"{op[param]['UTL']:{op[param]['fmt']}}")
            if length > UTL_:
                UTL_ = length

        if np.isinf(op[param]['USL']):
            if 4 > USL_:
                USL_ = 4
        else:
            length = len(f"{op[param]['USL']:{op[param]['fmt']}}")
            if length > USL_:
                USL_ = length

        if len(f"{op[param]['10ᵡ']}") > mul_:
            mul_ = len(f"{op[param]['10ᵡ']}")

        if len(f"{op[param]['Unit']}") > unit_:
            unit_ = len(f"{op[param]['Unit']}")

        if len(f"{op[param]['fmt']}") > fmt_:
            fmt_ = len(f"{op[param]['fmt']}")

    # name_ += 2
    if name_ < 9:
        name_ = 9  # for the header
    mul_ += 2
    unit_ += 2
    fmt_ += 2

    th = f"{indent}{indent}{'Parameter':{name_}} | LSL"
    cw(fd, th)

    bh = f"{indent}{indent}"
    b_parameter = '-' * (name_ + 1)
    b_parameter += '+'
    cw(fd, bh)

    for index, param in enumerate(op):
        ind = f"{indent}{indent}"

        name = f"{param}"
        Name = f"{name:{name_}} | "

        LSL = f"{LSL_:{op[param]['fmt']}} | "

        LTL = f"'{op[param]['LTL']:{LTL_}{op[param]['fmt']}}, "

        Nom = f"'Nom': {op[param]['Nom']:{Nom_}{op[param]['fmt']}}, "

        UTL = f"'UTL': {op[param]['UTL']:{UTL_}{op[param]['fmt']}}, "

        USL = f"'USL': {op[param]['USL']:{USL_}{op[param]['fmt']}}, "

        mul__ = f"'{op[param]['10ᵡ']}'"
        Mul = f"'10ᵡ': {mul__:>{mul_}}, "

        unit__ = f"'{op[param]['Unit']}'"
        Unit = f"'Unit': {unit__:>{unit_}}, "

        fmt__ = f"'{op[param]['fmt']}'"
        if index + 1 == len(op):  # last line
            Fmt = f"'fmt': {fmt__:>{fmt_}}}}}}"
        else:
            Fmt = f"'fmt': {fmt__:>{fmt_}}}},"

        line = ind + Name + LSL + LTL + Nom + UTL + USL + Mul + Unit + Fmt
        cw(fd, line)


if __name__ == '__main__':

    input_parameters = {
        'Temperature':    {'Shmoo':  True, 'Min':   -40.0, 'Default': 25.0, 'Max':  170.0, '10ᵡ':  '', 'Unit': '°C', 'fmt': '.0f'},
        'new_parameter1': {'Shmoo': False, 'Min': -np.inf, 'Default':  0.0, 'Max': np.inf, '10ᵡ': 'μ', 'Unit':  'V', 'fmt': '.3f'},
        'new_parameter2': {'Shmoo': False, 'Min': -np.inf, 'Default':  0.0, 'Max': np.inf, '10ᵡ':  '', 'Unit':  'dB', 'fmt': '.6f'}}

    output_parameters = {
        'new_parameter1': {'LSL': -np.inf, 'LTL':  np.nan, 'Nom':  0.0, 'UTL': np.nan, 'USL': np.inf, '10ᵡ': '', 'Unit': '?', 'fmt': '.3f'},
        'new_parameter2': {'LSL': -np.inf, 'LTL': -5000.0, 'Nom': 10.0, 'UTL':   15.0, 'USL': np.inf, '10ᵡ': '', 'Unit': '?', 'fmt': '.1f'},
        'new_parameter3': {'LSL': -np.inf, 'LTL':  np.nan, 'Nom':  0.0, 'UTL': np.nan, 'USL': np.inf, '10ᵡ': '', 'Unit': '?', 'fmt': '.6f'},
        'new_parameter4': {'LSL': -np.inf, 'LTL':  np.nan, 'Nom':  0.0, 'UTL': np.nan, 'USL': np.inf, '10ᵡ': '', 'Unit': '?', 'fmt': '.3f'}}

    # tippprint(None, input_parameters)
    toppprint(None, output_parameters)
