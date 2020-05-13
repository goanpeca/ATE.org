#!/usr/bin/env conda run -n ATE python
# -*- coding: utf-8 -*-
"""
Created on Tuesday, May 12 2020 @ 11:49:35 (Q2 20202)
By tom
"""

import numpy as np
import .common


class TSTTemplate(TSTTemplateBC):
    '''line1
    line2
    '''

    def do(self, ip, op):
        op.new_parameter1 = self.randn('new_parameter1')
        op.new_parameter2 = self.randn('new_parameter2')
        op.new_parameter3 = self.randn('new_parameter3')
        op.new_parameter4 = self.randn('new_parameter4')


if __name__ == '__main__':
    import os
    tester = os.environ.get('TESTER')
    tester_mode = os.environ.get('TESTERMODE')
    if tester_mode == 'DIRECT':
        pass  # TODO: implement
    else:  # 'INTERACTIVE'
        from ATE.org import TestRunner
        testRunner = TestRunner(__file__)
