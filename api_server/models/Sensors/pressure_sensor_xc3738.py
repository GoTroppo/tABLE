############
# This class reads analog input from a XC-3738 Pressure sensor
# which is connected to an MCP3008 analog A/D Converter
############



# Importing modules
import spidev # To communicate with SPI devices
from time import sleep  # To add delay
from threading import Thread
import logging
from controllers.neopixel_controller import NeopixelController


#Define Default Values

# This is the analog channel input number for MCP3008
MCP3008_CHANNEL=0

TIME_TO_SLEEP = 0.05
MAX_INPUT_VOLTS = 3.3
MULTIPLIER = 100

#### Define class ####
class xc3738_sensor(Thread):
  DEBUG_MODE=False
  stop_monitor=False
  is_debug_message_printed = False


  spi = spidev.SpiDev() # Created an object

  neopixel_controller = NeopixelController()

  is_monitor_running = False
  is_neopixel_enabled = True

  def __init__(self, sleep=0.05,max_volt=3.3,multiplier=100):
    print("**** Created  xc3738_sensor ****")
    # Call the Thread class's init function
    Thread.__init__(self)

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
    volts = (data * MAX_INPUT_VOLTS) / float(1023) # MCP3008 is 10bit (1024)
    volts = round(volts, 2) # Round off to 2 decimal places
    return volts
 
  # Below function will convert data to pressure.
  def ConvertPressure(self,data):
    press = ((data * MAX_INPUT_VOLTS * self.MULTIPLIER)/float(1023))
    press = round(press)
    return press

 # def lightUpPixels(reading):


  def run(self):
    try:
      print("**** Started Pressure Sensor Monitor ****")

      while True:
        if (self.stop_monitor):
          break
        is_monitor_running=True
        press_output = self.analogInput(MCP3008_CHANNEL) # Reading from CH0
        press_volts = self.ConvertVolts(press_output)
        press_level = self.ConvertPressure(press_output)
 
        if(self.DEBUG_MODE):
          self.is_debug_message_printed = False
          print("Pressure : {} ({}V) {} bits".format(press_level,press_volts,press_output))
        elif(not self.is_debug_message_printed and not self.DEBUG_MODE):
          self.is_debug_message_printed = True
          print("****** Debug Off *****")

        if (self.is_neopixel_enabled):
          if(press_output > 100):
            num_pixels=round(press_output/100)
            self.neopixel_controller.neopixel.rainbow_meter(num_pixels)
          else:
            self.neopixel_controller.neopixel.blank_neopixel()

        sleep(TIME_TO_SLEEP)

    # When ^C is used put colours back to none
    except KeyboardInterrupt:
      is_monitor_running=False
      print("No more pressure !!!!!")
