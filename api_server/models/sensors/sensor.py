##### This is a base class for sensors

from threading import Thread
import logging

class Sensor(Thread):

  isAnalog=True

  def __init__(self):
    print("**** Created  Sensor ****")
    # Call the Thread class's init function
    super(Thread, self).__init__()

  def setAnalog(is_analog):
    self.isAnalog = is_analog

  def setToDigital():
    self.isAnalog = False
  
