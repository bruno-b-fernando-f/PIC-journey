# -*- coding: utf-8 -*-
"""
Created on Mon Feb 23 17:51:46 2026

@author: babreu
"""
import gdsfactory as gf

c3 = gf.Component() 
c = gf.components.straight(length=1)

# This is the key step where the array is created.
# The add_ref function is used to place the unit cell c into the main component c3, but with additional parameters to create a grid:
# columns=2, rows=2: This specifies a 2x2 grid.
# column_pitch=10: The horizontal distance between the centers of adjacent columns is 10 µm.
# row_pitch=20: The vertical distance between the centers of adjacent rows is 20 µm.
# The variable aref holds a reference to this entire array.
aref = c3.add_ref(c, columns=2, rows=2, column_pitch=10, row_pitch=20)  
c3.add_ports(aref.ports) # The ports are then automatically named to indicate the position in the array (o1_0_0, o2_0_0, o1_1_0, o2_1_0, etc.).

# Reference the Component "c" 4 references in it with a 2 rows, 2 columns array.
c3.pprint_ports()
c3.draw_ports()
c3

#%%
c = gf.Component()
b = c << gf.components.bend_euler()
s = c.add_ref(
    gf.components.straight(length=1),
    rows=2,
    row_pitch=10,
    columns=2,
    column_pitch=10,
)
b.connect("o1", s["o2", 1, 1], mirror = True)
c

#%%
c4 = gf.Component()
c = gf.components.straight(length=1)
aref = c4 << gf.components.array(component=c, columns=2, rows=2, row_pitch=10, column_pitch=10)
c4.add_ports(aref.ports)
c4.pprint_ports()
c4.show()

















