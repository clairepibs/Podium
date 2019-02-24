import RPi.GPIO as GPIO
from time import sleep
 
GPIO.setmode(GPIO.BOARD)
 
Motor1_pin1 = 16
Motor1_pin2 = 18
Motor1_pin3 = 22
 
GPIO.setup(Motor1_pin1,GPIO.OUT)
GPIO.setup(Motor1_pin2,GPIO.OUT)
GPIO.setup(Motor1_pin3,GPIO.OUT)
 
print ("Turning Motor Forward")
GPIO.output(Motor1_pin1,GPIO.HIGH)
GPIO.output(Motor1_pin2,GPIO.LOW)
GPIO.output(Motor1_pin3,GPIO.HIGH)
sleep(5)
print ("Turning Motor Backward")
GPIO.output(Motor1_pin1,GPIO.LOW)
GPIO.output(Motor1_pin2,GPIO.HIGH)
GPIO.output(Motor1_pin3,GPIO.HIGH)
sleep(5)
print ("Stopping motor")
GPIO.output(Motor1_pin3,GPIO.LOW)
 
GPIO.cleanup()