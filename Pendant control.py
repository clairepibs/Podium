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
		direc = right_but
		loc = x_loc
		
		move_pend(right_but, pul_x)
	elif GPIO.input(left_but) == False:
		move_pend(left_but)
	elif GPIO.input(up_but) == False:
		move_pend(up_but)
	elif GPIO.input(down_but) == False:
		move_pend(down_but)
	
	# Move loop
	while GPIO.input(direc) == False:
		delay = pot_speed()
		step(motor, delay)
		
		# Increase location by 1
		count += count
		
		# Check if limits have been hit
		check_lims()
		
		# Print location on LCD
		printLCD()
		
	# Implement jarring control
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
    
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
