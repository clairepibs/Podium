# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 13:46:56 2019
"""
import time
from lcdbackpack import LcdBackpack

# Set up port location - this should not change
lcdbackpack = LcdBackpack('/dev/ttyACM0', 115200)
#connect to the serial port 
lcdbackpack.connect()
#clear any characters
lcdbackpack.clear()

lcdbackpack.set_backlight_white()

def print_lcd():
    
# Initialize screen format
    lcdbackpack.set_cursor_home()
    lcdbackpack.write("X:")
    lcdbackpack.set_cursor_position(1,2)
    lcdbackpack.write("Y:")
    lcdbackpack.set_cursor_position(11,1)
    lcdbackpack.write(" |IND")
    lcdbackpack.set_cursor_position(11,2)
    lcdbackpack.write(" | 01")
    
    
def print_lcd_pos(x_pos,y_pos):
    
    lcdbackpack.set_cursor_position(3,1)
    lcdbackpack.write("{:+.3f}".format(x_pos))
    lcdbackpack.set_cursor_position(3,2)
    lcdbackpack.write("{:+.3f}".format(y_pos))
    
def print_lcd_ind(index):
    lcdbackpack.set_cursor_position(15,2)
    lcdbackpack.write("{:01d}".format(index))
