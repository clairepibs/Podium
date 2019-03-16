#iteration 1 to test motor direction, continually enables motors
#changes motor direction after 5 seconds 
import RPi.GPIO as GPIO
from time import sleep
 
GPIO.setmode(GPIO.BOARD)

ena_x = 3
dir_x = 5
pul_x = 7
 
GPIO.setup(ena_x,GPIO.OUT)
GPIO.setup(dir_x,GPIO.OUT)
GPIO.setup(pul_x,GPIO.OUT)
 
print ("Turning Motor Forward")
GPIO.output(ena_x,GPIO.HIGH)
GPIO.output(dir_x,GPIO.HIGH)
#this needs to be changed to pwm
GPIO.output(pul_x,GPIO.HIGH)

sleep(5)

print ("Turning Motor Backward")
GPIO.output(ena_x,GPIO.LOW)
GPIO.output(dir_x,GPIO.HIGH)
#this needs to be changed to pwm
GPIO.output(pul_x,GPIO.HIGH)
sleep(5)
print ("Stopping motor")
GPIO.output(pul_x,GPIO.LOW)
 
GPIO.cleanup()
