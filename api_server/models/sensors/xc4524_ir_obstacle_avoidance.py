############
# This class defines XC-4524 IR Obstacle Avoidance sensor
# Reference:
#   https://www.jaycar.com.au/arduino-compatible-ir-obstacle-avoidance-sensor-module/p/XC4524
############

# Importing modules
from models.sensors.sensor import Sensor
from models.devices.neopixel import Neopixel

#### Define class ####
class Xc4524Sensor(Sensor):
  neopixel_controller = None

  def __init__(self, max_volt=3.3,multiplier=100):
    super(Xc4524Sensor, self).__init__()

    self.is_analog = True
    print("**** Created  xc4524_sensor ****")
    self.MAX_INPUT_VOLTS = max_volt
    self.MULTIPLIER = multiplier

  def trigger(self,data):
    #print("Xc4524Sensor data {}".format(data))
    #pass
  
    for gpio in self.reactors:
      instance=self.reactors[gpio]
      if(isinstance(instance,Neopixel)):
        if(data < 1):
          instance.set_pixel(10,"0000FF")
        else:
          instance.blank_neopixel()

