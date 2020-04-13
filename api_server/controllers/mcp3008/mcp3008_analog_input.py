from threading import Thread
from time import sleep
from models.sensors.sensor import Sensor

class MCP3008AnalogInput(Thread):
  # Analog Channel ID for MCP3008
  channel_id=None

  #SPI Device instance from Mcp3008Controller
  spi_dev = None

  #Attached Sensor
  attached_sensor=None

  DEBUG_MODE=False
  is_debug_message_printed = False
  TIME_TO_SLEEP = sleep

  stop_monitor=False

  def __init__(self,spi_dev,channel_id,sensor:Sensor,sleep=0.05):
    super(MCP3008AnalogInput, self).__init__()
    self.spi_dev = spi_dev
    self.channel_id=channel_id
    self.attached_sensor=sensor
    self.TIME_TO_SLEEP = sleep
    print("**** Created  MCP3008AnalogInput ****")

  # Read MCP3008 data
  def readAnalogInput(self):
    adc = self.spi_dev.xfer2([1,(8+self.channel_id)<<4,0])
    data = ((adc[1]&3) << 8) + adc[2]
    return data

  def run(self):
    try:
      print("**** Started Monitor ****")

      while True:
        if (self.stop_monitor):
          break
        is_monitor_running=True
        reading = self.readAnalogInput()
 
        if(self.DEBUG_MODE):
          self.is_debug_message_printed = False
          print("Reading : {}".format(reading))
        elif(not self.is_debug_message_printed and not self.DEBUG_MODE):
          self.is_debug_message_printed = True
          print("****** Debug Off *****")

        # ToDo: Need to review the clearing of pixels with other requests
        '''
        if (self.is_neopixel_enabled):
          if(press_output > 100):
            num_pixels=round(press_output/100)
            self.neopixel_controller.current_neopixel.rainbow_meter(num_pixels)
          else:
            self.neopixel_controller.current_neopixel.blank_neopixel()
        '''

        if(self.attached_sensor is not None):
          self.attached_sensor.trigger(reading)

        sleep(self.TIME_TO_SLEEP)

    # When ^C is used put colours back to none
    except KeyboardInterrupt:
      is_monitor_running=False
      print("No more Monitoring on MCP3008 Analog input !!!!!")