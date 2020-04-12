##### This is a base class for sensors
import weakref
from threading import Thread
import logging

class Sensor(Thread):
  instances=weakref.WeakSet()

  is_analog=True
  DEBUG_MODE=False
  is_debug_message_printed = False

  def __init__(self):
    print("**** Created  Sensor ****")
    Sensor.instances.add(self)

    # Call the Thread class's init function
    super(Thread, self).__init__()

  def setAnalog(is_analog):
    self.is_analog = is_analog

  def setToDigital():
    self.is_analog = False
  
