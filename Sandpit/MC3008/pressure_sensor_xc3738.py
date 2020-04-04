# Importing modules
import spidev # To communicate with SPI devices
from time import sleep  # To add delay

TIME_TO_SLEEP = 0.05
MAX_INPUT_VOLTS = 3.3
MULTIPLIER = 100

# Start SPI connection
spi = spidev.SpiDev() # Created an object
spi.open(0,0) 

# Read MCP3008 data
def analogInput(channel):
  spi.max_speed_hz = 1350000
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data

# Below function will convert data to voltage
def ConvertVolts(data):
  volts = (data * MAX_INPUT_VOLTS) / float(1023) # MCP3008 is 10bit (1024)
  volts = round(volts, 2) # Round off to 2 decimal places
  return volts
 
# Below function will convert data to pressure.
def ConvertPressure(data):
  press = ((data * MAX_INPUT_VOLTS * MULTIPLIER)/float(1023))
  press = round(press)
  return press

try:
  while True:
    press_output = analogInput(0) # Reading from CH0
    press_volts = ConvertVolts(press_output)
    press_level = ConvertPressure(press_output)
 
    print("Pressure : {} ({}V) {} bits".format(press_level,press_volts,press_output))
    sleep(TIME_TO_SLEEP)

# When ^C is used put colours back to none
except KeyboardInterrupt:
  print("No more pressure !!!!!")
