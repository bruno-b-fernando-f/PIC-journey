# -*- coding: utf-8 -*-
"""
Created on Mon Feb 23 19:13:34 2026

@author: babreu
"""
import numpy as np
import gdsfactory as gf
from gdsfactory.gpdk import PDK

PDK.activate()


import gdsfactory as gf
from gdsfactory.gpdk import PDK
import photonic_components as pc

PDK.activate()

g = pc.constant_pitch_and_filling_factor_grating(
    radius=25.0,
    waveguide_width=1,
    y_span=15.0,
    m=1.15,
    L_extra=10.0,
    n_periods=20,
    pitch=0.65,
    duty_cycle=0.5,
    layer=(1, 0),
    input_wg_length=2.0)


horizontal_distance = 150
vertical_pitch = 250

lengths = [400,800,1600,3200]
radius_curvature = 5
cross_section=gf.cross_section.strip(width=1, layer=(1, 0))
number_of_corners = 24
buffer_length = 0








array_component = gf.Component()

for i in range(len(lengths)):
    

    
    c = gf.Component()
    
    g1 = c << g
    g2 = c << g
    g1.rotate(180)
    g2.movex(horizontal_distance)

    route = pc.connect_two_ports_with_certain_length(
        component=c,
        port1=g1.ports["o1"],
        port2=g2.ports["o1"],
        length=lengths[i],
        radius_curvature=radius_curvature,
        cross_section=cross_section,
        number_of_corners = number_of_corners,
        buffer_length = buffer_length 
    )
    
    array_component << c
    c.movey(-vertical_pitch*i)
    


array_component.plot()

#%%
lengths = 400
number_of_corners = [4, 8, 12, 16]

array_component2 = gf.Component()



for i in range(len(number_of_corners)):
    

    
    c = gf.Component()
    
    g1 = c << g
    g2 = c << g
    g1.rotate(180)
    g2.movex(horizontal_distance)

    route = pc.connect_two_ports_with_certain_length(
        component=c,
        port1=g1.ports["o1"],
        port2=g2.ports["o1"],
        length=lengths,
        radius_curvature=radius_curvature,
        cross_section=cross_section,
        number_of_corners = number_of_corners[i],
        buffer_length = buffer_length 
    )
    
    array_component2 << c
    c.movey(-vertical_pitch*i)
    


array_component2.plot()


#%%
top = gf.Component()

array_ref = top << gf.components.array(array_component, columns = 3, rows = 1, column_pitch = 300)
array_ref2 = top << gf.components.array(array_component2, columns = 3, rows = 1, column_pitch = 300)
array_ref2.movey(-1250)

top.plot()
#%%

# write GDS
top.write_gds("top.gds")    
    
    
    
    
    
    
    
    
    
    
    