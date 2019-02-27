# Below are functions used in PODIUM's motor control codes

#-----------------------------------------------------------------------------

def move(motor, delay):
    '''
    move!
    
    INPUTS:     None
    OUTPUTS:    None
    '''
    
    # set pulse to high
    GPIO.output(motor, HIGH)
    # delay for ON (min 10 us)
    time.sleep(delay)
    # set pulse to low
    GPIO.output(motor, LOW)
    # delay for OFF
    time.sleep(delay)
    
    # Check if limits have been hit
    check_lims()

#-----------------------------------------------------------------------------

def stop():
    '''
    Stops motors immediately (no jarring control)
    
    INPUTS:     None
    OUTPUTS:    None
    '''
    GPIO.output(pul_x, LOW)
    GPIO.ouput(pul_y, LOW)

#-----------------------------------------------------------------------------

def start_up():
    '''
    Moves motors to (0,0), set speed to nominal, reset reference ('zero point')
    to (0,0).
    
    INPUTS:     
    OUTPUTS:    
    '''
    
    # Send motors to neg limits
    send_lim(pul_x, dir_x, FALSE, lim_x_neg)
    send_lim(pul_y, dir_y, FALSE, lim_y_neg)
    
    # Set coordinates to (0,0)
    stepCount_x = 0
    stepCount_y = 0
    
    # Set speed to nominal (may not need this)
    delay = nom_speed

#-----------------------------------------------------------------------------
    
def send_lim(motor, direcPin, lim, limSwitch):
    '''
    Sends motor to given limit at nominal speed.
    
    INPUTS:     
    OUTPUTS:    
    '''
    # May need to have lim conversions based on mech setup
    
    # Set direction
    GPIO.output(direcPin, lim)
    
    # Set to nominal speed
    delay = nom_speed
    
    # Move while limit switch not triggered
    while limSwitch:
        move(motor, delay)
        
#-----------------------------------------------------------------------------

def check_lims():
    '''
    Checks limits and stops appropriate motor if limits are hit. Indicates
    limit has been hit on LCD and GUI.
    
    INPUTS:
    OUTPUTS: Has limit been hit? (T/F)
    '''
    
    # Might not need T/F outputs if just printing onto screens
    
    if lim_x_pos:
        stop()
        return TRUE
    if lim_x_pos:
        stop()
        return TRUE
    if lim_x_pos:
        stop()
        return TRUE
    if lim_x_pos:
        stop()
        return TRUE
    else:
        break
    
    # Visually indicate limits have been reached
    lcd_print()

#-----------------------------------------------------------------------------
    
def pend_control():
    '''
    Reads buttons and potentiometer on pendant, moves motor
    accordingly. Also saves locations based on step tracking.
    
    INPUTS:
        
    OUTPUTS:
    '''
    # Initialize variables
    global stepCount_x
    global stepCount_y
    delay = nom_speed
    
    # Pop-up on GUI to avoid simultaneous use

    # Check initial speed
    delay = convert_pot()
    
    # Check X-axis buttons
    if right:
        GPIO.output(dir_x, pos_x)           # Set direction to positive x
        while right:            
            # Check speed of motor, and set delay time
            delay = speed_control()
            
            # Move up one step
            move(pul_x, delay)
            
            # Count steps
            stepCount_x += stepCount_x
            
            # Print location on LCD screen every X seconds???
                
    if left:
        GPIO.output(dir_x, !pos_x)
        while left:
            # Check speed of motor, and set delay time
            delay = speed_control()
            
            # Move up one step
            move(pul_x, delay)
            
            # Count steps
            stepCount_x -= stepCount_x
    
    # Check Y-axis buttons
    if up:
        GPIO.output(dir_y, pos_y)
        while up:
            # Check speed of motor, and set delay time
            delay = speed_control()
            
            # Move up one step
            move(pul_y, delay)
            
            # Count steps
            stepCount_y += stepCount_y
    if down:
        GPIO.output(dir_y, !pos_y)
        while down:
            # Check speed of motor, and set delay time
            delay = speed_control()
            
            # Move up one step
            move(pul_y, delay)
            
            # Count steps
            stepCount_y -= stepCount_y

#-----------------------------------------------------------------------------

def lcd_print():
    '''
    Prints input input onto LCD screen.
    
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

def calibrate():
    '''
    definition
    
    INPUTS:     
    OUTPUTS:    
    '''
    pass