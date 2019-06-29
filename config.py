# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 19:37:37 2019

@author: Zoe
"""

# List of global variables used between gui and motor control codes

# Global location variables
y_loc_abs = 0
x_loc_abs = 0
y_loc = 0
x_loc = 0

#-----------------------------------------------------------------------------
# VARIABLES TO CHANGE FOR CALIBRATION

# max x and y locations (mm)
max_x = 133
max_y = 87

# Set a nominal speed (delay in secs)
nom_speed_x = 0.0005
nom_speed_y = 0.0005
nom_accel = 0.0005 # is max instantaneous change in speed

# Define zeros
zero_x = 0
zero_y = 0

# Define speed/delay and rotpot values
volt_max = 65474
volt_min = 200
delay_max = 0.001
delay_min_x = 0.0004
delay_min_y = 0.0004

# define stepper motor directions
UP = 1
DOWN = 0
RIGHT = 0
LEFT = 1

# steps per mm (steps per rotation = 400, rotation = 1.27 mm/rot)
steps_per_mm = 315
mm_per_step = round(1/steps_per_mm, 4)

# flag to stop eveything
stopflag = 0
stop_lim_thread = 0
#-----------------------------------------------------------------------------
