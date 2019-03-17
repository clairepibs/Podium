# NOTE THIS IS ALREADY IN PODIUM FUNCTIONS

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
	GPIO.add_event_detect(zero_but, GPIO.BOTH, callback = set_zero)
	GPIO.add_event_detect(save_but, GPIO.BOTH, callback = add_coord)
	
	# Setup motors and directions
	if GPIO.input(right_but) == False:
		GPIO.output(dir_x, right)
		while GPIO.input(right_but) == False:
			delay = pot_speed()
			step(pul_x, delay)
		
			# Increase location by 1
			x_loc_abs += x_loc_abs
			x_loc += x_loc
		
			# Check if limits have been hit
			check_lims()
		
			# Print location on LCD
			printLCD(x_loc, y_loc)
			
	elif GPIO.input(left_but) == False:
		GPIO.output(dir_x, left)
		while GPIO.input(left_but) == False:
			delay = pot_speed()
			step(pul_x, delay)
		
			# Increase location by 1
			x_loc_abs -= x_loc_abs
			x_loc -= x_loc
		
			# Check if limits have been hit
			check_lims()
		
			# Print location on LCD
			printLCD(x_loc, y_loc)
			
	elif GPIO.input(up_but) == False:
		GPIO.output(dir_y, right)
		while GPIO.input(up_but) == False:
			delay = pot_speed()
			step(pul_y, delay)
		
			# Increase location by 1
			y_loc_abs += y_loc_abs
			y_loc += y_loc
		
			# Check if limits have been hit
			check_lims()
		
			# Print location on LCD
			printLCD(x_loc, y_loc)
			
	elif GPIO.input(down_but) == False:
		GPIO.output(dir_y, right)
		while GPIO.input(down_but) == False:
			delay = pot_speed()
			step(pul_y, delay)
		
			# Increase location by 1
			y_loc_abs -= y_loc_abs
			y_loc -= y_loc
		
			# Check if limits have been hit
			check_lims()
		
			# Print location on LCD
			printLCD(x_loc, y_loc)
	
	# Implement jarring control
	
	# Set absolute and local coordinates
	
	
