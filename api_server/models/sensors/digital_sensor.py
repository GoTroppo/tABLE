# Importing modules
from . sensor import Sensor

class DigitalSensor(Sensor):
  '''
  This class defines Digital Sensors
  '''

  def __init__(self,type):
    super(DigitalSensor, self).__init__(type)
    self.is_analog = False

  def trigger(self,data):
    #print("DigitalSensor {} data {}".format(self.type,data))
    pass


