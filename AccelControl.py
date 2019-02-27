def accel_control(desired_speed,current_speed,direction,motor,direction_pin):
    '''
    This function minimizes jarring/vibration for Podium by controlling the acceleration
    
    INPUTS: Desired speed (desired delay time)
            Current Speed (current delay time)
            Direction (pos or neg)
            Motor (x or y)
            Direction Pin (dir_x,dir_y)
              
    OUTPUTS: Desired Speed - delay time 
    
    '''
    #jump range +threshold must be changed from testing
    jump = 10
    threshold = 25
    
    # Check speed change, set current speed
    delt = desired_speed - current_speed
    speed = current_speed
    
    if abs(delt > threshold):
        count = delt/jump
        while (count > 0):
            if delt > 0:
                speed += jump
            else:
                speed -= jump
           ## double check inputs later
            move(motor, speed)
            count -=1
## once while loop finishes will be at desired speed
        
    
    
    
    