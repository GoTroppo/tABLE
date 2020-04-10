############
# This class reads analog input from a XC-3738 Pressure sensor
# which is connected to an MCP3008 analog A/D Converter
############

# Importing modules
from time import sleep  # To add delay
from models.sensors.sensor import Sensor
from controllers.neopixel_controller import NeopixelController
from controllers.mcp3008_controller import Mcp3008Controller

###### Define Default Values

# This is the analog channel input number for MCP3008
MCP3008_CHANNEL=0

TIME_TO_SLEEP = 0.05
MAX_INPUT_VOLTS = 3.3
MULTIPLIER = 100

#### Define class ####
class Xc3738Sensor(Sensor):
  DEBUG_MODE=False
  stop_monitor=False
  is_debug_message_printed = False

  mcp3008_controller=None
  neopixel_controller = NeopixelController()

  is_monitor_running = False
  is_neopixel_enabled = True

  def __init__(self, mcp3008_controller_obj, sleep=0.05,max_volt=3.3,multiplier=100):
    super(Sensor, self).__init__()
    print("**** Created  xc3738_sensor ****")
    self.mcp3008_controller = mcp3008_controller_obj

    self.TIME_TO_SLEEP = sleep
    self.MAX_INPUT_VOLTS = max_volt
    self.MULTIPLIER = multiplier

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

  def run(self):
    try:
      print("**** Started Pressure Sensor Monitor ****")

      while True:
        if (self.stop_monitor):
          break
        is_monitor_running=True
        press_output = self.mcp3008_controller.readAnalogInput(MCP3008_CHANNEL) # Reading from CH0
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
