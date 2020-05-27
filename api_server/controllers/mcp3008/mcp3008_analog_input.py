from time import sleep
import threading
from controllers.port.port import Port
from models.sensors.sensor import Sensor
from controllers.reactor.reactor_controller import ReactorController
from controllers.mcp3008.mcp3008_analog_input_monitor import Mcp3008PortMonitor

class MCP3008AnalogInput(Port):
  '''The MCP3008AnalogInput class manages inputs for the MCP3008 Analog to Digital converter chip.
  It will read data from the attached sensor.
  '''
   
  # Analog Channel ID for MCP3008
  channel_id=None

  #SPI Device instance from Mcp3008Controller
  spi_dev = None

  #Attached Sensor
  attached_sensor=None

  port_monitor=None

  reactor_controller=ReactorController.Instance()

  DEBUG_MODE=False
  is_debug_message_printed = False
  TIME_TO_SLEEP = sleep

  stop_monitor=False

  def __init__(self,spi_dev,channel_id,sensor:Sensor,sleep=0.05):
    super(MCP3008AnalogInput, self).__init__()
    self.name = "MCP3008AnalogInput_" + str(spi_dev) + "_" + str(channel_id)
    self.is_input=True  #This is always an input reading device
    self.spi_dev = spi_dev
    self.channel_id=channel_id
    self.attached_sensor=sensor
    self.TIME_TO_SLEEP = sleep
    self.port_monitor=Mcp3008PortMonitor(self,spi_dev,channel_id,sleep=0.05)
    #print("**** Created  MCP3008AnalogInput {} ****".format(self.ident))
    print("**** Created  MCP3008AnalogInput Name {} ****".format(self.name))

  def getChannel(self):
    return self.channel_id
  
  def readAnalogInput(self):
    '''Read the data in from the attached sensor device.'''

    adc = self.spi_dev.xfer2([1,(8+self.channel_id)<<4,0])
    data = ((adc[1]&3) << 8) + adc[2]
    return data

  #def run(self):
  def start(self):
    self.port_monitor.start()