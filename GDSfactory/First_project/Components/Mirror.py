# -*- coding: utf-8 -*-
"""
Created on Mon Feb 23 16:37:25 2026

@author: babreu
"""

import gdsfactory as gf
from gdsfactory.gpdk import PDK
import matplotlib.pyplot as plt



plt.close('all')

c = gf.Component()
# This line adds a reference (an instance) of a standard mmi1x2 component to c. 
# An MMI is a common device used in photonics to split one input signal into two output signals.
mmi = c.add_ref(gf.components.mmi2x2())
# This adds a reference to a bend_circular component, which is a simple 90-degree curved waveguide.
bend = c.add_ref(gf.components.bend_circular(layer=(1, 0)))
c.plot()

bend.connect("o2", mmi.ports["o4"], mirror = False)  # Connects follow Source -> Destination syntax.
c.plot()