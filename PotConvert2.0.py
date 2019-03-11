import os 
import time 
import busio 
import digitalio 
import board 
import adafruit_mcp3xxx.mcp3008 as MCP 
from adafruit_mcp3xxx.analog_in import AnalogIn

#values must be verified in testing
volt_min = 0
volt_max = 1023
delay_min = 0.5
delay_max = 0.0001

# create the spi bus 
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select) 
cs = digitalio.DigitalInOut(board.D22)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)
 
# create an analog input channel on pin 0 
chan0 = AnalogIn(mcp, MCP.P0)

def convert_pot():
    '''
    This function reads the current pot state
    and converts it into a delay time to control motor speed
    
    INPUTS: no inputs
    
    OUTPUTS: Delay time
    ** note min/max speed + delay times must be changed in testing
    '''
### note these values need to be verified in testing

    pot_volt = chan0.value
    delay = convert_volt(pot_volt)
    
      ##Uncomment for testing:
    #while True:
     #   pot_volt = read_channel(pot_channel)
      #  delay = convert_volt(pot_volt)
           
           #print Pot Val 
        #   print "--------------------------------------------"
       #    print("Temp : {} ({}V) {} deg C".format(temp_level,temp_volts,temp))
          # wait before repeating loop
          #time.sleep(0.5)
    
    return delay
 
# Define function to change read voltage value to delay time
def convert_volt(voltage):
    volt_range = volt_max - volt_min
    delay_range = delay_max - delay_min
    delay = (((voltage - volt_min)*delay_range)/volt_range)*delay_min
    return delay
 


