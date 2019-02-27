import spidev
import time
import os

#values must be verified in testing
volt_min = 0
volt_max = 1023
delay_min = 0.5
delay_max = 0.0001

pot_channel = 0

def convert_pot():
    '''
    This function reads the current pot state
    and converts it into a delay time to control motor speed
    
    INPUTS: no inputs
    
    OUTPUTS: Delay time
    ** note min/max speed + delay times must be changed in testing
    '''
## note these values need to be verified in testing

    # Open SPI bus
    spi = spidev.SpiDev()
    spi.open(0.0)
    spi.max_speed_hz=1000000
    pot_volt = read_channel(pot_channel)
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

#define function to read SPI Data from MCP3008 (ADC)
# Channel 0 will be used to read the rot pot
def read_channel(channel, spi):
    adc = spi.xfer2([1,(8+channel)<<4,0])
    PotVolt = ((adc[1]&3) << 8) + adc[2]
    return PotVolt
 
#define function to change read voltage value to delay time
def convert_volt(voltage):
    volt_range = volt_max - volt_min
    delay_range = delay_max - delay_min
    delay = (((voltage - volt_min)*delay_range)/volt_range)*delay_min
    return delay



