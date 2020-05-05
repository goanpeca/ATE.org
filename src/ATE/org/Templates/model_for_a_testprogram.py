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


if __name__ == '__main__':
	fts.run()
    fts.registerTCC(...)