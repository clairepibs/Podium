# Below are all functions used in PODIUM's motor control codes

#-----------------------------------------------------------------------------

def start_up():
    '''
    definition
    
    INPUTS:     
    OUTPUTS:    
    '''
    pass

#-----------------------------------------------------------------------------
    
def pend_control(stepCount_x, stepCount_y):
    '''
    Continuously reads buttons and potentiometer on pendant, moves motor
    accordingly. Also saves locations based on step tracking.
    
    INPUTS: current location, ie. (X,Y) coordinates
        
    OUTPUTS:
    '''
    # Initialize variables

    # Check speed of motor
    speed = pot_read()
        
    # Continuously check buttons on pendant
            
    while right:
        move(pul_x, speed, TRUE)
        stepCount_x += count_steps()
    while left:
        move(pul_x, speed, FALSE)
        stepcount_x -= count_steps()
    
    while up:
        move(pul_y, speed, TRUE)
        stepCount_y += count_steps()
    while down:
        move(pul_y, speed, FALSE)
        stepCount_y -= count_steps()
        
    if zero:
        send_zero
    elif save:
        #export to GUI
        pass
    
    #pop-up on GUI to avoid simultaneous use

#-----------------------------------------------------------------------------

def move(motor, speed, direc):
    '''
    This function moves according to pendant inputs a single motor while
    simultaneously counting the number of steps taken to determine location
    in plane.
    
    INPUTS:     motor (x or y pulse pin),
                speed from set_speed (duty cycle, 0-100)
                direction (pos or neg)
                
    OUTPUTS:    none
    '''
    
    # Step 1: Initialize variables
    freq = 100000
    
    # Step 2: Set direction pins
    if motor == pul_x:
        GPIO.output(dir_x, direc)
    if motor == pul_y:
        GPIO.output(dir_y, direc)
        
    # Step 3: Set pins to PWM, set frequency
    p = GPIO.PWM(motor, freq)
    
    # Step 4: Make motor move for given speed (duty cycle)
    # WE NEED TO MAKE THIS GRADUAL TO REDUCE JARRING
    p.start(speed)
    # I THINK THIS IS WRONG AND WE WANT TO CHANGE FREQUENCY OR 'DIY' A PWM SIGNAL
#-----------------------------------------------------------------------------

def stop():
    '''
    Stops motors with jarring control
    
    INPUTS:     None
    OUTPUTS:    None
    '''
    pass

#-----------------------------------------------------------------------------

def send_zero():
    '''
    definition
    
    INPUTS:     
    OUTPUTS:    
    '''
    
    pass
    
#-----------------------------------------------------------------------------

def count_steps():
    '''
    Counts steps taken during movment of motor for an unknown period of time.
    
    INPUTS:     None
    OUTPUTS:    Number of steps taken
    '''
    
    stepCount = 0
    stepsPerRev = 1600 # for 1/8 microstepping
    
    # Step ?: Return number of steps
    return stepCount

#-----------------------------------------------------------------------------

def pot_read():
    '''
    definition
    
    INPUTS:     
    OUTPUTS:    
    '''
    pass

#-----------------------------------------------------------------------------

def lcd_print():
    '''
    definition
    
    INPUTS:     
    OUTPUTS:    
    '''
    pass

#-----------------------------------------------------------------------------

def move_gui():
    '''
    definition
    
    INPUTS:     
    OUTPUTS:    
    '''
    pass

#-----------------------------------------------------------------------------

def check_lims():
    '''
    definition
    
    INPUTS:     
    OUTPUTS:    
    '''
    pass

#-----------------------------------------------------------------------------

def calibrate():
    '''
    definition
    
    INPUTS:     
    OUTPUTS:    
    '''
    pass
