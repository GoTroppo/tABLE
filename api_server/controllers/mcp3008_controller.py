############
# This class reads analog input from an MCP3008 analog A/D Converter
############

# Importing modules
import spidev # To communicate with SPI devices
#from time import sleep  # To add delay
#import logging

class Mcp3008Controller:
  spi = spidev.SpiDev() # Created an object

  def __init__(self, sleep=0.05,max_volt=3.3,multiplier=100):
    print("**** Created  Mcp3008Controller ****")

    # Start SPI connection
    self.spi.open(0,0)
    self.spi.max_speed_hz = 1350000

  # Read MCP3008 data
  def readAnalogInput(self,channel):
    adc = self.spi.xfer2([1,(8+channel)<<4,0])
    data = ((adc[1]&3) << 8) + adc[2]
    return data