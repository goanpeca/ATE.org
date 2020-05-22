# -*- coding: utf-8 -*-
"""
Created on Tue May  5 14:52:34 2020

@author: hoeren
"""

hardware = 'HW0'
base = 'FT'
target = 'blablabla'
USER_TXT = 'H2LHH'
sampleRate = 1.0
temperature = '25'

from ATE.org.sequencers import FixedTemperatureSequencer
fts = FixedTemperatureSequencer(temperature, sampleRate)

import .fubar
fts.registerTest(fubar, {call_values}, {limits}, {SBINs})

import .fu
fts.registerTest(fu, {CallValues}, {Limits}, {SBINs})

# ...


{SBINs} = {
    'Contact_resistance' : (0, 'Contact Fail'),
    'IDD_NewSubItem' : (16, 'Digital Fail'),
    ...
    'Sensitive_SomeParameter' : (72, 'Digital Fail')}


SBIN
0 - Contact fail
1 - Good A grade
2 - Good B
3
4
5
6
7
8
9 - Good I grade
10 - 1st fail bin
11 - ...



if __name__ == '__main__':
	fts.run()
    fts.registerTCC(...)