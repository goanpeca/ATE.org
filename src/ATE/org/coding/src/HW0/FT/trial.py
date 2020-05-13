#!/usr/bin/env conda run -n ATE python
# -*- coding: utf-8 -*-
"""
Created on Tuesday, May 12 2020 @ 20:15:47 (Q2 20202)
By tom
"""

from . import common as ci  # ci = Common Instance


class trial(trial_BC):
    '''line1
    line2
    '''

    # Input Parameter   | Shmoo | Min | Default  | Max | Unit | fmt
    # ------------------+-------+-----+----------+-----+------+----
    # ip.Temperature    |  Yes  | -40 |    25    | 170 | °C   | .0f
    # ip.new_parameter1 |  No   |  -∞ |  0.000   | +∞  | μV   | .3f
    # ip.new_parameter2 |  No   |  -∞ | 0.123457 | +∞  | dB   | .6f

    # Parameter         | LSL |   (LTL) |   Nom    | (UTL) | USL  | Unit | fmt
    # ------------------+-----+---------+----------+-------+------+------+----
    # op.new_parameter1 |  -∞ |    (-∞) |  0.000   | (+∞)  | +∞   | ?    | .3f
    # op.new_parameter2 |  -∞ | -5000.0 |   10.0   | 15.0  | +∞   | ?    | .1f
    # op.new_parameter3 |  -∞ |    (-∞) | 0.000000 | (+∞)  | +∞   | ?    | .6f
    # op.new_parameter4 |  -∞ |    (-∞) |  0.000   | (+∞)  | +∞   | ?    | .3f

    def do(self, ip, op):
        """Default implementation for the 'trial' test."""
        print(f"hardware = {instance.hardware}")
        print(f"base = {instance.base}")

        print(ip.Temperature)
        print(ip.new_parameter1)
        print(ip.new_parameter2)

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
