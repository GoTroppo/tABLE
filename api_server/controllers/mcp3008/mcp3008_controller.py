'''
This class reads analog input from an MCP3008 analog A/D Converter
'''

# Importing modules
import sys,errno
import spidev # To communicate with SPI devices
from . mcp3008_analog_input import MCP3008AnalogInput
from models.sensors.sensor import Sensor

#from time import sleep  # To add delay
#import logging

class Mcp3008Controller:
  spi = spidev.SpiDev() # Created an object
  spi_input_id = None

  # Key - Value pair of analog input instance to sensor object instance
  attached_sensors = {}
  
  def __init__(self, spi_input_id,sleep=0.05,max_volt=3.3,multiplier=100):
    print("**** Created  Mcp3008Controller ****")
    try:
      assert spi_input_id == 'spi0' or spi_input_id == 'spi1', "SPI input must be 'spi0' or 'spi1'"
      self.spi_input_id=spi_input_id
    except AssertionError as error:
        # Output expected AssertionErrors.
        print(error)
        sys.exit(errno.EINTR)

    except Exception as exception:
        # Output unexpected Exceptions.
        print(exception, False)
        sys.exit(errno.EINTR)

    # Start SPI connection
    self.spi.open(0,0)
    self.spi.max_speed_hz = 1350000

  def addSensor(self,analog_input_channel,sensor:Sensor):
    input = MCP3008AnalogInput(self.spi,analog_input_channel,sensor)
    self.attached_sensors[input]=sensor
    print("***** Mcp3008Controller addSensor SPI: {}, Input CH: {}, Sensor: {}".format(self.spi,analog_input_channel,id(input)))

  def getInput(self,analog_input_channel):
    for input,sensor in self.attached_sensors.items():
      if(input.getChannel() == analog_input_channel):
        return input
      
    return None          

  def getSensorList(self):
    sensor_list=[]
    for input, sensor_inst in self.attached_sensors.items() :
      sensor_list.append(sensor_inst)

    return sensor_list

  def getAttachedAnalogInputsList(self):
    analog_list=[]
    for input,sensor_inst in self.attached_sensors.items() :
      analog_list.append(input)

    return analog_list

  def getSPI_ID(self):
    return self.spi_input_id

