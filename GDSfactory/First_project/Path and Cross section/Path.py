# -*- coding: utf-8 -*-
"""
Created on Mon Feb 23 18:06:11 2026

@author: babreu
"""


import matplotlib.pyplot as plt
import numpy as np

import gdsfactory as gf

gf.gpdk.PDK.activate()


p1 = gf.path.straight(length=5)

# This creates a curved path segment using an Euler bend profile,
# which is a curve with a continuously changing radius designed to minimize light loss. This specific bend turns by 45 degrees.
# By setting use_eff=False, you are telling the function to ignore complex calculations and instead create a simpler bend with a constant, user-specified radius.
p2 = gf.path.euler(radius=5, angle=45, p=0.5, use_eff=False)

# The + operator is used to concatenate the two paths.
# It takes the second path (p2) and appends it to the end of the first path (p1), ensuring a smooth, continuous transition.
p = p1 + p2
f = p.plot()

#%%
p1 = gf.path.straight(length=5)
p2 = gf.path.euler(radius=5, angle=45, p=0.5, use_eff=False)
p = p2 + p1
f = p.plot()

#%%
# Note: -angle rotations correspond to a clockwise turn.
P = gf.Path()
P += gf.path.arc(radius=10, angle=90)  # Circular arc.
P += gf.path.straight(length=10)  # Straight section.
P += gf.path.euler(radius=3, angle=-90, use_eff = False)  # Euler bend (aka "racetrack" curve).
P += gf.path.straight(length=40)
P += gf.path.arc(radius=8, angle=-45)
P += gf.path.straight(length=10)
P += gf.path.arc(radius=8, angle=45)
P += gf.path.straight(length=10)

f = P.plot()

p2 = P.copy().rotate(45)
f = p2.plot()


P3= gf.Path()
P3.points = P.points - 2*p2.points

P3.plot()


#%%
# Extrude the Path and the cross-section.
# The extrude function converts a 1D path into a 2D shape by giving it a specified width.

c = gf.path.extrude(P, layer=(1, 0), width=1.5)
c.plot()


#%%

p = gf.path.straight()

# The code first defines three gf.Section objects, each representing a part of the total cross-section.
# s0: The central core section. It is 1 µm wide, centered at an offset of 0, and is on layer (1, 0).
# s1: A side section. It is 2 µm wide, its center is offset by +2 µm from the main centerline, and it is on layer (2, 0).
# s2: Another side section, identical to s1 but offset by -2 µm.
s0 = gf.Section(width=1, offset=0, layer=(1, 0), port_names=("in", "out"))
s1 = gf.Section(width=2, offset=2, layer=(2, 0))
s2 = gf.Section(width=2, offset=-2, layer=(2, 0))
x = gf.CrossSection(sections=(s0, s1, s2))

c = gf.path.extrude(p, cross_section=x)
c.draw_ports()
c.plot()


#%%

from gdsfactory.cross_section import ComponentAlongPath

# Create the path.
p = gf.path.straight()
p += gf.path.arc(10)
p += gf.path.straight()

# Define a cross-section containing a via.
via = ComponentAlongPath(
    component=gf.c.rectangle(size=(1, 1), centered=True), spacing=5, padding=2
)
s = gf.Section(width=0.5, offset=0, layer=(1, 0), port_names=("in", "out"))
x = gf.CrossSection(sections=(s,), components_along_path=(via,))

# Combine the path with the cross-section.
c = gf.path.extrude(p, cross_section=x)
c.plot()

#%%
points = np.array([(20, 10), (40, 10), (20, 40), (50, 40), (50, 20), (70, 20)])
plt.plot(points[:, 0], points[:, 1], ".-")

# This functionensures that one unit on the x-axis is the same length as one unit on the y-axis.
# This is crucial for plots where the geometric shape is important.
plt.axis("equal")

P = gf.path.smooth(
    points=points,
    radius=2,
    bend=gf.path.euler,  # Alternatively, use pp.arc, which will create a constant-radius bend.
    use_eff=False,
)
f = P.plot()

c = gf.path.extrude(P, layer=(1, 0), width=1.5)
c.plot()

#%%

straight_points = 100

P = gf.Path()
P.append(
    [
        gf.path.straight(
            length=10, npoints=straight_points
        ),  # Should have a curvature of 0
        gf.path.euler(
            radius=3, angle=90, p=0.5, use_eff=False
        ),  # Euler straight-to-bend transition with min. bend radius of 3 (max curvature of 1/3)
        gf.path.straight(
            length=10, npoints=straight_points
        ),  # Should have a curvature of 0
        gf.path.euler(radius=10, angle=90),  # Should have a curvature of 1/10
        gf.path.euler(radius=5, angle=-90),  # Should have a curvature of -1/5
        gf.path.straight(
            length=2, npoints=straight_points
        ),  # Should have a curvature of 0
    ]
)

f = P.plot()

# The .curvature() method of the Path object P is called.
# It returns two arrays: s, which contains the cumulative distance (arc length) at each point along the path,
# and K, which contains the corresponding curvature at that point. (Curvature is the reciprocal of the bend radius).
s, K = P.curvature()

# This plots the arc length s on the x-axis and the curvature K on the y-axis.
# The ".-" format string specifies that the plot should be a line with a dot marker at each data point.
plt.figure()
plt.plot(s, K, ".-")
plt.xlabel("Position along curve (arc length)")
plt.ylabel("Curvature")




































