from time import sleep
import threading
from controllers.port.port import Port
from models.sensors.sensor import Sensor
from controllers.reactor.reactor_controller import ReactorController
#from controllers.mcp3008.mcp3008_analog_input_monitor import Mcp3008PortMonitor
from controllers.port.port_monitor import PortMonitor

class MCP3008AnalogInput(PortMonitor):
  '''The MCP3008AnalogInput class manages inputs for the MCP3008 Analog to Digital converter chip.
  It will read data from the attached sensor.
  '''
   
  # Analog Channel ID for MCP3008
  channel_id=None

  #SPI Device instance from Mcp3008Controller
  spi_dev = None

  #Attached Sensor
  attached_sensor=None

  reactor_controller=ReactorController.Instance()

  DEBUG_MODE=False
  is_debug_message_printed = False
  TIME_TO_SLEEP = 0.05  # Default value

  stop_monitor=False

  def __init__(self,spi_dev,channel_id,sensor:Sensor,default_sleep=0.05):
    super(MCP3008AnalogInput, self).__init__(self)
    self.name = "MCP3008AnalogInput_" + str(spi_dev) + "_" + str(channel_id)
    self.is_input=True  #This is always an input reading device
    self.spi_dev = spi_dev
    self.channel_id=channel_id
    self.attached_sensor=sensor
    self.TIME_TO_SLEEP = default_sleep
    #print("**** Created  MCP3008AnalogInput Name {} ****".format(self.name))

  def getChannel(self):
    return self.channel_id
  
  def readAnalogInput(self):
    '''Read the data in from the attached sensor device.'''

    adc = self.spi_dev.xfer2([1,(8+self.channel_id)<<4,0])
    data = ((adc[1]&3) << 8) + adc[2]
    return data


  def run(self):
    '''Loop through regularly and read data in from attached Sensor.'''

    try:
      #print("**** Started MCP3008AnalogInput {} ****".format(self))

      while True:
        if (self.stop_monitor):
          break
        is_monitor_running=True
        reading = self.readAnalogInput()
        self.DEBUG_MODE=True
        if(self.DEBUG_MODE):
          self.is_debug_message_printed = False
          #print("MCP3008AnalogInput Reading : {}".format(reading))
        elif(not self.is_debug_message_printed and not self.DEBUG_MODE):
          self.is_debug_message_printed = True
          print("****** Debug Off *****")
          
        if(self.reactor_controller is not None):
          self.reactor_controller.trigger(self,reading)
        
        sleep(self.TIME_TO_SLEEP)

    except KeyboardInterrupt:
    # When ^C is used put colours back to none
      is_monitor_running=False
      print("No more Monitoring on MCP3008 Analog input !!!!!")
