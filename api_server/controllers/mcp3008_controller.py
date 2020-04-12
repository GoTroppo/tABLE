############
# This class reads analog input from an MCP3008 analog A/D Converter
############

# Importing modules
import sys,errno
import spidev # To communicate with SPI devices
#from time import sleep  # To add delay
#import logging

class Mcp3008Controller:
  spi = spidev.SpiDev() # Created an object
  spi_input_id = None

  # Key - Value pair of analog input port to sensor object
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

  def addSensor(self,analog_input_channel,sensor):
    self.attached_sensors[analog_input_channel]=sensor

  def getSensorList(self):
    print("##### getSensorList")
    sensor_list=[]
    for id, sensor_inst in self.attached_sensors.items() :
      sensor_list.append(sensor_inst)

    return sensor_list

  def getSPI_ID():
    return self.spi_input_id

  # Read MCP3008 data
  def readAnalogInput(self,channel):
    adc = self.spi.xfer2([1,(8+channel)<<4,0])
    data = ((adc[1]&3) << 8) + adc[2]
    return data