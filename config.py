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
max_x = 135
max_y = 135

# Set a nominal speed (delay in secs)
nom_speed = 0.001
nom_accel = 0.001 # is max instantaneous change in speed

# Define zeros
zero_x = 0
zero_y = 0

# Define speed/delay and rotpot values
volt_max = 65472
volt_min = 2000
delay_max = 0.01
delay_min = 0.00005

# define stepper motor directions
UP = 1
DOWN = 0
RIGHT = 1
LEFT = 0

# steps per mm (steps per rotation = 400, rotation = 1.27)
steps_per_mm = int(400/1.27)
mm_per_step = 1/steps_per_mm

# flag to stop eveything
stopflag = 0
#-----------------------------------------------------------------------------
