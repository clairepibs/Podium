#THINGS TO BE CAREFUL ABOUT
# 5V???? HELP?????
# Make sure this isnt python 2

import time
import serial
serialport = serial.Serial('/dev/ttyUSB0',9600, timeout=1)

#clear screen
serialport.write('\xfe\x01')

#write 2 lines of text
serialport.write('Raspberry PI    ')
serialport.write('/dev/ttyUSB0    ')

#switch screen off
serialport.write('\xfe\x08')
time.sleep(0.5)

#switch screen on
serialport.write('\xfe\x0c')
time.sleep(2)

#scroller
serialport.write('\xfe\x01')
serialport.write('_-==scroller==-_ ')
for num in range(0,16):
	serialport.write('\xfe\x1c')
	time.sleep(0.5)	
for num in range(0,16):
	serialport.write('\xfe\x18')
	time.sleep(0.5) 
	
#close connection
serialport.close()
