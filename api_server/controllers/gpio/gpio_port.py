#from threading import Thread
import sys,errno
from time import sleep
import RPi.GPIO as GPIO
from controllers.port.port import Port
from controllers.gpio.gpio_port_monitor import GpioPortMonitor
from models.sensors.sensor import Sensor

class GpioPort(Port):
  '''GPIO Port for Raspberry Pi
  This can be set to be input or output
  https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/
  '''

  gpio_id=None
  
  # Set default GPIO function to be input - ie reading from Sensors
  # as per https://sourceforge.net/p/raspberry-gpio-python/wiki/Checking%20function%20of%20GPIO%20channels/
  gpio_function=GPIO.IN  
  
  #Attached Sensor
  attached_device=None
  
  reactor_controller=None
  
  port_monitor=None

  DEBUG_MODE=False
  is_debug_message_printed = False
  TIME_TO_SLEEP = sleep

  stop_monitor=False

  def __init__(self,gpio_id,attached_device,sleep=0.05):
    super(GpioPort, self).__init__()
    self.gpio_id=gpio_id
    self.name = "GpioPort_" + str(gpio_id)
    self.attached_device=attached_device
    self.TIME_TO_SLEEP = sleep
    GPIO.setmode(GPIO.BCM)
    if(isinstance(attached_device, Sensor)):
        self.setFunction(GPIO.IN)
    else:
        self.setFunction(GPIO.OUT)
    self.port_monitor=GpioPortMonitor(self,gpio_id)

    print("**** Created  GpioPort for GPIO {} ****".format(self.gpio_id))
    print("****          GpioPort name {} ****".format(self.name))
    print("****          GpioPort self {} ****".format(self))

  def setFunction(self,type):
        types=[GPIO.IN, GPIO.OUT, GPIO.SPI, GPIO.I2C, GPIO.HARD_PWM, GPIO.SERIAL]
        try:
            assert type in types
            GPIO.setup(self.gpio_id, type)
            self.gpio_function = type

        except AssertionError as error:
            # Output expected AssertionErrors.
            print("AssertionError setFunction type '{}' not valid".format(type))
            print(error)
            sys.exit(errno.EINTR)
            
  def getFunction(self):
        return self.gpio_function

  def getGpioID(self):
        return self.gpio_id
  
  '''
  # Read Input data
  def readInput(self):
    if(self.gpio_function == GPIO.IN):
      if(self.gpio_id is not None):
        return GPIO.input(self.gpio_id)
    return None

  def run(self):
    if(self.gpio_function == GPIO.IN):
      try:
        print("**** Started GpioPort Monitor for {} ****".format(self.gpio_id))

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

          if(self.reactor_controller is not None):
            self.reactor_controller.trigger(self,reading)

          sleep(self.TIME_TO_SLEEP)

      # When ^C is used put colours back to none
      except KeyboardInterrupt:
        is_monitor_running=False
        print("No more Monitoring on GpioPort {} input !!!!!".format(self.gpio_id))
      '''
      
  #def run(self):
  def start(self):
    if(self.gpio_function == GPIO.IN):
      self.port_monitor.start()