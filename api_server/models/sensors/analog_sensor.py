from models.sensors.sensor import Sensor

#### Define class ####
class AnalogSensor(Sensor):

  def __init__(self, type,max_volt=3.3,multiplier=100):
    super(AnalogSensor, self).__init__(type)
    print("***** Created AnalogSensor {}".format(type))

    self.is_analog = True
    self.MAX_INPUT_VOLTS = max_volt
    self.MULTIPLIER = multiplier

  def trigger(self,data):
    #print("AnalogSensor {} data {}".format(self.type,data))
    pass

    '''
    for gpio in self.reactors:
      instance=self.reactors[gpio]
      if(isinstance(instance,Neopixel)):
        if(data > 100):
          num_pixels=round(data/100)
          instance.rainbow_meter(num_pixels)
        else:
          instance.blank_neopixel()
    '''
    
  def ConvertVolts(self,data):
    '''This method will convert data to voltage
    '''
    
    volts = (data * self.MAX_INPUT_VOLTS) / float(1023) # MCP3008 is 10bit (1024)
    volts = round(volts, 2) # Round off to 2 decimal places
    return volts
 
  def ConvertPressure(self,data):
    '''
    This method will convert data to analog value.
    '''
    press = ((data * self.MAX_INPUT_VOLTS * self.MULTIPLIER)/float(1023))
    press = round(press)
    return press

