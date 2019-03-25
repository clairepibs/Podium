# This is a test library for motor control by pendant using OOP
# Created on 2019-03-17 by Zoe LeHong

# LIST OF GLOBAL VARIABLES THAT ARE TRACKED WITHIN PROGRAM
# x_loc = x_loc_abs-zero_x
# y_loc
# x_loc_abs
# y_loc_abs
# zero_x
# zero_y
# index of list

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------

##-----------------------------------------------------------------------------
## VARIABLES TO CHANGE FOR CALIBRATION
#
## max x and y locations (mm)
#max_x = 200
#max_y = 200
#
## steps per mm (steps per rotation = 400, rotation = 1.27)
#steps_per_mm = int(400/1.27)
#mm_per_step = 1/c.steps_per_mm
#
## Set a nominal speed (delay in secs)
#nom_speed = 0.001
#nom_accel = 0.001 # is max instantaneous change in speed
#
## Define speed/delay and rotpot values
#volt_max = 65472
#volt_min = 2000
#delay_max = 0.01
#delay_min = 0.0001
#
## define stepper motor directions
#up = 1
#down = 0
#right = 1
#left = 0
#
## Define zeros
#zero_x = 0
#zero_y = 0
##-----------------------------------------------------------------------------

# IMPORT AND INITIALIZE

import RPi.GPIO as GPIO
from time import sleep
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from lcdbackpack import LcdBackpack
import config as c

# INITIALIZE VARIABLES

# Limit switch trigger flags
posXtrig = 1
posYtrig = 2
negXtrig = 3
negYtrig = 4

# Other flags
stop_threads = 0

# Stepper motor outputs
dir_x = 2
pul_x = 3
dir_y = 4
pul_y = 5

# Limit switch pins
lim_x_pos = 32
lim_x_neg = 36
lim_y_pos = 38
lim_y_neg = 40 

#pendant pins 
save_but = 29
zero_but = 31
up_but = 15
down_but = 19
right_but = 21
left_but = 23 

# INITIALIZE GPIO PINS

#programming the GPIO by Board numbers (see board pinout)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

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

# SETUP FOR POTENTIOMETER READING
# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D22)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan = AnalogIn(mcp, MCP.P0)

#-----------------------------------------------------------------------------
# FUNCTIONS USED IN MOTOR CONTROL
#-----------------------------------------------------------------------------
def startup_lcd():
    '''
    Initializes LCD, prints constant visuals
    
    INPUTS:     None
    OUTPUTS:    None
    '''
    
    
    print('LCD initialized')
    # Set up port location - this should not change
    lcdbackpack = LcdBackpack('/dev/ttyACM0', 115200)
    #connect to the serial port 
    lcdbackpack.connect()
    #clear any characters
    lcdbackpack.clear()
    # Set background colour
    lcdbackpack.set_backlight_white()
    
    # Initialize screen format
    lcdbackpack.set_cursor_home()
    lcdbackpack.write("X:")
    lcdbackpack.set_cursor_position(1,2)
    lcdbackpack.write("Y:")
    lcdbackpack.set_cursor_position(11,1)
    lcdbackpack.write(" |IND")
    lcdbackpack.set_cursor_position(11,2)
    lcdbackpack.write(" | 01")
    
#-----------------------------------------------------------------------------

def shutoff_lcd():
    pass
    
def stop_daemon():
    global stop_threads
    stop_threads = True
#-----------------------------------------------------------------------------
def print_pos_lcd():
    '''
    Prints location of motors every 0.5 seconds. Used as a daemon thread.
    
    INPUTS:     None
    OUTPUTS:    None
    '''
    #pass
    # Print new position on LCD and GUI
    global stop_threads
        
    while 1:
        print('X: {:0.3f}, Y: {:0.3f}' .format(c.x_loc, c.y_loc))
        
        # Print location on LCD
        lcdbackpack.set_cursor_position(3,1)
        lcdbackpack.write("{:+.3f}".format(x_loc))
        lcdbackpack.set_cursor_position(3,2)
        lcdbackpack.write("{:+.3f}".format(y_loc))
                
        sleep(1)
        
        if stop_threads:
            break
#-----------------------------------------------------------------------------

def print_lcd_ind(index):
    '''
    Prints new index only to LCD
    
    INPUTS:     None
    OUTPUTS:    None
    '''
    lcdbackpack.set_cursor_position(15,2)
    lcdbackpack.write("{:01d}".format(index))
    print('Index: ', index)

