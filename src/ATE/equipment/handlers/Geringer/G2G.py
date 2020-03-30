# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 12:31:22 2020

@author: hoeren

This module comprises the device driver used by ATE.org to communicate
with the Geringer G2G strip handler.

https://www.geringer.de/de/produkte/sondermaschinenbau

TODO: protocol is multiple multi-site ... got something from Ulf, need to
give it a place here, and make it conform the ABC of handlers

TODO: add the communication 'datasheet' to the doc tree

"""
from ATE.equipment import handlerABC

class g2g(handlerABC):
    pass


if __name__ == '__main__':
    pass