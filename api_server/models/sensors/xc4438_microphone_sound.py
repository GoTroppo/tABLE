############
# This class reads analog input from a XC-4438 Microphone Sound sensor
# which is connected to an MCP3008 analog A/D Converter
############

# Importing modules
from time import sleep  # To add delay
from models.sensors.sensor import Sensor
#from controllers.neopixel_controller import NeopixelController
from controllers.mcp3008_controller import Mcp3008Controller

#### Define class ####
class Xc4438Sensor(Sensor):
  stop_monitor=False

  # This is the analog channel input number for MCP3008
  MCP3008_CHANNEL=None

  mcp3008_controller=None
#  neopixel_controller = NeopixelController(18) #Todo 

  is_monitor_running = False
  is_neopixel_enabled = False

  def __init__(self, mcp3008_controller, mcp3008_channel,sleep=0.05,max_volt=3.3,multiplier=100):
    super(Sensor, self).__init__()
    print("**** Created  xc4438_sensor ****")
    self.mcp3008_controller = mcp3008_controller
    self.MCP3008_CHANNEL=mcp3008_channel

    self.TIME_TO_SLEEP = sleep
    self.MAX_INPUT_VOLTS = max_volt
    self.MULTIPLIER = multiplier

  # Below function will convert data to voltage
  def ConvertVolts(self,data):
    volts = (data * self.MAX_INPUT_VOLTS) / float(1023) # MCP3008 is 10bit (1024)
    volts = round(volts, 2) # Round off to 2 decimal places
    return volts
 
  # Below function will convert data to sound level.
  def ConvertSoundLevel(self,data):
    level = ((data * self.MAX_INPUT_VOLTS * self.MULTIPLIER)/float(1023))
    level = round(level)
    return level

  def run(self):
    try:
      print("**** Started Microphone Sound Sensor Monitor ****")

      while True:
        if (self.stop_monitor):
          break
        is_monitor_running=True
        sound_output = self.mcp3008_controller.readAnalogInput(self.MCP3008_CHANNEL)
        sound_volts = self.ConvertVolts(sound_output)
        sound_level = self.ConvertSoundLevel(sound_output)
 
        if(self.DEBUG_MODE):
          self.is_debug_message_printed = False
          print("Sound : {} ({}V) {} bits".format(sound_level,sound_volts,sound_output))
        elif(not self.is_debug_message_printed and not self.DEBUG_MODE):
          self.is_debug_message_printed = True
          print("****** Debug Off *****")

        '''
        if (self.is_neopixel_enabled):
          if(sound_output > 100):
            num_pixels=round(sound_output/100)
            self.neopixel_controller.neopixel.rainbow_meter(num_pixels)
          else:
            self.neopixel_controller.neopixel.blank_neopixel()
        '''
        
        sleep(self.TIME_TO_SLEEP)

    # When ^C is used put colours back to none
    except KeyboardInterrupt:
      is_monitor_running=False
      print("No more sound !!!!!")
