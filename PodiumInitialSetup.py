
#Created on Sun Feb 24 11:43:44 201
#Initial var definition and libraries needed for all functions
#before writing any functions, must copy all var definition here 

import RPi.GPIO as GPIO
from time import sleep

import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

#programming the GPIO by Board numbers (see board pinout)
GPIO.setmode(GPIO.BCM) 
GPIO.setwarnings(False) #do not show any warnings

# INITIALIZE VARIABLES

# Stepper motor outputs
dir_x = 2
pul_x = 3
dir_y = 
pul_y = 

# define stepper motor directions
up = 1
down = 0
right = 1
left = 0

# Limit switch pins
lim_x_pos = 32
lim_x_neg = 36
lim_y_pos = 38
lim_y_neg = 40 

# Limit switch trigger flags
posXtrig = 1
posYtrig = 2
negXtrig = 3
negYtrig = 4

#pendant pins 
save_but = 29
zero_but = 31
up_but = 15
down_but = 19
right_but = 21
left_but = 23 

# Sequence of test points
sequence = []
index = 0

#enable pin as either output or input
GPIO.setup(dir_x,GPIO.OUT)
GPIO.setup(pul_x,GPIO.OUT)
GPIO.setup(dir_y,GPIO.OUT)
GPIO.setup(pul_y,GPIO.OUT)

# Set GPIO switch input pins for internal resistance
GPIO.setup(up_but, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(down_but, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(right_but, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(left_but, GPIO.IN, pull_up_down = GPIO.PUD_UP)

GPIO.setup(save_pos_pin,GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(zero_reset_pin,GPIO.IN, pull_up_down = GPIO.PUD_UP)

GPIO.setup(lim_x_pos,GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(lim_x_neg,GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(lim_y_pos,GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(lim_y_neg,GPIO.IN, pull_up_down = GPIO.PUD_UP)

# Setup for potentiometer reading

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D22)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan = AnalogIn(mcp, MCP.P0)

#-----------------------------------------------------------------------------
# VARIABLES TO CHANGE FOR CALIBRATION

# max x and y locations (mm)
max_x = 200
max_y = 200

# Set a nominal speed (delay in secs)
nom_speed = 0.0001
nom_accel = 0

#-----------------------------------------------------------------------------

# LIST OF GLOBAL VARIABLES THAT ARE CHANGED
# x_loc
# y_loc
# x_loc_abs
# y_loc_abs
# zero_x
# zero_y
# index of list
