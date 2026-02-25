# -*- coding: utf-8 -*-
"""
Created on Mon Feb 23 15:37:05 2026

@author: babreu
"""

import gdsfactory as gf
from gdsfactory.gpdk import PDK
import matplotlib.pyplot as plt


PDK.activate()

# Create a blank component (essentially an empty GDS cell with some special features).
c = gf.Component()


# Create some new geometry from the functions available in the geometry library.
t = gf.components.text("Hello!", layer=(1,0))
r = gf.components.rectangle(size=(5, 10), layer=(2, 0))

# Add references to the new geometry to c, our blank component.
text1 = c.add_ref(t)  # Add the text we created as a reference.
# Using the << operator (identical to add_ref()), add the same geometry a second time.
text2 = c << t
r = c << r  # Add the rectangle we created.

# Now that the geometry has been added to "c", we can move everything around:
text1.movey(25)
text2.move((5, 30))
text2.rotate(45)
r.movex(-15)

print(c)
c.plot()

#%%
c = gf.Component()
p1 = c.add_polygon(
    [(-8, -6), (6, 8), (7, 17), (9, 5)],layer = (1,0) 
    )
p2 = c.get_region(layer=(1, 0))  # Get the region of the polygon.


p3 = p2.size(2000)  # Regions are in nm!

c.add_polygon(p3, layer=(2, 0))  # Add the region to the component.

c.plot()


#%%
c = gf.Component()
p1 = c.add_polygon(
    [(-8, -6), (6, 8), (7, 17), (9, 5)], layer=(1, 0)
)  # Polygons are in um.
r1 = c.get_region(layer=(1,0))  # Regions are in DBU (1 nm in this case).
r2 = r1.sized(2000)  # Regions are in DBU.
r3 = r2 - r1

c.add_polygon(r3, layer=(2, 0))  # Add the region to the component.
c.plot()


#%%
c = gf.Component() # Creates a new blank component.
p1 = [(-8, -6), (6, 8), (7, 17), (9, 5)] # This adds a list of coordinates (p1) and adds it to the component c on the layer (1, 0).
s1 = c.add_polygon(p1, layer=(1, 0)) 
r1 = gf.Region(s1.polygon) # To manipulate the shape, the polygon is converted into a region object (r1).
r2 = r1.sized(2000)  # In DBU, 1 DBU = 1 nm, size it by 2000 nm = 2um.
r3 = r2 - r1 # We then take the larger region (r2) and subtract the smaller region (r)1 from it. The result is a new region (r3).
c.add_polygon(r3, layer=(2, 0)) # The newly created r3 is then added to the component c, but on the layer (2, 0) this time.
c.plot() # This command generates a plot of the component, allowing you to see the final result.

#%%
c = gf.Component()
p1 = [(-8, -6), (6, 8), (7, 17), (9, 5)]
s1 = c.add_polygon(p1, layer=(1, 0))
r1 = gf.Region(s1.polygon)
r2 = r1.sized(2000)  # In DBU, 1 DBU = 1 nm, size it by 2000 nm = 2um.
r3 = r2 - r1

c2 = gf.Component() # This portion creates an empty component in which r3 gets added into, this happens on the layer (2, 0) and then gets plotted.
c2.add_polygon(r3, layer=(2, 0))
c2.plot()





























