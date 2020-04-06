# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 13:31:45 2020

@author: hoeren

This module comprises the device driver used by ATE.org to communicate
with the TempTronic ATS710 thermo-streamer.

https://www.intestthermal.com/
https://www.intestthermal.com/products/thermostream-air-forcing-systems/configurations
https://www.intestthermal.com/high-speed-mobile-temperature-environments-710m

TODO: add the communication 'datasheet' to the doc tree

"""
from ATE.equipment import ThermoABC

class ats710(ThermoABC):
    pass


if __name__ == '__main__':
    pass