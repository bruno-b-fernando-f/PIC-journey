# -*- coding: utf-8 -*-
"""
Created on Tue Dec  2 08:55:39 2025

@author: babreu


based on scripts by gcharalampous https://github.com/gcharalampous/lumerical-py-scripts
"""



"""
User-inputs are required.

In this file, the user is must enter the parameters required to sweep. 

The waveguide parameters to sweep are 'wg_thickness' and 'wg_width' .



               ^                                                                         
               |                                                                         
               |                                                                         
               |                    -                                                    
            wg_width                                                                     
        <--------------->                                                                
       +-------|--------+ ^                                                              
       |       |        | |                                                              
       |   waveguide    | | wg_thickness                                                 
       |       |        | |                                                              
   ------------|----------v--------------------->                                        
          (0,0)|                                                                         
               |                                                                         
               |                                                                         
               |                                                                         

"""




wg_width_start = 0.10e-6            # Choose the start waveguide width 'wg_width_start' 
#you want to start sweeping
wg_width_stop = 1.10e-6             # Choose the stop waveguide width 'wg_width_stop' you 
#want to finish sweeping
wg_width_step = 0.10e-6             # Choose the step of each sweep 'wg_width_step'




wg_height_start = 0.05e-6           # Choose the start waveguide height 'wg_height_start' 
#you want to start sweeping
wg_height_stop = 0.55e-6            # Choose the stop waveguide height 'wg_height_stop' you 
#want to finish sweeping
wg_height_step = 0.05e-6            # Choose the step of each sweep 'wg_height_step'




