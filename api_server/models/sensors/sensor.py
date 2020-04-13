##### This is a base class for sensors
import weakref

class Sensor(object):
  # Holds all the current Sensors
  instances=weakref.WeakSet()

  # Maps the GPIO pins to instances of display devices
  reactors = {}

  is_analog=True
  DEBUG_MODE=False
  is_debug_message_printed = False

  def __init__(self):
    Sensor.instances.add(self)

  @classmethod
  def get_instances(cls):
    return list(Sensor.instances)

  def setAnalog(self,is_analog):
    self.is_analog = is_analog

  def setToDigital(self):
    self.is_analog = False

  def trigger(self,data):
    pass

  def addReactor(self,id,instance):
    self.reactors[id]=instance

  
