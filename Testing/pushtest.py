import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

##GPIO.setwarnings(false)
#set 40  to be an input pin and intial value to be pulled low (off)
GPIO.setup(40, GPIO.IN, pull_up_down= GPIO.PUD_UP)
GPIO.setup(38, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def button_callback(channel):
	print ("left button was pushed")
	print ("rising edge detected on 38 - grey")

print ("wait for falling edge")

GPIO.add_event_detect(38, GPIO.RISING, callback=button_callback)

while 1:
	try:
		print ("waiting for purple falling edge")
		GPIO.wait_for_edge(40,GPIO.FALLING, timeout=5000)
	except KeyboardInterrupt:
		print("fin")
		GPIO.cleanup()

#print ("fin")

#GPIO.cleanup()


