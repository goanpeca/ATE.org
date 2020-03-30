# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 11:53:18 2020

@author: hoeren

This module comprises the device driver used by ATE.org to communicate
with the Accretech PM90 model probers.

https://www.accretech.eu/en/#
https://www.accretech.eu/en/products/semiconductor/wafer-probing-machines/

TODO: add the communication 'datasheet' to the doc tree

"""
from ATE.equipment.probers import proberABC

class pm90(proberABC):
    pass


if __name__ == '__main__':
    pass