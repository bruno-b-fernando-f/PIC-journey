# -*- coding: utf-8 -*-
"""
Created on Mon Feb 23 18:30:01 2026

@author: babreu
"""

import gdsfactory as gf
from gdsfactory.gpdk import LAYER

c = gf.components.circle()
c2 = gf.Component()
region = c.get_region(layer=LAYER.WG, smooth=0.1)
c2.add_polygon(region, layer=LAYER.WG)
c2