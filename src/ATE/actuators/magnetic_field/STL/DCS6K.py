# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 12:44:38 2020

@author: hoeren

This module comprises the device driver used by ATE.org to communicate
with the STL 6KW coil driver.

http://www.stl-gmbh.de/en/

TODO: add the communication 'datasheet' to the doc tree

"""
from ATE.equipment import CoildriverABC

class dcs6k(CoildriverABC):
    pass


if __name__ == '__main__':
    pass