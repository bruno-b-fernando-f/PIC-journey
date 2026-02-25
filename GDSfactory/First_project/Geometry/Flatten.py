# -*- coding: utf-8 -*-
"""
Created on Mon Feb 23 18:28:00 2026

@author: babreu
"""


import gdsfactory as gf

c = gf.Component()
e = c << gf.components.ellipse(
    radii=(10, 5), layer=(1, 0)
)  # Ellipse. equivalent to c.add_ref(gf.components.ellipse(radii=(10, 5), layer=(1, 0)).
r = c << gf.components.rectangle(
    size=(15, 5), layer=(2, 0)
)  # Rectangle. equivalent to c.add_ref(gf.components.rectangle(size=(15, 5), layer=(2, 0)).
print(len(c.insts))  # 2 component instances.

# This command flattens the component c, removing all levels of hierarchy.
# It replaces all instances (references) of sub-components with copies of their raw geometric shapes.
c.flatten()
print(len(c.insts))  # 0 in the flattened component.
c