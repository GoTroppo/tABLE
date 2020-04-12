############
# This class defines XC-3738 Pressure sensor
############

# Importing modules
from models.sensors.sensor import Sensor

#### Define class ####
class Xc3738Sensor(Sensor):
  neopixel_controller = None

  def __init__(self, max_volt=3.3,multiplier=100):
    super(Sensor, self).__init__()
    self.is_analog = True
    print("**** Created  xc3738_sensor ****")
    self.MAX_INPUT_VOLTS = max_volt
    self.MULTIPLIER = multiplier

  # Below function will convert data to voltage
  def ConvertVolts(self,data):
    volts = (data * self.MAX_INPUT_VOLTS) / float(1023) # MCP3008 is 10bit (1024)
    volts = round(volts, 2) # Round off to 2 decimal places
    return volts
 
  # Below function will convert data to pressure.
  def ConvertPressure(self,data):
    press = ((data * self.MAX_INPUT_VOLTS * self.MULTIPLIER)/float(1023))
    press = round(press)
    return press

  # ToDo: Remove this !!
  def addNeopixelController(self,controller):
    self.neopixel_controller = controller
    print("addNeopixelController")

