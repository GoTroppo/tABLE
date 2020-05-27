from time import sleep
import threading
from controllers.port.port import Port
from models.sensors.sensor import Sensor
from controllers.reactor.reactor_controller import ReactorController
from controllers.port.port_monitor import PortMonitor


class Mcp3008PortMonitor(PortMonitor):
  '''The MCP3008AnalogInput class manages inputs for the MCP3008 Analog to Digital converter chip.
  It will read data from the attached sensor.
  '''


  #SPI Device instance from Mcp3008Controller
  spi_dev = None

  reactor_controller=ReactorController.Instance()

  DEBUG_MODE=False
  is_debug_message_printed = False
  TIME_TO_SLEEP = sleep

  stop_monitor=False

  def __init__(self,mcp300_analog_input,spi_dev,channel_id,sleep=0.05):
    super(Mcp3008PortMonitor, self).__init__(mcp300_analog_input)
    self.is_input=True  #This is always an input reading device
    self.mcp300_analog_input = mcp300_analog_input
    self.spi_dev = spi_dev
    self.channel_id=channel_id
    self.TIME_TO_SLEEP = sleep
    self.name = "Mcp3008PortMonitor_" + str(self.spi_dev) + "_" + str(self.channel_id)
    print("**** Created  Mcp3008PortMonitor {} ****".format(self.ident))
    print("**** Created  Mcp3008PortMonitor Name {} ****".format(self.name))
  
  def readAnalogInput(self):
    '''Read the data in from the attached sensor device.'''

    adc = self.spi_dev.xfer2([1,(8+self.channel_id)<<4,0])
    data = ((adc[1]&3) << 8) + adc[2]
    return data

  def run(self):
    '''Loop through regularly and read data in from attached Sensor.'''

    try:
      print("**** Started Mcp3008PortMonitor {} ****".format(self))

      while True:
        if (self.stop_monitor):
          break
        is_monitor_running=True
        reading = self.readAnalogInput()
        self.DEBUG_MODE=True
        if(self.DEBUG_MODE):
          self.is_debug_message_printed = False
          #print("Mcp3008PortMonitor Reading : {}".format(reading))
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