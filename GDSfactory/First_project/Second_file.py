# -*- coding: utf-8 -*-
"""
Created on Mon Feb 23 15:28:26 2026

@author: babreu
"""


import gdsfactory as gf

gf.gpdk.PDK.activate()
c = gf.Component()
c.add_polygon([(-8, -6), (6, 8), (7, 17), (9, 5)], layer=(1, 0))
c.plot()

def bend(radius: float = 5) -> gf.Component:
    return gf.components.bend_euler(radius=radius)

component = bend(radius=10)

component.plot()