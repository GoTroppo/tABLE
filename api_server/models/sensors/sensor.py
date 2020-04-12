##### This is a base class for sensors
import weakref

class Sensor():
  instances=weakref.WeakSet()

  is_analog=True
  DEBUG_MODE=False
  is_debug_message_printed = False

  def __init__(self):
    print("**** Created  Sensor ****")
    Sensor.instances.add(self)

  def setAnalog(is_analog):
    self.is_analog = is_analog

  def setToDigital():
    self.is_analog = False
  
