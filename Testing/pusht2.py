import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

##GPIO.setwarnings(false)
#set 40  to be an input pin and intial value to be pulled low (off)
GPIO.setup(40, GPIO.IN, pull_up_down= GPIO.PUD_UP)
GPIO.setup(38, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def button_callback(channel):
	print ("button pressed")

GPIO.add_event_detect(38, GPIO.FALLING, callback= button_callback)
GPIO.add_event_detect(40, GPIO.FALLING, callback= button_callback)

t=0

while t < 30:
	try:
		t = t +1
		time.sleep(1)
		print (t)
	except KeyboardInterrupt:
		print ("fin")
		GPIO.cleanup()
GPIO.cleanup
