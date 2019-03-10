
import RPi.GPIO as GPIO
import time

dir_x = 5
pul_x = 7
HIGH =1
LOW = 0

GPIO.setup(dir_x,GPIO.OUT)
GPIO.setup(pul_x,GPIO.OUT)

#programming the GPIO by Board numbers
GPIO.setmode(GPIO.BOARD) 
GPIO.setwarnings(False) #do not show any warnings


while 1:
    GPIO.output(5, HIGH)
    
    # set pulse to high
    GPIO.output(7, LOW)
    # delay for ON (min 10 us)
    time.sleep(0.5)
    # set pulse to low
    GPIO.output(7, HIGH)
    # delay for OFF
    time.sleep(0.5)
