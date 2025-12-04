# -*- coding: utf-8 -*-
"""
Created on Tue Dec  2 08:55:39 2025

@author: babreu


based on scripts by gcharalampous https://github.com/gcharalampous/lumerical-py-scripts
"""


#----------------------------------------------------------------------------
# Imports from user input files
# ---------------------------------------------------------------------------

import numpy as np
import lumapi, os
import shapely.geometry as sg
import shapely.ops as so
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, Normalize
from config import *



from build_simulation.coupling_waveguide_geometry import waveguide_draw
from build_simulation.fde_region import add_fde_region  
from user_inputs.input_simulation_parameters import *

#%%
# ------------------------- No inputs are required ---------------------------

mode = lumapi.MODE() 
waveguide_draw(mode)
add_fde_region(mode)

#%%

def modeProfiles():

    # Initialize empty lists to store mode properties
    neff = []           # effective index
    ng = []             # group index
    polariz_frac = []   # polarization fraction
    polariz_mode = []   # polarization mode (TE or TM)
    loss = []           # Waveguide Propagation Loss
    # Loop over each mode and extract its properties
    for m in range(1,num_modes+1):
        # Extract effective index and polarization fraction
        neff.append(mode.getdata("FDE::data::mode"+str(m),"neff"))
        ng.append(mode.getdata("FDE::data::mode"+str(m),"ng"))
        polariz_frac.append(mode.getdata("FDE::data::mode"+str(m),"TE polarization fraction"))
        loss.append((mode.getdata("FDE::data::mode"+str(m),"loss")))

        # Determine if mode is TE-like or TM-like based on polarization fraction
        if ( polariz_frac[m-1] > 0.5 ):
            polariz_mode.append("TE")
        else:
            polariz_mode.append("TM")

        # Extract electric and magnetic fields and plot the electric field
        plt.figure(m-1, figsize=(512/my_dpi, 256/my_dpi), dpi=my_dpi)
        x  = np.squeeze(mode.getdata("FDE::data::mode"+str(m),"x")); 
        y= np.squeeze(mode.getdata("FDE::data::mode"+str(m),"y"));
        E1 = np.squeeze(mode.getelectric("FDE::data::mode"+str(m)))
        H1 = np.squeeze(mode.getmagnetic("FDE::data::mode"+str(m)))
        if colormesh_plot_log:
            plt.pcolormesh(x*1e6,y*1e6,np.transpose(E1),shading = 'gouraud',cmap = 'jet', norm=LogNorm(vmin=1e-3, vmax=1))
        else:
            plt.pcolormesh(x*1e6,y*1e6,np.transpose(E1),shading = 'gouraud',cmap = 'jet', norm=Normalize(vmin=0, vmax=1))
        # Add a colorbar to the plot
        cbar = plt.colorbar()
        cbar.set_label('Intensity')


        plt.xlabel("x (\u00B5m)")
        plt.ylabel("y (\u00B5m)")
        plt.axis('scaled')
        plt.title("Mode-"+str(m) + "(E-field): " + polariz_mode[m-1] + ", neff=" + str(np.round(neff[m-1],4)))


        # Add the waveguide
        wg1_xmin = mode.getnamed("waveguide_1","x min")
        wg1_xmax = mode.getnamed("waveguide_1","x max")
        
        wg2_xmin = mode.getnamed("waveguide_1","x min")
        wg2_xmax = mode.getnamed("waveguide_1","x max")

        r1 = sg.box(wg1_xmin*1e6,0,wg1_xmax*1e6,wg_thickness*1e6)
        
        r2 = sg.box(wg2_xmin*1e6,0,wg2_xmax*1e6,wg_thickness*1e6)

    









        # Save the figure files as .png
        plt.tight_layout()
        file_name_plot = os.path.join(str(MODE_WAVEGUIDE_DIRECTORY_WRITE), "mode_profile_"+str(m)+".png")
        plt.savefig(file_name_plot)

        
    return neff, ng, polariz_frac, polariz_mode, loss




if(__name__=="__main__"):
    with lumapi.MODE(hide = True) as mode:
        
        # Disable Rendering
        mode.redrawoff()

        # Draw the waveguide structure using a custom function
        waveguide_draw(mode)

        # Add a finite-difference eigenmode (FDE) region to the simulation environment
        add_fde_region(mode)

        # Run the simulation, create a mesh, and compute the modes, then save
        mode.run()
        mode.findmodes()
        #mode.save(MODE_WAVEGUIDE_DIRECTORY_WRITE_FILE + "\\waveguide_modes.lms")
        
        #input("\nPress Enter to exit...")
        
        # Turn redraw back on and close LumAPI connection
        mode.redrawon()  

        # Mode Profiles
        # Initialize empty lists to store mode properties
        neff = []           # effective index
        ng = []             # group index
        polariz_frac = []   # polarization fraction
        polariz_mode = []   # polarization mode (TE or TM)

        neff, ng, polariz_frac, polariz_mode, loss = modeProfiles()
        
        