# -*- coding: utf-8 -*-
"""
Created on Wed Feb 25 15:40:00 2026

@author: babreu
"""


import numpy as np
import gdsfactory as gf




def _sector_annulus_polygon(
    r_inner: float,
    r_outer: float,
    theta_start_deg: float,
    theta_stop_deg: float,
    npts: int = 512,
):
    th0 = np.deg2rad(theta_start_deg)
    th1 = np.deg2rad(theta_stop_deg)

    th_outer = np.linspace(th0, th1, npts)
    th_inner = np.linspace(th1, th0, npts)

    outer = np.column_stack([r_outer * np.cos(th_outer), r_outer * np.sin(th_outer)])
    inner = np.column_stack([r_inner * np.cos(th_inner), r_inner * np.sin(th_inner)])

    pts = np.vstack([outer, inner]).tolist()
    return pts


def _lumerical_taper_polygon_localx(
    Ltaper: float,
    w1_half: float,
    w2_half: float,
    m: float,
    npts: int = 2000,
):
    x0 = Ltaper / 2.0
    a = w2_half
    alpha = (w1_half - w2_half) / (Ltaper**m)

    x_local = np.linspace(-Ltaper / 2.0, Ltaper / 2.0, npts)
    y = alpha * (x0 - x_local) ** m + a

    top = np.column_stack([x_local, y])
    bot = np.column_stack([x_local[::-1], -y[::-1]])
    pts_local = np.vstack([top, bot])

    return pts_local


@gf.cell
def constant_pitch_and_filling_factor_grating(
    radius: float = 12.0,
    waveguide_width: float = 0.5,  # um
    y_span: float = 2.0,  # um
    m: float = 1.15,
    L_extra: float = 2.0,  # um
    n_periods: int = 10,
    pitch: float = 0.65,  # um
    duty_cycle: float = 0.25,  # fraction of pitch that is "tooth" (not etched)
    layer = (1, 0),
    npts_taper: int = 2000,
    npts_sector: int = 512,
    input_wg_length: float = 2.0,  # um
):
    c = gf.Component()

    theta = np.degrees(np.arcsin((y_span / 2) / radius))
    etch_width = pitch * (1 - duty_cycle)
    L = n_periods * pitch + etch_width

    # ---- taper section (polygon in [0, Ltaper]) ----
    Ltaper = radius * np.cos(np.deg2rad(theta))
    w1_half = waveguide_width / 2.0
    w2_half = y_span / 2.0

    pts_local = _lumerical_taper_polygon_localx(
        Ltaper=Ltaper,
        w1_half=w1_half,
        w2_half=w2_half,
        m=m,
        npts=npts_taper,
    )

    pts_global = pts_local.copy()
    pts_global[:, 0] += Ltaper / 2.0
    c.add_polygon(pts_global.tolist(), layer=layer)

    # ---- input straight waveguide (rectangle in [-L_in, 0]) ----
    if input_wg_length and input_wg_length > 0:
        x0 = -float(input_wg_length)
        x1 = 0.0
        wg = [
            [x0, -w1_half],
            [x1, -w1_half],
            [x1, +w1_half],
            [x0, +w1_half],
        ]
        c.add_polygon(wg, layer=layer)

    # ---- ports ----
    c.add_port(
        name="o1",
        center=(-float(input_wg_length), 0.0),
        width=2 * w1_half,
        orientation=180,
        layer=layer,
    )

    # ---- input section (ring sector) ----
    r_inner_in = radius * np.cos(np.deg2rad(theta))
    r_outer_in = radius
    pts_in = _sector_annulus_polygon(
        r_inner=r_inner_in,
        r_outer=r_outer_in,
        theta_start_deg=-theta,
        theta_stop_deg=theta,
        npts=npts_sector,
    )
    c.add_polygon(pts_in, layer=layer)

    # ---- output section (ring sector shifted radii) ----
    r_inner_out = radius + L
    r_outer_out = radius + L + L_extra
    pts_out = _sector_annulus_polygon(
        r_inner=r_inner_out,
        r_outer=r_outer_out,
        theta_start_deg=-theta,
        theta_stop_deg=theta,
        npts=npts_sector,
    )
    c.add_polygon(pts_out, layer=layer)

    # ---- grating (etched ring sectors) ----
    for i in range(1, n_periods + 1):
        r_in = radius + pitch * (i - 1) + etch_width
        r_out = radius + pitch * i
        pts_g = _sector_annulus_polygon(
            r_inner=r_in,
            r_outer=r_out,
            theta_start_deg=-theta,
            theta_stop_deg=theta,
            npts=npts_sector,
        )
        c.add_polygon(pts_g, layer=layer)

    return c




def connect_two_ports_with_certain_length(
    component: gf.Component,
    port1,
    port2,
    length: float = 200.0,
    buffer_length: float = 5.0,
    radius_curvature: float = 5.0,
    cross_section=None,
    number_of_corners = 8,
):
    p1 = component.ports[port1] if isinstance(port1, str) else port1
    p2 = component.ports[port2] if isinstance(port2, str) else port2

    if cross_section is None:
        cross_section = gf.cross_section.strip(width=p1.width, layer=p1.layer)

    x1, y1 = p1.center
    x2, y2 = p2.center

    R = float(radius_curvature)

    distance_between_ports = abs(x2 - x1)

    dx = (float(length) - distance_between_ports - 6.0 * R) / (number_of_corners/2)
    if dx < -1e-9:
        raise ValueError(
            "Target length is too short for the given port spacing and radius_curvature."
        )

    sgn = 1.0 if (x2 - x1) >= 0 else -1.0

    
    waypoints = []
    for i in range(int(number_of_corners/4)):
        waypoints.append((x1 + sgn * (2 * R), y1 + 0.0))
        waypoints.append((x1 + sgn * (2 * R), y1 - 2 * R - dx)),
        waypoints.append((x1 + sgn * (4 * R)+buffer_length, y1 - 2 * R - dx)),
        waypoints.append((x1 + sgn * (4 * R)+buffer_length, y1 + 0.0))
        x1 += sgn * (4 * R) + 2*buffer_length
        
        
    route = gf.routing.route_single(
        component=component,
        port1=p1,
        port2=p2,
        waypoints=waypoints,
        cross_section=cross_section,
        radius=R,
    )
    
    length_route = route.length

    diff = length-length_route/1e3
    dx = dx + diff / (number_of_corners/2)

    for inst in route.instances:
        inst.delete()    

    x1 = p1.center[0]
    waypoints = []
    for i in range(int(number_of_corners/4)):
        waypoints.append((x1 + sgn * (2 * R), y1 + 0.0))
        waypoints.append((x1 + sgn * (2 * R), y1 - 2 * R - dx)),
        waypoints.append((x1 + sgn * (4 * R)+buffer_length, y1 - 2 * R - dx)),
        waypoints.append((x1 + sgn * (4 * R)+buffer_length, y1 + 0.0))
        x1 += sgn * (4 * R) + 2*buffer_length
        
    
    route = gf.routing.route_single(
        component=component,
        port1=p1,
        port2=p2,
        waypoints=waypoints,
        cross_section=cross_section,
        radius=R,
    )
    
    return route

















