#-----------------------------------------------------------------------------
   
def pot_speed():
    '''
    This function converts reads voltage from 1ok potentiometer, and converts it to a delay time.
    NOTE: MUST HAVE SPI SETUP WITH MCP3008 LIBRARY FOR USE
    
    INPUTS:        none
    OUTPUTS:     delay (seconds)
    '''
    
    # Read pot
    volt = chan.value
    
    # Conversion
    volt_range = c.volt_max - c.volt_min
    delay_range = c.delay_max - c.delay_min
    delay = abs(volt*delay_range/volt_range-c.delay_max)
    
    print('Speed: ', delay)
    
    return delay
     
#-----------------------------------------------------------------------------
     
def check_lim():
    '''
    This function checks if limit switches have been hit.
    
    INPUTS:   None     
    OUTPUTS:  Returns limit switch flag or "false" if no switch has been hit   
    '''
    
    #print('Checking limits')
    if GPTO.input(lim_x_pos) == True:
        stop()
        left.move_mm()
        return posXtrig
    elif GPTO.input(lim_x_neg) == True:
        stop()
        right.move_mm()
        return posYtrig
    elif GPTO.input(lim_y_pos) == True:
        stop()
        down.move_mm()
        return negXtrig
    elif GPTO.input(lim_y_neg) == True:
        stop()
        up.move_mm()
        return negYtrig
    else:
        return False

# -----------------------------------------------------------------------------

def check_save():
    '''
    This function checks if save button has been pressed.

    INPUTS:   None
    OUTPUTS:  Returns save flag or "false" if save button has not been hit
    '''

    #print('Checking save button')
    #pass


    if GPTO.input(save_but) == True:
        return True
    else:
        return False

# -----------------------------------------------------------------------------

def check_zero():
    '''
    This function checks if zero button has been pressed.

    INPUTS:   None
    OUTPUTS:  Returns save flag or "false" if zero button has not been hit
    '''

    #print('Checking zero button')
    pass


    if GPTO.input(zero_but) == True:
        return True
    else:
        return False


#-----------------------------------------------------------------------------

def hard_stop():
    '''
    Stops motors immediately (no jarring control)
    
    INPUTS:     None
    OUTPUTS:    None
    '''
    
    GPIO.output(pul_x, LOW)
    GPIO.output(pul_y, LOW)
    print('Stopping motor')
    
#-----------------------------------------------------------------------------

def soft_stop(delay):
    '''
    Stops motors with acceleration control
    
    INPUTS:     None
    OUTPUTS:    None
    '''
    
    # Not sure about this one
    up.accel_control(delay, 0)
    down.accel_control(delay, 0)
    right.accel_control(delay, 0)
    left.accel_control(delay, 0)
    
    print('Stopping motor')
    
#-----------------------------------------------------------------------------

def cleanup():
    '''
    Moves motors to (0,0), set speed to nominal,
    reset reference ('zero point') to (0,0).
    INPUTS:    
    OUTPUTS:    
    '''
    
    print("Starting cleanup")
    
    # Send motors to neg limits
    down.go_lim()
    left.go_lim()
    
    # Set coordinates and zero to (0,0)
    c.x_loc_abs = 0
    c.y_loc_abs = 0
    c.x_loc = 0
    c.y_loc = 0
    c.zero_x = 0
    c.zero_y = 0
    
#-----------------------------------------------------------------------------

def set_zero_pend():
    '''
    Sets current location to zero, updates location trackers
    
    INPUTS:     
    OUTPUTS:    
    '''
    
    print('Setting new zero to current location')
    
    # Set new zero coordinates
    c.zero_x = c.x_loc_abs
    c.zero_y = c.y_loc_abs
    
    # Reset local coordinates
    c.x_loc = 0
    c.y_loc = 0
    
    print_pos_lcd()

#-----------------------------------------------------------------------------

