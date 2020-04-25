############
# This class manages the Raspberry Pi GPIO input/outputs
############

# Importing modules
import sys,errno
from models.sensors.sensor import Sensor
from . gpio_port import GpioPort

#from time import sleep  # To add delay
#import logging

class GpioController:

  # Key - Value pair of analog input instance to sensor object instance
  attached_sensors = {}
  
  def __init__(self, ):
    print("**** Created  GpioController ****")

  def addSensor(self,gpio_id,sensor:Sensor):
    port = GpioPort(gpio_id,sensor)
    self.attached_sensors[port]=sensor

  def getAttachedSensorList(self):
    sensor_list=[]
    for input, sensor_inst in self.attached_sensors.items() :
      sensor_list.append(sensor_inst)

    return sensor_list

  def getAttachedPortsList(self):
    port_list=[]
    for input,sensor_inst in self.attached_sensors.items() :
      port_list.append(input)

    return port_list


