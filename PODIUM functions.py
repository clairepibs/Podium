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

def stop(void):
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
	One step of motor at certain speed
	
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
def printLCD():
	'''
	Prints input input onto LCD screen. Uses global location variables
	
	INPUTS:
	OUTPUTS:    
	'''
	pass
#-----------------------------------------------------------------------------
def send_lim(lim):
	'''
	Sends motor to given limit at nominal speed.
	
	INPUTS:     limit switch to move to (pin number)
	OUTPUTS:    
	'''
	# Initialize global variables
	global x_loc_abs
	global y_loc_abs
	# Send to given limit switch
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
		
	# Set local coordinates and print location to LCD
	x_loc = x_loc_abs - zero_x
	y_loc = y_loc_abs - zero_y
	printLCD()
#-----------------------------------------------------------------------------
def cleanup():
	'''
	Moves motors to (0,0), set speed to nominal, reset reference ('zero point') to (0,0).
	INPUTS:    
	OUTPUTS:    
	'''
	# Initialize global variables
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
def accel_control():
	'''
	Stops motors immediately (no jarring control)
	INPUTS:     None
	OUTPUTS:    None
	'''
	pass
#-----------------------------------------------------------------------------
def add_coord(void):
	'''
	Adds a coordinate to list on GUI, increases index

	INPUTS:     
	OUTPUTS:    
	'''
	global index
	
	sequence.append([x_loc_abs, y_loc_abs])
	
	index += 1
	
	printLCD()
	
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
def check_lims_pend():
    '''
    Checks limits and stops appropriate motor if limits are hit.
    
    INPUTS:
    OUTPUTS:
    '''

	if GPTO.input(lim_x_pos) == True:
		stop()
	if GPTO.input(lim_x_neg) == True:
		stop()
	if GPTO.input(lim_y_pos) == True:
		stop()
	if GPTO.input(lim_y_neg) == True:
		stop()
	else:
		pass 
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
	volt = chan.value
	
	# Conversion
	volt_range = volt_max - volt_min
	delay_range = delay_max - delay_min
	delay = abs(volt*delay_range/volt_range-delay_max)
	
	return delay
#-----------------------------------------------------------------------------
def set_zero_pend():
	'''
	Sets current location to zero, updates location trackers
	
	INPUTS:     
	OUTPUTS:    
	'''
	global zero_x
	global zero_y
	global x_loc
	global y_loc
	
	# Set new zero coordinates
	zero_x = x_loc_abs
	zero_y = y_loc_abs
	
	# Reset local coordinates
	x_loc = 0
	y_loc = 0
	
	# Print new location on LCD
	printLCD()
#-----------------------------------------------------------------------------
def pend_control():
	'''
	Reads buttons and potentiometer on pendant, moves motor
	accordingly. Also saves locations based on step tracking.
    
	INPUTS:
	OUTPUTS:
	'''
	
	# Initialize variables
	global x_loc_abs
	global y_loc_abs
	global x_loc
	global y_loc
    
	# Pop-up on GUI to avoid simultaneous use????????
	
	# Initialize button checks for zero and save
	GPIO.add_event_detect(zero_but, GPIO.RISING, callback = set_zero_pend)
	GPIO.add_event_detect(save_but, GPIO.RISING, callback = add_coord)
	
	# Setup motors and directions
	if GPIO.input(right_but) == False:
		GPIO.output(dir_x, right)
		while GPIO.input(right_but) == False:
			# Check if limits have been hit
			check_lims_pend()
			
			delay = pot_speed()
			step(pul_x, delay)
		
			# Increase location by 1
			x_loc_abs += 1
			x_loc += 1
		
			# Print location on LCD
			printLCD()
			
	elif GPIO.input(left_but) == False:
		GPIO.output(dir_x, left)
		while GPIO.input(left_but) == False:
			# Check if limits have been hit
			check_lims_pend()
			
			delay = pot_speed()
			step(pul_x, delay)
		
			# Increase location by 1
			x_loc_abs -= 1
			x_loc -= 1
		
			# Print location on LCD
			printLCD()
			
	elif GPIO.input(up_but) == False:
		GPIO.output(dir_y, right)
		while GPIO.input(up_but) == False:
			# Check if limits have been hit
			check_lims_pend()
			
			delay = pot_speed()
			step(pul_y, delay)
		
			# Increase location by 1
			y_loc_abs += 1
			y_loc += 1
		
			# Print location on LCD
			printLCD()
			
	elif GPIO.input(down_but) == False:
		GPIO.output(dir_y, right)
		while GPIO.input(down_but) == False:
			# Check if limits have been hit
			check_lims_pend()
			
			delay = pot_speed()
			step(pul_y, delay)
		
			# Increase location by 1
			y_loc_abs -= 1
			y_loc -= 1
		
			# Print location on LCD
			printLCD()
	
	# Implement jarring control
#-----------------------------------------------------------------------------

# GUI SPECIFIC

#-----------------------------------------------------------------------------
def move_GUI(dest_x, dest_y):
    '''
    Sends motors to target location (LOCAL COORDINATES, NOT ABSOLUTE)
    
    INPUTS:     
    OUTPUTS:    
    '''
	# Initialize variables
	global x_loc_abs
	global y_loc_abs
	global x_loc
	global y_loc
	delay = nom_speed
	count = 0
	
	# Move to location
	distance_x = dest_x - x_loc
	distance_y = dest_y - y_loc
	
	# Move motors to new location and set new location variables
	for count in range(0, distance_x):
		step(pul_x, delay)
		
	x_loc_abs += distance_x
	x_loc = x_loc_abs - zero_x
	
	for count in range(0, distance_y):
		step(pul_y, delay)
	y_loc_abs += distance_y
	y_loc = y_loc_abs + distance_y
	
	# Print new location on LCD
	printLCD()
#-----------------------------------------------------------------------------
def check_lims_GUI():
    '''
    Checks limits and stops appropriate motor if limits are hit. Indicates
    limit has been hit on LCD and GUI.
    
    NOTE: DOES THIS ACTUALLY NEED TO CHECK PINS
    
    INPUTS:
    OUTPUTS: Has limit been hit? (T/F)
    '''

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
def set_zero_GUI(x,y):
	'''
	Sets current location to zero, updates location trackers
	
	INPUTS:		new zero coordinates (decimal)  
	OUTPUTS:	
	'''
	global zero_x
	global zero_y
	
	# Set new zero coordinates
	zero_x = x
	zero_y = y
	
	# Reset local coordinates
	x_loc = x_loc_abs - zero_x
	y_loc = y_loc_abs - zero_y
	
	# Print new location on LCD
	printLCD()
#-----------------------------------------------------------------------------