# SET UP MOTORS FOR REFERENCE
#-----------------------------------------------------------------------------
class MotorControl:
    
    #from podium_gui import MainWindow

    def __init__(self):
        self.direc = 0
        self.dir = 0
        self.axis = 0
        self.step_fact_y = 0
        self.step_fact_x = 0
        self.lim = 0
        self.but = 0
        self.flag = 0
        self.trig_but = 0
        print('Initialized MotorControl')

    def step(self, delay):
        '''
        Motor takes a step at given speed, tracks location
        
        INPUTS:     None
        OUTPUTS:    None, but changes global location variables
        '''
        
        #print('taking a step in {} direction' .format(str(self.axis)))
        
        # GPIO high
        sleep(delay)
        #GPIO low
        sleep(delay)
        
        c.x_loc_abs += self.step_fact_x
        c.x_loc += self.step_fact_x*c.mm_per_step
        c.y_loc_abs += self.step_fact_y
        c.y_loc += self.step_fact_y*c.mm_per_step
        
        check_lim()
    
    def accel_control(self, delay_old, delay_new):
        '''
        Prevents jarring, gradually increases/decreases speed
        
        INPUTS:     old speed and new speed
        OUTPUTS:    None, but changes global flag: stop_threads
        '''
        
        
        if abs(delay_new - delay_old) > c.nom_accel:
            print('Initializing accel control')
            while round(delay_old, 3) != round(delay_new):
                self.step(delay_old)
                if delay_new - delay_old > 0:
                    delay_old += c.nom_accel
                else:
                    delay_old -= c.nom_accel
                print('Speed: ', delay_old)
        
        else:
            print('No need for acceleration control')
            pass
    
    def go_lim(self):
        '''
        Goes to given limit at nominal speed
        
        INPUTS:     None
        OUTPUTS:    None, but changes global flag: stop_threads
        '''
        
        print('going to {} {} limit'.format(str(self.direc), str(self.axis)))
        
        self.accel_control(0, c.nom_speed)
        
        while GPIO.input(self.trig_but) == False:
            self.step(c.nom_speed)
            
#        self.accel_control(c.nom_speed, 0) -- not sure how to deal with this one

    def move_pend(self, temp):
        '''
        Moves pendant while given button is pushed
        
        INPUTS:     None
        OUTPUTS:    None, but changes global flag: stop_threads
        '''
        
        # Set direction
        #GPIO.output(self.direc, self.dir)
                
        delay_old = pot_speed()
        
        while temp != 0: #GPIO.input(self.but) == True:
            print('Moving {} in {} drection' .format(str(self.axis), str(self.direc)))

            # Read potentiometer
            delay_new = pot_speed()
            # Compare old and new delay to implement accel control
            self.accel_control(delay_old, delay_new)
            # Take a step
            self.step(delay_new)
            sleep(1)
            print('Number of iterations: ',temp)
            temp-=1 

        # Acceleration control for stop
        self.accel_control(delay_new, 0)
    
    def move_mm(self):
        '''
        Moves 1 mm in given direction, with speed control.
        
        INPUTS:     None
        OUTPUTS:    None, but changes global flag: stop_threads
        '''
        
        print('moving one mm')
        for i in range(0, c.steps_per_mm):
            self.step(c.nom_speed)
            
        self.accel_control(c.nom_speed, 0)
#        

# SET DIRECTION OPTIONS
class up (MotorControl):
    
    def __init__(self):
        self.direc = dir_y
        self.dir = c.UP
        self.axis = pul_y
        self.step_fact_y = 1
        self.step_fact_x = 0
        self.lim = lim_y_pos
        self.but = up_but
        self.flag = posYtrig
        self.trig_but = lim_x_pos
        print('Initialized up')
        
class down (MotorControl):
    
    def __init__(self):
        self.direc = dir_y
        self.dir = c.DOWN
        self.axis = pul_y
        self.step_fact_y = -1
        self.step_fact_x = 0
        self.lim = lim_y_neg
        self.but = down_but
        self.flag = negYtrig
        self.trig_but = lim_x_neg
        print('Initialized down')

class right (MotorControl):
    
    def __init__(self):
        self.direc = dir_x
        self.dir = c.RIGHT
        self.axis = pul_x
        self.step_fact_y = 0
        self.step_fact_x = 1
        self.lim = lim_x_pos
        self.but = right_but
        self.flag = posXtrig
        self.trig_but = lim_y_pos
        print('Initialized right')
        
class left (MotorControl):
    
    def __init__(self):
        self.direc = dir_x
        self.dir = c.LEFT
        self.axis = pul_x
        self.step_fact_y = 0
        self.step_fact_x = -1
        self.lim = lim_x_neg
        self.but = left_but
        self.flag = negXtrig
        self.trig_but = lim_y_neg
        print('Initialized left')

if __name__:
    
    cleanup()
    # Initialize pendant LCD (clear and set up???)
    startup_lcd()
    
