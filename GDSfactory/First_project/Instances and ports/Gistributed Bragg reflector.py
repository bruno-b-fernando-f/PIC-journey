# -*- coding: utf-8 -*-
"""
Created on Mon Feb 23 17:57:16 2026

@author: babreu
"""
import gdsfactory as gf


@gf.cell
def dbr_period(w1=0.5, w2=0.6, l1=0.2, l2=0.4, straight=gf.components.straight):
    """Return one DBR period."""
    c = gf.Component()
    r1 = c << straight(length=l1, width=w1)
    r2 = c << straight(length=l2, width=w2)

    # The second waveguide (r2) is automatically moved to connect its input port (o1) to the output port of the first waveguide (r1.ports["o2"]).
    # The allow_width_mismatch=True is necessary because the two waveguides have different widths.
    r2.connect(port="o1", other=r1.ports["o2"], allow_width_mismatch=True)
    
    # The unconnected input of the first section and the unconnected output of the second section are "exported".
    # These will become the ports of the main dbr_period component.
    c.add_port("o1", port=r1.ports["o1"])
    c.add_port("o2", port=r2.ports["o2"])
    return c


l1 = 0.2
l2 = 0.4
n = 30
period = dbr_period(l1=l1, l2=l2)
period

#%%
# period: The component to be repeated.
# columns=n: Creates n copies in the horizontal direction (since n was set to 3, it creates 3 copies).
# rows=1: Creates a single row.
# column_pitch=l1 + l2: This sets the horizontal distance between the start of each repeated period. 
# By setting it to the total length of one period (l1 + l2), the copies are placed perfectly end-to-end, creating a continuous structure.

dbr = gf.Component()
dbr.add_ref(period, columns=n, rows=1, column_pitch=l1 + l2)
dbr


#%%
p1 = dbr.add_port("o1", port=period.ports["o1"]) 
p2 = dbr.add_port("o2", port=period.ports["o2"])
p2.dcenter = ((l1+l2)*n,0)
dbr.draw_ports()
dbr














