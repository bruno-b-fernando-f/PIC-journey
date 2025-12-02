# -*- coding: utf-8 -*-
"""
Created on Tue Dec  2 09:01:48 2025

@author: babreu

based on scripts by gcharalampous https://github.com/gcharalampous/lumerical-py-scripts
"""


"""
No user-inputs are required.

The purpose of this script is to take the parameters from the 'materials.py'
and 'simulation_parameters.py' and render the structure below

                                   
                                ^ y-axis               
                                |                      
                                |                      
                                |                      
                                |                      
                                |                      
                              z o ------------- >  x-axis

                    +--------------------------------+                          
                    |           Claddding            |                          
                    |                                |                        
                    |         +-----------+          |                          
                    |         |           |          |                          
                    |         | waveguide |          |                          
                    |         |           |          |                          
                    +--------------------------------+                          
                    |               Box              |                          
                    +--------------------------------+                          
                    |                                |                          
                    |           Substrate            |                          
                    |                                |                          
                    +--------------------------------+                          !
                                                                               
                                                                               

The 2D waveguide is rendered on the 'y' and 'x' axis while the 'z' axis 
remains the propagation. The z-axis is not used during mode simulations.


"""

import lumapi

from user_inputs.input_simulation_parameters import *
from user_inputs.input_materials import *
from config import*


#%%
save_file = "\\simple_waveguide_geometry.lms"
 


#%%

def waveguide_draw(mode):
    

    
    # Adds the four rectangulars shown above

    mode.addrect(name = "waveguide")
    mode.addrect(name = "cladding")
    mode.addrect(name = "box")
    mode.addrect(name = "substrate")

    if(slab_thickness>0):
      slab_enable  = 1
    else:
      slab_enable = 0 



    # Set the parameters of each structure from the user file

    configuration = (
    
         

    ("cladding",  (("x", 0.),
                   ("y", 0.),
                   ("x span", simulation_span_x + 2e-6),
                   ("y min", clad_min_y),
                   ("y max", clad_max_y),
                   ("z span", 5e-6),
                   ("material",clad_material),
                   ("override mesh order from material database",1),
                   ("mesh order",3))),
    
    ("box",       (("x", 0.),
                   ("z", 0.),
                   ("x span", simulation_span_x + 2e-6),
                   ("y min", clad_min_y- box_thickness),
                   ("y max", clad_min_y),
                   ("z span", 5e-6),
                   ("material",box_material),
                   ("override mesh order from material database",1),
                   ("mesh order",3))),
    
    
     ("substrate",(("x", 0.),
                   ("z", 0.),
                   ("x span", simulation_span_x + 2e-6),
                   ("y min", clad_min_y - box_thickness - sub_thickness),
                   ("y max", clad_min_y - box_thickness),
                   ("z span", 5e-6),
                   ("material",sub_material),
                   ("override mesh order from material database",1),
                   ("mesh order",3))),   
     
     ("waveguide", (("x", 0.),
                    ("y min", 0),
                    ("z", 0.),
                    ("x span", wg_width),
                    ("y max", wg_thickness),
                    ("z span", 5e-6),
                    ("material",wg_material),
                    ("override mesh order from material database",1),
                    ("mesh order",2))),
     

     
        
    )





    # Populate the 2D waveguide structure
    
    for obj, parameters in configuration:
           for k, v in parameters:
               mode.setnamed(obj, k, v)    




#%% Useful to test geometry



if(__name__=="__main__"):
    with lumapi.MODE(hide=True) as mode:
    
      # Disable Rendering
      mode.redrawoff()

      # Draw the waveguide structure using a custom function
      waveguide_draw(mode)

      # Turn redraw back on and close LumAPI connection
      mode.redrawon()        

      mode.save(MODE_WAVEGUIDE_DIRECTORY_WRITE_FILE + save_file)