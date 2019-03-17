# Below are functions used in PODIUM's motor control codes

# all functions must follow syntax:

#def fun():
#    '''
#    definition
#    
#    INPUTS:     
#    OUTPUTS:    
#    '''
#    pass

# UNIVERSAL FUNCTIONS (FOR PENDANT AND GUI)

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

def step(motor, delay):
	'''
	One step
	
	INPUTS:     motor to move, delay (s)
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

#-----------------------------------------------------------------------------


def start_up():
	'''
	Moves motors to (0,0), set speed to nominal, reset reference ('zero point') to (0,0).
	INPUTS:    
	OUTPUTS:    
	'''
	
	global x_loc_abs
	global y_loc_abs
	global x_loc
	global y_loc
	global zero_x
	global zero_y
	
	# Send motors to neg limits
	send_lim(lim_x_neg)
	send_lim(lim_y_neg)
    
	# Set coordinates and zero to (0,0)
	x_loc_abs = 0
	y_loc_abs = 0
	x_loc = 0
	y_loc = 0
	zero_x = 0
	zero_y = 0

#-----------------------------------------------------------------------------
    
def send_lim(lim):
	'''
	Sends motor to given limit at nominal speed.
	
	INPUTS:     limit switch to move to (pin number)
	OUTPUTS:    
	'''
	
	global x_loc_abs
	global y_loc_abs
	
	if lim == lim_x_pos:
		motor = pul_x
		GPIO.output(dir_x, right)
	if lim == lim_x_neg:
		motor = pul_x
		GPIO.output(dir_x, left)
	if lim == lim_y_pos:
		motor = pul_y
		GPIO.output(dir_y, up)
	if lim == lim_y_neg:
		motor = pul_y
		GPIO.output(dir_y, down)
    
	# Move while limit switch not triggered
	while GPIO.input(lim) == False:
		delay = nominalSpeed
		step(motor, delay)
		
	# Set appropriate location to 0
	if lim == lim_x_pos:
		x_loc_abs = max_x
	if lim == lim_x_neg:
		x_loc_abs = 0
	if lim == lim_y_pos:
		y_loc_abs = max_y
	if lim == lim_y_neg:
		y_loc_abs = 0

#-----------------------------------------------------------------------------

def check_lims():
    '''
    Checks limits and stops appropriate motor if limits are hit. Indicates
    limit has been hit on LCD and GUI.
    
    INPUTS:
    OUTPUTS: Has limit been hit? (T/F)
    '''
    
    # Might not need T/F outputs if just printing onto screens
    
	if GPTO.input(lim_x_pos) == True:
		stop()
		return posXtrig
	if GPTO.input(lim_x_neg) == True:
		stop()
		return posYtrig
	if GPTO.input(lim_y_pos) == True:
		stop()
		return negXtrig
	if GPTO.input(lim_y_neg) == True:
		stop()
		return negYtrig
	else:
		return False

#-----------------------------------------------------------------------------

def set_zero():
	'''
	Sends motors to tared zero location
	ENSURE YOU RESET LOCAL COORDINATES TO ZERO OUTSIDE FUNCTION
    
	INPUTS:     
	OUTPUTS:    
	'''
	global zero_x
	global zero_y
	
	# Set new zero coordinates
	zero_x = x_loc_abs
	zero_y = y_loc_abs

#-----------------------------------------------------------------------------

def accel_control():
    '''
	Stops motors immediately (no jarring control)
	INPUTS:     None
	OUTPUTS:    None
    '''
    pass

#-----------------------------------------------------------------------------

def send2zero():
    '''
    Sends motors to tared zero location
    
    INPUTS:     
    OUTPUTS:    
    '''
    pass

#-----------------------------------------------------------------------------

# PENDANT-SPECIFIC 

#-----------------------------------------------------------------------------
def pot_speed():
	'''
	This function converts reads voltage from 1ok potentiometer, and converts it to a delay time.
	NOTE: MUST HAVE SPI SETUP WITH MCP3008 LIBRARY FOR USE
	
	INPUTS:		none
	OUTPUTS: 	delay (seconds)
	'''
	# Define speed/delay and rotpot values
	volt_max = 65472
	volt_min = 2000
	delay_max = 0.01
	delay_min = 0.00001
	
	# Read pot
	pot_volt = chan.value
	volt = convert_volt(pot_volt)
	
	# Conversion
	volt_range = volt_max - volt_min
	delay_range = delay_max - delay_min
	delay = abs(volt*delay_range/volt_range-delay_max)
	
	return delay

#-----------------------------------------------------------------------------

def move_pend(direc):
	'''
	move!
    
    INPUTS:     direction (value is pin of button being pressed)
    OUTPUTS:    None
    '''
    
    # Initialize variables
	global x_loc_abs
	global y_loc_abs
	count = 0
	
	# Set direction of movement and motor pin
	if direc = up_but:
		GPIO.output(dir_y, up)
		motor = pul_y
	if direc = down_but:
		GPIO.output(dir_y, down)
		motor = pul_y
	if direc = right_but:
		GPIO.output(dir_x, right)
		motor = pul_x
	if direc = left_but:
		GPIO.output(dir_x, left)
		motor = pul_x
	
	while GPIO.input(direc) == False:
		delay = pot_speed()
		step(motor, delay)
		
		# Increase step count by 1
		count += count
		
		# Check if limits have been hit
		check_lims()
	
	# Implement jarring control
	
	# Change coordinates
	if direc = up_but:
		y_loc_abs = count + y_loc_abs
	if direc = down_but:
		y_loc_abs = count - y_loc_abs
	if direc = right_but:
		x_loc_abs = count + x_loc_abs
	if direc = left_but:
		x_loc_abs = count - x_loc_abs

#-----------------------------------------------------------------------------

def lcd_print():
    '''
    Prints input input onto LCD screen.
    
    INPUTS:     
    OUTPUTS:    
    '''
    pass

#-----------------------------------------------------------------------------

# GUI SPECIFIC

#-----------------------------------------------------------------------------
