import weakref

class Sensor():
  '''
  This is a base class for sensors
  '''
  
  valid_sensor_types = {\
  "Analog" : ["Xc3738Sensor","Xc4438Sensor"], \
  "Digital" : ["Xc4524Sensor"] \
  }
  
  '''
  **Analog Sensors**
  '''
  
  '''This class defines XC-3738 Pressure sensor.
  It is used to read data from the XC-3738 Pressure sensor from Jaycar.
  Reference:
  - https://www.jaycar.com.au/thin-film-pressure-sensor-for-arduino/p/XC3738
  '''
  
  '''This class defines XC-4438 Arduino Compatible Microphone Sound Sensor Module.
  It is used to read data from the XC-3738 Pressure sensor from Jaycar.
  Reference:
  - https://www.jaycar.com.au/arduino-compatible-microphone-sound-sensor-module/p/XC4438
  '''
  
  
  '''
  **Digital Sensors**
  '''
  
  '''
  Xc4524Sensor defines XC-4524 IR Obstacle Avoidance sensor
  Reference:
  - https://www.jaycar.com.au/arduino-compatible-ir-obstacle-avoidance-sensor-module/p/XC4524
  '''
  
  # Holds all the current Sensors
  instances=weakref.WeakSet()

  # Maps the GPIO pins to instances of display devices
  reactors = {}

  is_analog=True
  DEBUG_MODE=False
  is_debug_message_printed = False
  type=None

  def __init__(self,type):
    self.type=type
    Sensor.instances.add(self)

  @classmethod
  def get_instances(cls):
    return list(Sensor.instances)

  def setToAnalog(self):
    self.is_analog = True

  def setToDigital(self):
    self.is_analog = False

  def trigger(self,data):
    pass

  def addReactor(self,id,instance):
    self.reactors[id]=instance

  
