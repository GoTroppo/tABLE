# Importing modules
from . sensor import Sensor
from . models.devices.neopixel import Neopixel

#### Define class ####
class Xc4524Sensor(Sensor):
  '''
  This class defines XC-4524 IR Obstacle Avoidance sensor
  Reference:
  - https://www.jaycar.com.au/arduino-compatible-ir-obstacle-avoidance-sensor-module/p/XC4524
  '''

  neopixel_controller = None
  last_reading = None

  def __init__(self, max_volt=3.3,multiplier=100):
    super(Xc4524Sensor, self).__init__()

    self.is_analog = False
    print("**** Created  xc4524_sensor ****")
    self.MAX_INPUT_VOLTS = max_volt
    self.MULTIPLIER = multiplier

  def trigger(self,data):
    #print("Xc4524Sensor data {}".format(data))
    #pass
  
    for gpio in self.reactors:
      instance=self.reactors[gpio]
      if(isinstance(instance,Neopixel)):
        if(data == 0):
          instance.set_pixel(10,"0000FF")
          self.last_reading=data
        else:
          if(self.last_reading == 0):
            instance.blank_neopixel()
            self.last_reading=data


