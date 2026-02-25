# -*- coding: utf-8 -*-
"""
Created on Mon Feb 23 16:41:36 2026

@author: babreu
"""

import matplotlib.pyplot as plt
import gdsfactory as gf


plt.close('all')

gf.gpdk.PDK.activate()

# Create a blank Component
p = gf.Component()

# Add a polygon.
xpts = [0, 0, 5, 6, 9, 12]
ypts = [0, 1, 1, 2, 2, 0]
# The zip function takes two lists (xpts and ypts) and pairs their elements together. 
# The first element of xpts is paired with the first of ypts, the second with the second, and so on.
# This creates a sequence of (x, y) tuples. A tuple is a data structure that consists of multiple parts.
# list(...): The output of zip is converted into a list of these coordinate tuples.
p.add_polygon(list(zip(xpts, ypts)), layer=(2, 0))

# Plot the Component with the polygon in it.
p.plot()


c = gf.Component()
poly_ref = c.add_ref(p)
poly_ref1 = c.add_ref(p)
poly_ref2 = c.add_ref(p)

poly_ref.rotate(90)
poly_ref2.rotate(180)

c.plot()


#%%
# Add a 2nd polygon to "p".
xpts = [14, 14, 16, 16]
ypts = [0, 2, 2, 0]
p.add_polygon(list(zip(xpts, ypts)), layer=(1, 0))
p
c

#%%
c2 = gf.Component()
d_ref1 = c2.add_ref(c)  # Reference the Component "c" that 3 references in it.
d_ref2 = c2 << c  # Use the "<<" operator to create a 2nd reference to c.plot().
d_ref3 = c2 << c 

d_ref1.move((20, 0))
d_ref2.move((40, 0))

c2

#%%
c = gf.Component()
wr1 = c << gf.components.straight(width=0.6)
wr2 = c << gf.components.straight(width=0.6)
wr2.movey(10)

c.plot()

# This takes the ports from the bottom waveguide (wr1), which are named o1 and o2, and adds them to c with the prefix "bot_".
# The new ports on c will be named bot_o1 and bot_o2.
c.add_ports(wr1.ports, prefix="bot_")

# This does the same for the upper waveguide (wr2), creating 2 new ports on c named top_o1 and top_o2.
c.add_ports(wr2.ports, prefix="top_")

c.pprint_ports()
c.auto_rename_ports()

c.pprint_ports()






























