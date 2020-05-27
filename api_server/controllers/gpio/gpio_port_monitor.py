import sys,errno
from time import sleep
import RPi.GPIO as GPIO
from controllers.port.port_monitor import PortMonitor

class GpioPortMonitor(PortMonitor):

  DEBUG_MODE=False
  is_debug_message_printed = False
  TIME_TO_SLEEP = sleep

  stop_monitor=False
  gpio_port=None
  
  def __init__(self,gpio_port,sleep=0.05):
    super(GpioPortMonitor, self).__init__(gpio_port)
    self.gpio_port=gpio_port
    self.TIME_TO_SLEEP = sleep
    
    print("**** Created  GpioPortMonitor for GPIO {} ****".format(self.gpio_port.gpio_id))
    print("****          GpioPortMonitor name {} ****".format(self.name))
    print("****          GpioPortMonitor ident {} ****".format(self.ident))

  
  # Read Input data
  def readInput(self):
    if(self.gpio_port.gpio_function == GPIO.IN):
      if(self.gpio_port.gpio_id is not None):
        return GPIO.input(self.gpio_port.gpio_id)
    return None

  def run(self):
    if(self.gpio_port.gpio_function == GPIO.IN):
      try:
        print("**** Started GpioPortMonitor for {} ****".format(self.gpio_port.gpio_id))

        while True:
          if (self.stop_monitor):
            break
          is_monitor_running=True
          reading = self.readInput()
  
          if(self.DEBUG_MODE):
            self.is_debug_message_printed = False
            print("Reading GpioPort {} = {}".format(self.gpio_port.gpio_id,reading))
          elif(not self.is_debug_message_printed and not self.DEBUG_MODE):
            self.is_debug_message_printed = True
            print("****** Debug Off *****")

          if(self.reactor_controller is not None):
            self.reactor_controller.trigger(self,reading)

          sleep(self.TIME_TO_SLEEP)

      # When ^C is used put colours back to none
      except KeyboardInterrupt:
        is_monitor_running=False
        print("No more Monitoring on GpioPort {} input !!!!!".format(self.gpio_id))