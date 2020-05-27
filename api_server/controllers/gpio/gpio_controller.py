# Importing modules
import sys,errno
import RPi.GPIO as GPIO
from models.sensors.sensor import Sensor
from . gpio_port import GpioPort
#from . gpio_port_dummy import GpioPortDummy

#from time import sleep  # To add delay
#import logging

class GpioController:
  '''
  This class manages the Raspberry Pi GPIO input/outputs
  '''

  # Key - Value pair of analog input instance to sensor object instance
  attached_sensors = {}
  
  # Device Instances that are attached to GPIO ports
  # Key - Value pair of analog input instance to device object instance
  # where device object instance can be of type Sensor, Neopixel 
  attached_devices = {}

  __instance = None

  @staticmethod 
  def Instance():
    """ Static access method. """
    if GpioController.__instance == None:
      GpioController()
      print("***** Created GpioController *****")
    return GpioController.__instance
  
  def __init__(self):
      if GpioController.__instance != None:
          raise Exception("This class is a singleton!")
      else:
          GpioController.__instance = self
  
  def addSensor(self,gpio_id,sensor:Sensor):
        try:
            assert isinstance(sensor,Sensor)
#            port = GpioPortDummy(gpio_id,sensor)
            port = GpioPort(gpio_id,sensor)
            self.attached_devices[port]=sensor
            print(">>>>> GpioController addSensor gpio_id {} port {} sensor {}".format(gpio_id,port,sensor))
            print(">>>>> GpioController addSensor Sensor added for ID {}".format(port.getGpioID()))

        except AssertionError as error:
            # Output expected AssertionErrors.
            print("AssertionError Sensor needs to be a valid Sensor class")
            sys.exit(errno.EINTR)      

  def addDevice(self,gpio_id,device):
    print(">>>>> GpioController addDevice gpio_id {} device {}".format(gpio_id,device))
    #port = GpioPortDummy(gpio_id,device)
    port = GpioPort(gpio_id,device)
    self.attached_devices[port]=device
    print(">>>>> GpioController addDevice self.attached_devices {}".format(self.attached_devices))
    print(">>>>> GpioController addDevice device added for ID {}".format(port.getGpioID()))
    for gpio_port in self.attached_devices:
      print("GpioController addDevice loop - name {} port {} ID {}".format(gpio_port.name,gpio_port,gpio_port.getGpioID()))

  def getAttachedSensorList(self):
    sensor_list=[]
    for input, sensor_inst in self.attached_sensors.items() :
      sensor_list.append(sensor_inst)

    return sensor_list

  def getAttachedInputPortsList(self):
    #print("%%%%% GpioController getAttachedInputPortsList:\n{}".format(self.attached_devices))
    port_list=[]
    for port in self.attached_devices :
      #print("%%%%% GpioController getAttachedInputPortsList port {}".format(port))
      if(port.getFunction() == GPIO.IN):
        port_list.append(port)

    print("%%%%% GpioController getAttachedInputPortsList port_list {}".format(port_list))
    return port_list
  
  def getAttachedDevice(self,gpio_id):
        '''Retrieve the device object for gpio_id'''
        #print(">>>>>> GpioController getAttachedDevice self.attached_devices:\n{}".format(self.attached_devices))
        #print(">>>>>> GpioController getAttachedDevice looking for {}".format(gpio_id))
        for gpio_port in self.attached_devices:
              #print("GpioController getAttachedDevice loop - name {} port {} ID {}".format(gpio_port.name,gpio_port,gpio_port.getGpioID()))
              #print("GpioController getAttachedDevice loop {} ID {} -- {}".format(gpio_port.name,gpio_port.getGpioID(),self.attached_devices[gpio_port]))
              #print("GpioController getAttachedDevice loop {} -- {}".format(gpio_port,self.attached_devices[gpio_port]))
              if (gpio_port.getGpioID() == gpio_id):
                    return self.attached_devices[gpio_port]
        return None


