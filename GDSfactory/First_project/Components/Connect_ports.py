# -*- coding: utf-8 -*-
"""
Created on Mon Feb 23 16:00:52 2026

@author: babreu
"""

import gdsfactory as gf
from gdsfactory.gpdk import PDK
import matplotlib.pyplot as plt


PDK.activate()

#%%


def straight(length=10, width: float = 1, layer=(1, 0)): 
    c = gf.Component()
    c.add_polygon([(0, 0), (length, 0), (length, width), (0, width)], layer=layer) # This draws the main rectangular body of the waveguide.
    c.add_port( # This adds two connection points, or ports, which are essential for connecting this component to others.
        name="o1", center=(0, width / 2), width=width, orientation=180, layer=layer # "o1" is the input port and is facing left due to rotation (orientation=180)
    )
    c.add_port(
        name="o2", center=(length, width / 2), width=width, orientation=0, layer=layer # "o2" is the output port and is facing right.
    )
    return c

#%%
c = gf.Component()

# Three waveguides are created. They have different lengths and sit on different layers, but all have the same width.
wg1 = c << straight(length=6, width=2.5, layer=(1, 0)) 
wg2 = c << straight(length=6, width=2.5, layer=(2, 0))
wg3 = c << straight(length=15, width=2.5, layer=(3, 0))
wg2.movey(10) # This moves wg2 up by 10 µm.
wg2.rotate(10) # this rotates wg2 by 10 degrees.

wg3.movey(20) # This moves wg3 up by 20 µm.
wg3.rotate(15) # This rotates wg3 by 15 degrees.

c.plot()

#%%
# Let us keep wg1 in place on the bottom, and connect the other straights to it.
# To do that, on wg2 we will take the "o1" port and connect it to the "o2" on wg1:
wg2.connect("o1", wg1.ports["o2"], allow_layer_mismatch=True)


# Next, on wg3 let us take the "o1" port and connect it to the "o2" on wg2:
wg3.connect("o1", wg2.ports["o2"], allow_layer_mismatch=True)
    
c.plot()



#%%
c.add_port("o1", port=wg1.ports["o1"]) 
c.add_port("o2", port=wg3.ports["o2"])
c.draw_ports()
c.plot()

#%%
c2 = gf.Component()
wg1 = straight(length=10)
wg2 = straight(length=10, layer=(2, 0))
mwg1_ref = c2.add_ref(wg1)
mwg2_ref = c2.add_ref(wg2)
mwg2_ref.movex(10) # This moves mwg2_ref to the right by 10µm.
c2.plot()

mwg1_ref.connect(port="o2", other=mwg2_ref.ports["o1"], allow_layer_mismatch=True)
c2.plot()

c2.add_label(text="First label", position=mwg1_ref.dcenter)
c2.add_label(text="Second label", position=mwg2_ref.dcenter)

c2.add_label(
    # An f-string (text) is used to create a dynamic and multi-line (\n) label. 
    # It automatically calculates the total width of the component (c2.xsize) and embeds it in the text.
    text=f"The x size of this\nlayout is {c2.xsize}",
    position=(c2.x, c2.y), # The label is placed at the component's origin (c2.x, c2.y), which is typically (0, 0).
    layer=(10, 0), # The label is placed on layer 10.
)


c2.plot()






















