
#Created on Sun Feb 24 11:43:44 201
#Initial var definition and libraries needed for all functions
#before writing any functions, must copy all var definition here 

import RPi.GPIO as GPIO
from time import sleep

#programming the GPIO by Board numbers
GPIO.setmode(GPIO.BOARD) 
GPIO.setwarnings(False) #do not show any warnings
 
#define inputs and outputs 

#Stepper motor outputs
dir_x = 5
pul_x = 7
dir_y = 35
pul_y = 37

#define stepper motor directions
CW = 1
CCW = 0

#Limit switch pins
lim_x_pos = 32
lim_x_neg = 36
lim_y_pos = 38
lim_y_neg = 40 

#pendant pins 
save_pos_pin = 29
zero_reset_pin = 31
speed_rotpot = 10
up_but = 15
down_but = 19
right_but = 21
left_but = 23 

#enable pin as either output or input
GPIO.setup(dir_x,GPIO.OUT)
GPIO.setup(pul_x,GPIO.OUT)
GPIO.setup(dir_y,GPIO.OUT)
GPIO.setup(pul_y,GPIO.OUT)

GPIO.setup(lim_x_pos,GPIO.IN)
GPIO.setup(lim_x_neg,GPIO.IN)
GPIO.setup(lim_y_pos,GPIO.IN)
GPIO.setup(lim_y_neg,GPIO.IN)

GPIO.setup(save_pos_pin,GPIO.IN)
GPIO.setup(zero_reset_pin,GPIO.IN)
GPIO.setup(up_but,GPIO.IN)
GPIO.setup(down_but,GPIO.IN)
GPIO.setup(right_but,GPIO.IN)
GPIO.setup(left_but,GPIO.IN)

#read values from input 
up = GPIO.input(up_but)
down = GPIO.input(down_but)
right = GPIO.input(right_but)
left = GPIO.input(left_but)

save_position = GPIO.input(save_pos_pin)
zero_reset = GPIO.input(zero_reset_pin)








