#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 07:22:29 2020

@author: tom

References:
    PEP8 : https://www.python.org/dev/peps/pep-0008/
    numpy doc style : https://numpydoc.readthedocs.io/en/latest/format.html

"""
import os
import numpy as np
from ATE.utils.DT import DT
import getpass
from jinja2 import FileSystemLoader, Environment


def generate_module_docstring():
    retval = []

    line = f"Created on {str(DT())}"
    retval.append(line)

    line = "By "
    user = getpass.getuser()
    line += user
    domain = str(os.environ.get('USERDNSDOMAIN'))
    if domain != 'None':
        line += f" ({user}@{domain})".lower()
    retval.append(line)
    return retval


def generate_input_parameters_table(ip):
    """Generates a list of strings, holding a talble (with header) of the input parameters"""

    retval = []
    name_ = 0
    Shmoo_ = 3  # True = Yes, False = No
    Min_ = 0
    Default_ = 0
    Max_ = 0
    Unit_ = 0
    fmt_ = 0
    for param in ip:
        if len(f"ip.{param}") > name_:
            name_ = len(f"ip.{param}")
    # Min --> number or -inf (no nan)
        if np.isinf(ip[param]['Min']):
            length = len('-∞')
            if Min_ < length:
                Min_ = length
        elif np.isnan(ip[param]['Min']):
            raise Exception(f"ip.{param}['Min'] == np.nan ... not possible !")
        else:
            length = len(f"{ip[param]['Min']:{ip[param]['fmt']}}")
            if Min_ < length:
                Min_ = length
    # Default --> number (no nan or inf)
        if np.isinf(ip[param]['Default']):
            raise Exception(f"ip.{param}['Default'] == ±np.inf ... not possible !")
        elif np.isnan(ip[param]['Default']):
            raise Exception(f"ip.{param}['Default'] == np.nan ... not possible !")
        else:
            length = len(f"{ip[param]['Default']:{ip[param]['fmt']}}")
            if Default_ < length:
                Default_ = length
    # Max --> number or inf (no nan)
        if np.isinf(ip[param]['Max']):
            length = len('+∞')
            if Max_ < length:
                Max_ = length
        elif np.isnan(ip[param]['Max']):
            raise Exception(f"ip.{param}['Max'] == np.nan ... not possible !")
        else:
            length = len(f"{ip[param]['Max']:{ip[param]['fmt']}}")
            if Max_ < length:
                Max_ = length
    # combined Unit
        length = len(f"{ip[param]['10ᵡ']}{ip[param]['Unit']}")
        if Unit_ < length:
            Unit_ = length
    # format
        length = len(f"{ip[param]['fmt']}")
        if fmt_ < length:
            fmt_ = length

    length = len('Input Parameter')
    if name_ < length:
        name_ = length

    length = len('Shmoo')
    if Shmoo_ < length:
        Shmoo_ = length

    length = len('Min')
    if Min_ < length:
        Min_ = length

    length = len('Default')
    if Default_ < length:
        Default_ = length

    length = len('Max')
    if Max_ < length:
        Max_ = length

    length = len('Unit')
    if Unit_ < length:
        Unit_ = length

    length = len('fmt')
    if fmt_ < length:
        fmt_ = length

    th = f"{'Input Parameter':<{name_}} | "
    th += f"{'Shmoo':^{Shmoo_}} | "
    th += f"{'Min':>{Min_}} | "
    th += f"{'Default':^{Default_}} | "
    th += f"{'Max':<{Max_}} | "
    th += f"{'Unit':>{Unit_}} | "
    th += f"{'fmt':>{fmt_}}"
    retval.append(th)

    bh = '-' * (name_ + 1) + '+'
    bh += '-' * (Shmoo_ + 2) + '+'
    bh += '-' * (Min_ + 2) + '+'
    bh += '-' * (Default_ + 2) + '+'
    bh += '-' * (Max_ + 2) + '+'
    bh += '-' * (Unit_ + 2) + '+'
    bh += '-' * (fmt_ + 1)
    retval.append(bh)

    for index, param in enumerate(ip):
        name = f"ip.{param}"
        Name = f"{name:{name_}} | "
    # Shmoo
        if ip[param]['Shmoo'] is True:
            Shmoo = f"{'Yes':^{Shmoo_}} | "
        else:
            Shmoo = f"{'No':^{Shmoo_}} | "
    # Min
        if np.isinf(ip[param]['Min']):
            Min = f"{'-∞':>{Min_}} | "
        else:
            Min = f"{ip[param]['Min']:>{Min_}{ip[param]['fmt']}} | "
    # Default
        Default = f"{ip[param]['Default']:^{Default_}{ip[param]['fmt']}} | "
    # Max
        if np.isinf(ip[param]['Max']):
            Max = f"{'+∞':<{Max_}} | "
        else:
            Max = f"{ip[param]['Max']:<{Max_}{ip[param]['fmt']}} | "
    # Unit
        cu = ip[param]['10ᵡ'] + ip[param]['Unit']
        Unit = f"{cu:<{Unit_}} | "
    # format
        Fmt = f"{ip[param]['fmt']:<{fmt_}}"

        line = Name + Shmoo + Min + Default + Max + Unit + Fmt
        retval.append(line)
    return retval


def generate_input_parameters_ppd(ip):
    '''Test Input Parameters Pretty Print Dict.

    This function creates a list of strings that 'pretty print' the dictionary.
    '''

    retval = []
    for index, param in enumerate(ip):
        if index == len(ip) - 1:
            line = f"'{param}': {ip[param]}}}"
        else:
            line = f"'{param}': {ip[param]},"
        line = line.replace('nan', 'np.nan')
        line = line.replace('inf', 'np.inf')
        retval.append(line)
    return retval


def generate_output_parameters_table(op):
    """Generates a list of strings, holding a talble (with header) of the output parameters"""

    retval = []
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
        if len(f"op.{param}") > name_:
            name_ = len(f"op.{param}")
    # LSL --> inf or number (no nan)
        if np.isinf(op[param]['LSL']):
            if LSL_ < 2:
                LSL_ = 2  # len('-∞') = 2
        else:
            length = len(f"{op[param]['LSL']:{op[param]['fmt']}}")
            if LSL_ < length:
                LSL_ = length
    # LTL --> inf, nan or number
        if np.isinf(op[param]['LTL']):
            if LTL_ < 2:
                LTL_ = 2  # len('-∞') = 2
        elif np.isnan(op[param]['LTL']):
            if not np.isinf(op[param]['LSL']):
                length = len(f"{op[param]['LSL']:{op[param]['fmt']}}") + 2  # the '()' around
                if LTL_ < length:
                    LTL_ = length
        else:
            length = len(f"{op[param]['LTL']:{op[param]['fmt']}}")
            if LTL_ < length:
                LTL_ = length
    # Nom --> number (no inf, no nan)
        length = len(f"{op[param]['Nom']:{op[param]['fmt']}}")
        if length > Nom_:
            Nom_ = length
    # UTL --> inf, nan or number
        if np.isinf(op[param]['UTL']):
            if UTL_ < 2:
                UTL_ = 2
        elif np.isnan(op[param]['UTL']):
            if not np.isinf(op[param]['USL']):
                length = len(f"{op[param]['USL']:{op[param]['fmt']}}") + 2
                if UTL_ < length:
                    UTL_ = length
        else:
            length = len(f"{op[param]['UTL']:{op[param]['fmt']}}")
            if UTL_ < length:
                UTL_ = length
    # USL --> inf or number (not nan)
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

    length = len('Output Parameters')
    if name_ < length:
        name_ = length

    length = len('LSL')
    if LSL_ < length:
        LSL_ = length

    length = len('(LTL)')
    if LTL_ < length:
        LTL_ = length

    length = len('(UTL)')
    if UTL_ < length:
        UTL_ = length

    length = len('USL')
    if USL_ < length:
        USL_ = length

    Unit_ = mul_ + unit_
    length = len('Unit')
    if Unit_ < length:
        Unit_ = length

    length = len('fmt')
    if fmt_ < length:
        fmt_ = length

    th = f"{'Parameter':<{name_}} | "
    th += f"{'LSL':>{LSL_}} | "
    th += f"{'(LTL)':>{LTL_}} | "
    th += f"{'Nom':^{Nom_}} | "
    th += f"{'(UTL)':<{UTL_}} | "
    th += f"{'USL':<{USL_}} | "
    th += f"{'Unit':>{Unit_}} | "
    th += f"{'fmt':>{fmt_}}"
    retval.append(th)

    bh = '-' * (name_ + 1) + '+'
    bh += '-' * (LSL_ + 2) + '+'
    bh += '-' * (LTL_ + 2) + '+'
    bh += '-' * (Nom_ + 2) + '+'
    bh += '-' * (UTL_ + 2) + '+'
    bh += '-' * (USL_ + 2) + '+'
    bh += '-' * (Unit_ + 2) + '+'
    bh += '-' * (fmt_ + 1)
    retval.append(bh)

    for index, param in enumerate(op):
        name = f"op.{param}"
        Name = f"{name:<{name_}} | "
    # LSL
        if np.isinf(op[param]['LSL']):
            LSL = f"{'-∞':>{LSL_}} | "
        else:
            LSL = f"{op[param]['LSL']:>{LSL_}{op[param]['fmt']}} | "
    # LTL
        if np.isinf(op[param]['LTL']):
            LTL = f"{'-∞':>{LTL_}} | "
        elif np.isnan(op[param]['LTL']):
            if np.isinf(op[param]['LSL']):
                LTL = f"{'(-∞)':>{LTL_}} | "
            else:
                ltl = f"({op[param]['LSL']:{op[param]['fmt']}})"
                LTL = f"{ltl:>{LTL_}} | "
        else:
            LTL = f"{op[param]['LTL']:>{LTL_}{op[param]['fmt']}} | "
    # Nom
        Nom = f"{op[param]['Nom']:^{Nom_}{op[param]['fmt']}} | "
    # UTL
        if np.isinf(op[param]['UTL']):
            UTL = f"{'+∞':<{UTL_}} | "
        elif np.isnan(op[param]['UTL']):
            if np.isinf(op[param]['USL']):
                UTL = f"{'(+∞)':<{UTL_}} | "
            else:
                utl = f"({op[param]['USL']:{op[param]['fmt']}})"
                UTL = f"{utl:<{UTL_}} | "
        else:
            UTL = f"{op[param]['UTL']:<{UTL_}{op[param]['fmt']}} | "
    # USL
        if np.isinf(op[param]['USL']):
            USL = f"{'+∞':<{USL_}} | "
        else:
            USL = f"{op[param]['USL']:<{USL_}{op[param]['fmt']}} | "
    # Unit
        cu = op[param]['10ᵡ'] + op[param]['Unit']
        Unit = f"{cu:<{Unit_}} | "
    # format
        Fmt = f"{op[param]['fmt']:<{fmt_}}"

        line = Name + LSL + LTL + Nom + UTL + USL + Unit + Fmt
        retval.append(line)
    return retval


def generate_output_parameters_ppd(op):
    """Test Output Parameters Pretty Print Dict.

    This function creates a list of strings that 'pretty print' the dictionary.
    """

    retval = []
    for index, param in enumerate(op):
        if index == len(op) - 1:
            line = f"'{param}': {op[param]}}}"
        else:
            line = f"'{param}': {op[param]},"
        line = line.replace('nan', 'np.nan')
        line = line.replace('inf', 'np.inf')
        retval.append(line)
    return retval


def test_generator(project_path, definition):
    test_base_generator(project_path, definition)
    test_proper_generator(project_path, definition)
    test__init__generator(project_path, definition)


class test_proper_generator:
    """Generator for the Test Class."""

    def __init__(self, project_path, definition):
        template_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
        file_loader = FileSystemLoader(template_path)
        env = Environment(loader=file_loader)
        env.trim_blocks = True
        env.lstrip_blocks = True
        env.rstrip_blocks = True
        template_name = str(self.__class__.__name__).split('.')[-1].split(' ')[0]
        template_name = template_name.replace('generator', 'template') + '.jinja2'
        template = env.get_template(template_name)

        hardware = definition['hardware']
        base = definition['base']
        name = definition['name']
        file_name = f"{name}.py"

        rel_path_to_dir = os.path.join('src', hardware, base, name)
        abs_path_to_dir = os.path.join(project_path, rel_path_to_dir)
        abs_path_to_file = os.path.join(abs_path_to_dir, file_name)

        msg = template.render(
            module_doc_string=generate_module_docstring(),
            input_parameter_table=generate_input_parameters_table(definition['input_parameters']),
            output_parameter_table=generate_output_parameters_table(definition['output_parameters']),
            definition=definition)

        if not os.path.exists(abs_path_to_dir):
            os.makedirs(abs_path_to_dir)
        f = open(abs_path_to_file, 'w', encoding='utf-8')
        f.write(msg)


class test_base_generator:
    """Generator for the Test Base Class."""

    def __init__(self, project_path, definition):
        template_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
        file_loader = FileSystemLoader(template_path)
        env = Environment(loader=file_loader)
        env.trim_blocks = True
        env.lstrip_blocks = True
        env.rstrip_blocks = True
        template_name = str(self.__class__.__name__).split('.')[-1].split(' ')[0]
        template_name = template_name.replace('generator', 'template') + '.jinja2'
        template = env.get_template(template_name)

        hardware = definition['hardware']
        base = definition['base']
        name = definition['name']
        file_name = f"{name}_BC.py"

        rel_path_to_dir = os.path.join('src', hardware, base, name)
        abs_path_to_dir = os.path.join(project_path, rel_path_to_dir)
        abs_path_to_file = os.path.join(abs_path_to_dir, file_name)

        msg = template.render(
            module_doc_string=generate_module_docstring(),
            ipppd=generate_input_parameters_ppd(definition['input_parameters']),
            opppd=generate_output_parameters_ppd(definition['output_parameters']),
            definition=definition)

        if not os.path.exists(abs_path_to_dir):
            os.makedirs(abs_path_to_dir)
        f = open(abs_path_to_file, 'w', encoding='utf-8')
        f.write(msg)


class test__init__generator:
    """Generator for the __init__.py file of a given test."""

    def __init__(self, project_path, definition):
        template_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
        file_loader = FileSystemLoader(template_path)
        env = Environment(loader=file_loader)
        env.trim_blocks = True
        env.lstrip_blocks = True
        env.rstrip_blocks = True
        template_name = str(self.__class__.__name__).split('.')[-1].split(' ')[0]
        template_name = template_name.replace('generator', 'template') + '.jinja2'
        template = env.get_template(template_name)

        hardware = definition['hardware']
        base = definition['base']
        name = definition['name']
        file_name = '__init__.py'

        rel_path_to_dir = os.path.join('src', hardware, base, name)
        abs_path_to_dir = os.path.join(project_path, rel_path_to_dir)
        abs_path_to_file = os.path.join(abs_path_to_dir, file_name)

        imports = []
        for item in os.listdir(abs_path_to_dir):
            if item.upper().endswith('_BC.PY'):
                what = '.'.join(item.split('.')[:-1])
                imports.append(f"from {what} import {what}")

        msg = template.render(
            hardware=hardware,
            base=base,
            name=name,
            imports=imports)

        if not os.path.exists(abs_path_to_dir):
            os.makedirs(abs_path_to_dir)
        f = open(abs_path_to_file, 'w', encoding='utf-8')
        f.write(msg)


def test_program_generator(project_path, definition):
    pass


class HW_common_generator:
    pass


class FT_common_generator:
    pass


class PR_common_generatror:
    pass


class src__init__generator:
    """Generator for the __init__.py file of the src (root)"""
    pass


class HW__init__generator:
    pass


class FT__init__generator:
    """Generator for the __init__.py file of 'FT' for the given hardware."""

    def __init__(self, project_path, hardware):
        template_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
        file_loader = FileSystemLoader(template_path)
        env = Environment(loader=file_loader)
        env.trim_blocks = True
        env.lstrip_blocks = True
        env.rstrip_blocks = True
        template_name = str(self.__class__.__name__).split('.')[-1].split(' ')[0]
        template_name = template_name.replace('generator', 'template') + '.jinja2'
        template = env.get_template(template_name)

        file_name = '__init__.py'
        rel_path_to_dir = os.path.join('src', hardware, 'FT')
        abs_path_to_dir = os.path.join(project_path, rel_path_to_dir)
        abs_path_to_file = os.path.join(abs_path_to_dir, file_name)

        imports = []
        for item in os.listdir(abs_path_to_dir):
            if item.upper().endswith('_BC.PY'):
                what = '.'.join(item.split('.')[:-1])
                imports.append(f"from {what} import {what}")

        msg = template.render(
            hardware=hardware,
            imports=imports)

        if not os.path.exists(abs_path_to_dir):
            os.makedirs(abs_path_to_dir)
        f = open(abs_path_to_file, 'w', encoding='utf-8')
        f.write(msg)


class PR__init__generator:
    """Generator for the __init__.py file of 'PR' for the given hardware."""

    def __init__(self, project_path, hardware):
        template_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
        file_loader = FileSystemLoader(template_path)
        env = Environment(loader=file_loader)
        env.trim_blocks = True
        env.lstrip_blocks = True
        env.rstrip_blocks = True
        template_name = str(self.__class__.__name__).split('.')[-1].split(' ')[0]
        template_name = template_name.replace('generator', 'template') + '.jinja2'
        template = env.get_template(template_name)

        file_name = '__init__.py'
        rel_path_to_dir = os.path.join('src', hardware, 'PR')
        abs_path_to_dir = os.path.join(project_path, rel_path_to_dir)
        abs_path_to_file = os.path.join(abs_path_to_dir, file_name)

        imports = []
        for item in os.listdir(abs_path_to_dir):
            if item.upper().endswith('_BC.PY'):
                what = '.'.join(item.split('.')[:-1])
                imports.append(f"from {what} import {what}")

        msg = template.render(
            hardware=hardware,
            imports=imports)

        if not os.path.exists(abs_path_to_dir):
            os.makedirs(abs_path_to_dir)
        f = open(abs_path_to_file, 'w', encoding='utf-8')
        f.write(msg)






if __name__ == '__main__':
    definition = {
        'name' : 'trial',
        'type' : 'custom',
        'hardware' : 'HW0',
        'base' : 'FT',
        'doc_string' : ['line1', 'line2'],
        'input_parameters' : {
            'Temperature' : {'Shmoo': True, 'Min': -40.0, 'Default': 25.0, 'Max': 170.0, '10ᵡ': '', 'Unit': '°C', 'fmt': '.0f'},
            'new_parameter1': {'Shmoo': False, 'Min': -np.inf, 'Default': 0.0, 'Max': np.inf, '10ᵡ': 'μ', 'Unit':  'V', 'fmt': '.3f'},
            'new_parameter2': {'Shmoo': False, 'Min': -np.inf, 'Default':  0.123456789, 'Max': np.inf, '10ᵡ':  '', 'Unit':  'dB', 'fmt': '.6f'}},
        'output_parameters' : {
            'new_parameter1': {'LSL': -np.inf, 'LTL':  np.nan, 'Nom':  0.0, 'UTL': np.nan, 'USL': np.inf, '10ᵡ': '', 'Unit': '?', 'fmt': '.3f'},
            'new_parameter2': {'LSL': -np.inf, 'LTL': -5000.0, 'Nom': 10.0, 'UTL':   15.0, 'USL': np.inf, '10ᵡ': '', 'Unit': '?', 'fmt': '.1f'},
            'new_parameter3': {'LSL': -np.inf, 'LTL':  np.nan, 'Nom':  0.0, 'UTL': np.nan, 'USL': np.inf, '10ᵡ': '', 'Unit': '?', 'fmt': '.6f'},
            'new_parameter4': {'LSL': -np.inf, 'LTL':  np.nan, 'Nom':  0.0, 'UTL': np.nan, 'USL': np.inf, '10ᵡ': '', 'Unit': '?', 'fmt': '.3f'}},
        'dependencies' : {}}

    project_path = os.path.dirname(__file__)
    dump_dir = os.path.join(project_path, 'src', definition['hardware'], definition['base'])
    if not os.path.exists(dump_dir):
        os.makedirs(dump_dir)

    for line in generate_module_docstring():
        print(line)
    print()

    test_generator(project_path, definition)
    definition['base'] = 'PR'
    test_generator(project_path, definition)

    for line in generate_input_parameters_table(definition['input_parameters']):
        print(line)
    print()

    for line in generate_input_parameters_ppd(definition['input_parameters']):
        print(line)
    print()

    for line in generate_output_parameters_table(definition['output_parameters']):
        print(line)
    print()

    for line in generate_output_parameters_ppd(definition['output_parameters']):
        print(line)

    PR__init__generator(project_path, 'HW0')
    FT__init__generator(project_path, 'HW0')
