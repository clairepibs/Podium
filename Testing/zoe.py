import RPi.GPIO as GPIO
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# Define Motor parameters
# Note: changed motor pins to BCM to test
dir_x = 2
pul_x = 3

right = 21
left = 20

HIGH = 1
LOW = 0

# Define speed/delay and rotpot values
volt_max = 65472
volt_min = 2000
delay_max = 0.01
delay_min = 0.00001

# Set GPIO pins for motor output
GPIO.setup(dir_x,GPIO.OUT)
GPIO.setup(pul_x,GPIO.OUT)
# Set GPIO pins for internal resistance
GPIO.setup(right, GPIO.IN, pull_up_down= GPIO.PUD_UP)
GPIO.setup(left, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D22)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan = AnalogIn(mcp, MCP.P0)

GPIO.setwarnings(False) #do not show any warnings

def convert_volt(voltage):

	volt_range = volt_max - volt_min
	delay_range = delay_max - delay_min
	delay = abs(voltage*delay_range/volt_range-delay_max)
	return delay

def convert_pot():
	'''This function reads the value of the rot pot and 
	converts it to a delay to be used for motor speed'''
	pot_volt = chan.value
	delay = convert_volt(pot_volt)
	return delay

def move (direction):

	dir = 0

	if direction == right:
		dir = 1
	try:
		while GPIO.input(direction) == False:
			timeI = time.time()

			# set direction pin
			GPIO.output(dir_x, dir)
			print("Direction: ", dir)

			speed = convert_pot()

        		# set pulse to high
			GPIO.output(pul_x, False)
        		# delay for ON (min 10 us)
			time.sleep(speed)
        		# set pulse to low
			GPIO.output(pul_x, True)
        		# delay for OFF
			time.sleep(speed)

			print('Raw ADC Value: \tTime Delay: ', chan.value, convert_pot())
			timeF=time.time()
			print(timeF-timeI)

	except KeyboardInterrupt:
		GPIO.cleanup()

# START OF MAIN CODE

GPIO.add_event_detect(right, GPIO.BOTH, callback = move)
GPIO.add_event_detect(left, GPIO.BOTH, callback = move)

try:
	while 1:
		pass

except KeyboardInterrupt:
	GPIO.cleanup()
