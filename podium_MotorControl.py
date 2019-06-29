# This is the python script for PODIUM motor control and pendant
# Created on 2019-03-17 by Zoe LeHong

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
import threading

# INITIALIZE VARIABLES

# Other flags
stop_threads = 0
HIGH = 1
LOW = 0

# Stepper motor outputs
dir_x = 2
pul_x = 3
dir_y = 17
pul_y = 27

# Limit switch pins
lim_x_pos = 24
lim_x_neg = 23
lim_y_pos = 12
lim_y_neg = 25

#pendant pins
save_but = 20
zero_but = 21
up_but = 6
down_but = 13
right_but = 19
left_but = 26

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

GPIO.setup(save_but,GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(zero_but,GPIO.IN, pull_up_down = GPIO.PUD_UP)

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
    global lcdbackpack

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
    lcdbackpack.write(" | 00")

#-----------------------------------------------------------------------------

def shutoff_lcd():
    lcdbackpack.display_off()
    #lcdbackpack.disconnect()

#-----------------------------------------------------------------------------

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
        #print('X: {:0.3f}, Y: {:0.3f}' .format(c.x_loc, c.y_loc))

        # Print location on LCD
        lcdbackpack.set_cursor_position(3,1)
        lcdbackpack.write("{:+.3f}".format(c.x_loc))
        lcdbackpack.set_cursor_position(3,2)
        lcdbackpack.write("{:+.3f}".format(c.y_loc))

        sleep(0.5)

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

def pot_speed(min):
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
    delay_range = c.delay_max - min
    delay = abs(volt*delay_range/volt_range-c.delay_max)

    print('Speed: ', delay)

    return delay

# -----------------------------------------------------------------------------

def check_save():
    '''
    This function checks if save button has been pressed.

    INPUTS:   None
    OUTPUTS:  Returns save flag or "false" if save button has not been hit
    '''

    #print('Checking save button')
    #pass


    if GPIO.input(save_but) == True:
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


    if GPIO.input(zero_but) == True:
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
    
    GPIO.output(pul_x, HIGH)
    GPIO.output(pul_y, HIGH)
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

##    GPIO.output(pul_x, HIGH)
##    GPIO.output(pul_y, HIGH)
    
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
    
    GPIO.output(pul_x, HIGH)
    GPIO.output(pul_y, HIGH)
    
    # Set coordinates and zero to (0,0)
    c.x_loc_abs = 0
    c.y_loc_abs = 0
    c.x_loc = 0
    c.y_loc = 0
    c.zero_x = 0
    c.zero_y = 0
    
#-----------------------------------------------------------------------------

def set_zero_pend(*args):
    '''
    Sets current location to zero, updates location trackers
    
    INPUTS:     
    OUTPUTS:    
    '''
    
    print('Setting new zero to current location')
    
    # Set new zero coordinates
    c.zero_x = c.x_loc_abs*c.mm_per_step
    c.zero_y = c.y_loc_abs*c.mm_per_step
    
    # Reset local coordinates
    c.x_loc = 0
    c.y_loc = 0

    print(c.x_loc_abs)
    print(c.y_loc_abs)
    print(c.zero_x)
    print(c.zero_y)
    

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
        self.max_speed = 0
        self.nom_speed = 0
        print('Initialized MotorControl')

    def step(self, delay):
        '''
        Motor takes a step at given speed, tracks location
        
        INPUTS:     None
        OUTPUTS:    None, but changes global location variables
        '''
        
        # Check if limit switch is hit
        if c.posXtrig == "Yes":
            print("Limit switch triggered, cannot move in positive X")
            pass
        if c.negXtrig == "Yes":
            print("Limit switch triggered, cannot move in negative X")
            pass
        if c.posYtrig == "Yes":
            print("Limit switch triggered, cannot move in positive Y")
            pass
        if c.negYtrig == "Yes":
            print("Limit switch triggered, cannot move in negative Y")
            pass
        
        # GPIO high
        GPIO.output(self.axis, HIGH)
        sleep(delay)
        # GPIO low
        GPIO.output(self.axis, LOW)
        sleep(delay)
        
        c.x_loc_abs += self.step_fact_x
        c.x_loc += self.step_fact_x*c.mm_per_step
        c.y_loc_abs += self.step_fact_y
        c.y_loc += self.step_fact_y*c.mm_per_step
        
        #check_lim(None)
    
    def accel_control(self, delay_old, delay_new):
        '''
        Prevents jarring, gradually increases/decreases speed
        
        INPUTS:     old speed and new speed
        OUTPUTS:    None, but changes global flag: stop_threads
        '''
        
        print("stuck in acccel control")
        if abs(delay_new - delay_old) < c.nom_accel:
            print('Initializing accel control')
            while round(delay_old, 4) != round(delay_new,4):
                self.step(delay_old)
                if delay_new - delay_old > 0:
                    delay_old += c.nom_accel
                else:
                    delay_old -= c.nom_accel
                print('Speed: ', delay_old)
        
        else:
            #print('No need for acceleration control')
            pass
    
    def go_lim(self):
        '''
        Goes to given limit at nominal speed
        
        INPUTS:     None
        OUTPUTS:    None, but changes global flag: stop_threads
        '''
        
        print('going to {} {} limit'.format(str(self.direc), str(self.axis)))
        print('THIS FUNCTIONALITY IS COMMENTED OUT UNTER FURTHER REFINING')

##        if self.direc == dir_x:
##            if self.dir == c.RIGHT:
##                for i in range(c.x_loc_abs, c.max_x*c.steps_per_mm):
##                    self.step(self.nom_speed)
##            else:
##                for i in range(c.x_loc_abs, 0):
##                    self.step(self.nom_speed)
##        elif self.direc == dir_y:
##            if self.dir == c.UP:
##                for i in range(c.y_loc_abs, c.max_y*c.steps_per_mm):
##                    self.step(self.nom_speed)
##            else:
##                for i in range(c.y_loc_abs, 0):
##                    self.step(self.nom_speed) 
        
        #self.accel_control(0, self.nom_speed)
##        GPIO.output(self.direc, self.dir)
##        
##        while GPIO.input(self.trig_but) == True:
##            self.step(self.nom_speed)
##
        GPIO.output(pul_x, HIGH)
        GPIO.output(pul_y, HIGH)
            
#        self.accel_control(c.nom_speed, 0) -- not sure how to deal with this one

    def move_pend(self, *args):
        '''
        Moves pendant while given button is pushed
        
        INPUTS:     None
        OUTPUTS:    None, but changes global flag: stop_threads
        '''        
        # Set direction
        GPIO.output(self.direc, self.dir)
                
        delay_old = pot_speed(self.max_speed)

##        limitcheck = threading.Thread(target = check_lim)
##        limitcheck.setDaemon(True)
##        limitcheck.start()

        #print('Moving {} in {} direction' .format(str(self.axis), str(self.direc)))
        
        while GPIO.input(self.but) == False:
            # Read potentiometer
            #delay_new = pot_speed(self.max_speed)
            # Compare old and new delay to implement accel control
            #self.accel_control(delay_old, delay_new)
            # Take a step
            self.step(delay_old)

        print("Button no longer pushed")

        #c.stop_lim_thread = 1

        # Acceleration control for stop
        #self.accel_control(delay_new, 0)
        
        GPIO.output(pul_x, HIGH)
        GPIO.output(pul_y, HIGH)
    
    def move_mm(self):
        '''
        Moves 1 mm in given direction, with speed control.
        
        INPUTS:     None
        OUTPUTS:    None, but changes global flag: stop_threads
        '''

        # Set direction
        GPIO.output(self.direc, self.dir)
        
        print('moving off limit')
        for i in range (0, c.steps_per_mm*2):
            self.step(self.nom_speed)
            
        #self.accel_control(self.nom_speed, 0)

##        GPIO.output(pul_x, HIGH)
##        GPIO.output(pul_y, HIGH)
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
        self.trig_but = lim_y_pos
        self.max_speed = c.delay_min_y
        self.nom_speed = c.nom_speed_y
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
        self.trig_but = lim_y_neg
        self.max_speed = c.delay_min_y
        self.nom_speed = c.nom_speed_y
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
        self.trig_but = lim_x_pos
        self.max_speed = c.delay_min_x
        self.nom_speed = c.nom_speed_x
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
        self.trig_but = lim_x_neg
        self.max_speed = c.delay_min_x
        self.nom_speed = c.nom_speed_x
        print('Initialized left')

if __name__:
    up = up()
    down = down()
    right = right()
    left = left()
    #cleanup()
    # Initialize pendant LCD (clear and set up???)
    startup_lcd()
    GPIO.output(pul_x, HIGH)
    GPIO.output(pul_y, HIGH)
