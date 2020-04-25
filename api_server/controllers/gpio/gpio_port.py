from threading import Thread
from time import sleep
import wiringpi
from models.sensors.sensor import Sensor

class GpioPort(Thread):
  # GPIO Port for Raspberry Pi 
  gpio_id=None

  #Attached Sensor
  attached_sensor=None

  DEBUG_MODE=False
  is_debug_message_printed = False
  TIME_TO_SLEEP = sleep

  stop_monitor=False

  def __init__(self,gpio_id,sensor:Sensor,sleep=0.05):
    super(GpioPort, self).__init__()
    self.gpio_id=gpio_id
    self.attached_sensor=sensor
    self.TIME_TO_SLEEP = sleep
    wiringpi.wiringPiSetupGpio()
    print("**** Created  GpioPort for GPIO {} ****".format(self.gpio_id))

  # Read Input data
  def readInput(self):
    if(self.gpio_id is not None):
      return wiringpi.digitalRead(self.gpio_id)

    return None

  def run(self):
    try:
      print("**** Started GpioPort Monitor ****")

      while True:
        if (self.stop_monitor):
          break
        is_monitor_running=True
        reading = self.readInput()
 
        if(self.DEBUG_MODE):
          self.is_debug_message_printed = False
          print("Reading GpioPort {} = {}".format(self.gpio_id,reading))
        elif(not self.is_debug_message_printed and not self.DEBUG_MODE):
          self.is_debug_message_printed = True
          print("****** Debug Off *****")

        if(self.attached_sensor is not None):
          self.attached_sensor.trigger(reading)

        sleep(self.TIME_TO_SLEEP)

    # When ^C is used put colours back to none
    except KeyboardInterrupt:
      is_monitor_running=False
      print("No more Monitoring on GpioPort {} input !!!!!".format(self.gpio_id))