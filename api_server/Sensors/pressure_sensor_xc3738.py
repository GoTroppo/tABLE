# Importing modules
import spidev # To communicate with SPI devices
from time import sleep  # To add delay


class xc3738_sensor:

  DEBUG_MODE=False

  TIME_TO_SLEEP = 0.05
  MAX_INPUT_VOLTS = 3.3
  MULTIPLIER = 100
  spi = spidev.SpiDev() # Created an object

  def __init__(self, sleep=0.05,max_volt=3.3,multiplier=100):
    print("**** Started Pressure Sensor Monitor ****")

    # Start SPI connection
    self.spi.open(0,0) 
    self.TIME_TO_SLEEP = sleep
    self.MAX_INPUT_VOLTS = max_volt
    self.MULTIPLIER = multiplier
    

  # Read MCP3008 data
  def analogInput(self,channel):
    self.spi.max_speed_hz = 1350000
    adc = self.spi.xfer2([1,(8+channel)<<4,0])
    data = ((adc[1]&3) << 8) + adc[2]
    return data

  # Below function will convert data to voltage
  def ConvertVolts(self,data):
    volts = (data * self.MAX_INPUT_VOLTS) / float(1023) # MCP3008 is 10bit (1024)
    volts = round(volts, 2) # Round off to 2 decimal places
    return volts
 
  # Below function will convert data to pressure.
  def ConvertPressure(self,data):
    press = ((data * self.MAX_INPUT_VOLTS * self.MULTIPLIER)/float(1023))
    press = round(press)
    return press

  def run_monitor(self):
    try:
      while True:
        press_output = self.analogInput(0) # Reading from CH0
        press_volts = self.ConvertVolts(press_output)
        press_level = self.ConvertPressure(press_output)
 
        if (self.DEBUG_MODE):
          print("Pressure : {} ({}V) {} bits".format(press_level,press_volts,press_output))

        sleep(self.TIME_TO_SLEEP)

    # When ^C is used put colours back to none
    except KeyboardInterrupt:
      print("No more pressure !!!!!")
