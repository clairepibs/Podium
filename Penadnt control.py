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
	
	delay = nom_speed
    
	# Pop-up on GUI to avoid simultaneous use????????
	
	# Initialize button checks for zero and save
	GPIO.add_event_detect(zero_but, GPIO.BOTH, callback = set_zero)
	GPIO.add_event_detect(save_but, GPIO.BOTH, callback = add_coord)
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
    
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
