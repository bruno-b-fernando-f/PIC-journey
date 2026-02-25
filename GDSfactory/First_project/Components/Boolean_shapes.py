# -*- coding: utf-8 -*-
"""
Created on Mon Feb 23 16:32:58 2026

@author: babreu
"""

import gdsfactory as gf
from gdsfactory.gpdk import PDK
import matplotlib.pyplot as plt


PDK.activate()

plt.close('all')

c = gf.Component()
e1 = c.add_ref(gf.components.ellipse(layer=(2, 0)))
e2 = c.add_ref(gf.components.ellipse(layer=(2, 0))).movex(2)
c.plot()

c2 = gf.boolean(A=e2, B=e1, operation="not", layer=(2, 0))
c2.plot()

c3 = gf.boolean(A=e2, B=e1, operation="and", layer=(2, 0))
c3.plot()

c4 = gf.boolean(A=e2, B=e1, operation="or", layer=(2, 0))
c4.plot()

c5 = gf.boolean(A=e2, B=e1, operation="xor", layer=(2, 0))
c5.plot()