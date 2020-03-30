# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 13:33:33 2020

@author: hoeren

This module comprises the device driver used by ATE.org to communicate
with the MPI Thermal TA-3000A thermo-streamer.

https://mpi-thermal.com/
https://mpi-thermal.com/products/ta-3000a/

TODO: add the communication 'datasheet' to the doc tree

"""
from ATE.equipment import ThermoABC

class ta3000a(ThermoABC):
    pass


if __name__ == '__main__':
    pass