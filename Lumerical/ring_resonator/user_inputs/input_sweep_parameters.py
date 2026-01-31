# -*- coding: utf-8 -*-
"""
Created on Tue Dec  2 08:55:39 2025

@author: babreu


based on scripts by gcharalampous https://github.com/gcharalampous/lumerical-py-scripts
"""



"""

                                ^ y-axis               
                                |                      
                                |                      
                                |                      
                                |                      
                                |                      
                              z o ------------- >  x-axis

                    +----------------------------------------+                          
                    |               Cladding                 |                          
                    |                                        |                        
                    |        +------+    gap    +------+     |                          
                    |        |      | <-------> |      |     |                          
                    |        |rail  |   slot    |rail  |     |                          
                    |        |      |           |      |     |                          
                    +----------------------------------------+                          
                    |                  Box                   |                          
                    +----------------------------------------+                          
                    |                                        |                          
                    |               Substrate                |                          
                    |                                        |                          
                    +----------------------------------------+                          
                                                                               
                                                                       

"""




gap_width_start = 0.01e-6            # Choose the start waveguide width 'wg_width_start' 
#you want to start sweeping
gap_width_stop = 0.3e-6             # Choose the stop waveguide width 'wg_width_stop' you 
#want to finish sweeping
gap_width_step = 0.01e-6             # Choose the step of each sweep 'wg_width_step'




#wg_height_start = 0.05e-6           # Choose the start waveguide height 'wg_height_start' 
#you want to start sweeping
#wg_height_stop = 0.55e-6            # Choose the stop waveguide height 'wg_height_stop' you 
#want to finish sweeping
#wg_height_step = 0.05e-6            # Choose the step of each sweep 'wg_height_step'




