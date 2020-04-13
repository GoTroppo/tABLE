############
# This class defines XC-4438 Microphone Sound sensor
############

# Importing modules
from models.sensors.sensor import Sensor

#### Define class ####
class Xc4438Sensor(Sensor):
  def __init__(self, max_volt=3.3,multiplier=100):
    super(Xc4438Sensor, self).__init__()
    self.is_analog = True

    print("**** Created  xc4438_sensor ****")
    self.MAX_INPUT_VOLTS = max_volt
    self.MULTIPLIER = multiplier

  # Below function will convert data to voltage
  def ConvertVolts(self,data):
    volts = (data * self.MAX_INPUT_VOLTS) / float(1023) # MCP3008 is 10bit (1024)
    volts = round(volts, 2) # Round off to 2 decimal places
    return volts
 
  # Below function will convert data to sound level.
  def ConvertSoundLevel(self,data):
    level = ((data * self.MAX_INPUT_VOLTS * self.MULTIPLIER)/float(1023))
    level = round(level)
    return level