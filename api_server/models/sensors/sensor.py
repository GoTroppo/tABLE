##### This is a base class for sensors

from threading import Thread
import logging

class Sensor(Thread):
  instances=[]

  is_analog=True
  DEBUG_MODE=False
  is_debug_message_printed = False

  def __init__(self):
    print("**** Created  Sensor ****")
    Sensor.instances.append(self)

    # Call the Thread class's init function
    super(Thread, self).__init__()

  def setAnalog(is_analog):
    self.is_analog = is_analog

  def setToDigital():
    self.is_analog = False
  
