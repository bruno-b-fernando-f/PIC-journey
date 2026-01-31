#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 31 10:23:02 2026

@author: brunomelo
"""


import numpy as np
import matplotlib.pyplot as plt

def gaussian_field_2d(X, Y, w0, x0=0.0, y0=0.0):
    return np.exp(-(((X - x0)**2 + (Y - y0)**2) / (w0**2)))

def overlap_L2(E1, E2, dx, dy):
    num = np.abs(np.sum(E1 * np.conj(E2)) * dx * dy)**2
    den = (np.sum(np.abs(E1)**2) * dx * dy) * (np.sum(np.abs(E2)**2) * dx * dy)
    return num / den

def make_grid(L, N):
    x = np.linspace(-L, L, N)
    y = np.linspace(-L, L, N)
    dx = x[1] - x[0]
    dy = y[1] - y[0]
    X, Y = np.meshgrid(x, y, indexing="xy")
    return x, y, X, Y, dx, dy

def one_db_tolerance_offset(w0, L_factor=6.0, N=801, offsets_factor_max=4.0, n_offsets=401):
    """
    Returns (x_1dB, offsets, overlaps) where x_1dB is the smallest x>=0
    such that overlap(x) <= 10^(-1/10) * overlap(0). Uses linear interpolation.
    """
    L = L_factor * w0
    x, y, X, Y, dx, dy = make_grid(L, N)

    E1 = gaussian_field_2d(X, Y, w0, x0=0.0, y0=0.0)

    offsets = np.linspace(0.0, offsets_factor_max * w0, n_offsets)
    overlaps = np.empty_like(offsets)

    for i, xoff in enumerate(offsets):
        E2 = gaussian_field_2d(X, Y, w0, x0=xoff, y0=0.0)
        overlaps[i] = overlap_L2(E1, E2, dx, dy)

    peak = overlaps[0]
    thresh = peak * (10 ** (-1.0 / 10.0))

    idx = np.where(overlaps <= thresh)[0]
    if len(idx) == 0:
        return np.nan, offsets, overlaps

    k = idx[0]
    if k == 0:
        return offsets[0], offsets, overlaps

    x0, y0_ = offsets[k - 1], overlaps[k - 1]
    x1, y1_ = offsets[k], overlaps[k]

    # linear interpolation for overlap(x)=thresh
    if y1_ == y0_:
        x_1db = x1
    else:
        x_1db = x0 + (thresh - y0_) * (x1 - x0) / (y1_ - y0_)

    return x_1db, offsets, overlaps

plt.close('all')

if __name__ == "__main__":
    # ===== Part 1: 2x2 panel (fields + product + overlap vs offset) =====
    w0 = 1.0  # um
    L_factor = 6.0
    N = 801

    L = L_factor * w0
    x, y, X, Y, dx, dy = make_grid(L, N)

    E1 = gaussian_field_2d(X, Y, w0, x0=0.0, y0=0.0)

    x_offset = 1.5 * w0
    E2 = gaussian_field_2d(X, Y, w0, x0=x_offset, y0=0.0)

    product = E1 * np.conj(E2)
    eta = overlap_L2(E1, E2, dx, dy)
    print("Overlap @ offset =", x_offset, "um:", eta)

    offsets = np.linspace(0.0, 4.0 * w0, 201)
    overlaps = np.empty_like(offsets)
    for i, xoff in enumerate(offsets):
        E2_tmp = gaussian_field_2d(X, Y, w0, x0=xoff, y0=0.0)
        overlaps[i] = overlap_L2(E1, E2_tmp, dx, dy)

    fig, axs = plt.subplots(2, 2, figsize=(10, 8))

    im0 = axs[0, 0].imshow(np.abs(E1)**2, extent=[-L, L, -L, L], origin="lower")
    axs[0, 0].set_title("Mode 1 |E1|^2")
    axs[0, 0].set_xlabel("x (um)")
    axs[0, 0].set_ylabel("y (um)")
    fig.colorbar(im0, ax=axs[0, 0])

    im1 = axs[0, 1].imshow(np.abs(E2)**2, extent=[-L, L, -L, L], origin="lower")
    axs[0, 1].set_title(f"Mode 2 |E2|^2 (offset = {x_offset:.3g} um)")
    axs[0, 1].set_xlabel("x (um)")
    axs[0, 1].set_ylabel("y (um)")
    fig.colorbar(im1, ax=axs[0, 1])

    im2 = axs[1, 0].imshow(np.real(product), extent=[-L, L, -L, L], origin="lower")
    axs[1, 0].set_title("Re(E1 · E2*)")
    axs[1, 0].set_xlabel("x (um)")
    axs[1, 0].set_ylabel("y (um)")
    fig.colorbar(im2, ax=axs[1, 0])

    axs[1, 1].plot(offsets, overlaps)
    axs[1, 1].set_title("Overlap vs x offset")
    axs[1, 1].set_xlabel("x offset (um)")
    axs[1, 1].set_ylabel("Overlap")
    axs[1, 1].grid(True)

    plt.tight_layout()

    # ===== Part 2: 1 dB tolerance vs mode field diameter (MFD = 2 w0) =====
    # Define the 1 dB point as overlap(x_1dB) = overlap(0) * 10^(-1/10)
    w0_list = np.linspace(0.5, 5.0, 31)  # um
    mfd_list = 2.0 * w0_list             # um
    tol_list = np.empty_like(w0_list)

    for i, w in enumerate(w0_list):
        x_1db, _, _ = one_db_tolerance_offset(
            w0=w,
            L_factor=L_factor,
            N=N,
            offsets_factor_max=4.0,
            n_offsets=401
        )
        tol_list[i] = x_1db  # um

    plt.figure(figsize=(7.5, 5.5))
    plt.plot(mfd_list, tol_list)
    plt.xlabel("Mode field diameter, MFD = 2w0 (um)")
    plt.ylabel("1 dB lateral tolerance (um)")
    plt.grid(True)
    plt.tight_layout()

    plt.show()
