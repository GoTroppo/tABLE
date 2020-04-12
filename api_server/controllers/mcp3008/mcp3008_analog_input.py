from threading import Thread
from time import sleep

class MCP3008AnalogInput(Thread):
  channel_id=None
  DEBUG_MODE=False
  is_debug_message_printed = False
  TIME_TO_SLEEP = sleep

  stop_monitor=False
  mcp3008_controller = None

  def __init__(self,mcp3008_controller,channel_id,sleep=0.05,max_volt=3.3,multiplier=100):
    super(MCP3008AnalogInput, self).__init__()
    self.mcp3008_controller = mcp3008_controller
    self.channel_id=channel_id
    self.TIME_TO_SLEEP = sleep
    self.MAX_INPUT_VOLTS = max_volt
    self.MULTIPLIER = multiplier
    print("**** Created  MCP3008AnalogInput ****")

  def run(self):
    try:
      print("**** Started Monitor ****")

      while True:
        if (self.stop_monitor):
          break
        is_monitor_running=True
        reading = self.mcp3008_controller.readAnalogInput(self.channel_id)
 
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

        sleep(self.TIME_TO_SLEEP)

    # When ^C is used put colours back to none
    except KeyboardInterrupt:
      is_monitor_running=False
      print("No more Monitoring on MCP3008 Analog input !!!!!")