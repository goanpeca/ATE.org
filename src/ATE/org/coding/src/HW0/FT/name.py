#!/usr/bin/env conda run -n ATE python
# -*- coding: utf-8 -*-
from ATE.org.abc import testABC
# import .common


class name(testABC):
    '''
    Created on Tuesday, May 12 2020 @ 06:06:40 (Q2 20202) (Q2 20192)
    By @author: tom ()
    '''

    hardware = 'HW0'
    base = 'FT'
    Type = ''

    input_parameters = {
        'Temperature': {'Min': {'Shmoo': True, 'Min': -40.0, 'Default': 25.0, 'Max': 170.0, '10ᵡ': '', 'Unit': '°C', 'fmt': '.0f'}},
        'new_parameter1': {'Min': {'Shmoo': False, 'Min': -inf, 'Default': 0.0, 'Max': inf, '10ᵡ': 'μ', 'Unit': 'V', 'fmt': '.3f'}},
        'new_parameter2': {'Min': {'Shmoo': False, 'Min': -inf, 'Default': 0.0, 'Max': inf, '10ᵡ': '', 'Unit': 'dB', 'fmt': '.6f'}},
    }

    output_parameters = {
    }

    def do(self, ip, op, gp, dm):
        print("Doing %s test ..." % self.__class__.__name__.split("_")[0])

    def do_target(self, ip, op, gp, dm):
        return self.do(ip, op, gp, dm)


if __name__ == '__main__':
    import os
    tester = os.environ.get('TESTER')
    tester_mode = os.environ.get('TESTERMODE')
    if tester_mode == 'DIRECT':
        pass  # TODO: implement
    else:  # 'INTERACTIVE'
        from ATE.org import TestRunner
        testRunner = TestRunner(__file__)
