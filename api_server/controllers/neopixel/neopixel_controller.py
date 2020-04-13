from models.devices.neopixel import Neopixel
import time

class NeopixelController:
  # List of Neopixels associated to GPIO ids
  # eg 18:object_id for GPIO18
  # used as a Class Variable
  neopixel_list = {}

  def __init__(self):
    pass

  def addNeopixel(self,RPi_GPIO:int):
    if (RPi_GPIO not in NeopixelController.neopixel_list):
      NeopixelController.neopixel_list[RPi_GPIO] = Neopixel(Neopixel.getRPiPin(RPi_GPIO))
      print("***** Created Neopixel for GPIO {}".format(RPi_GPIO))
    else:
      print("Neopixel exists for GPIO {}".format(RPi_GPIO))

  def do_rainbow_cycle(self,RPi_GPIO):
    if(NeopixelController.isRpiGpioValid(RPi_GPIO) and RPi_GPIO in self.neopixel_list):
      self.neopixel_list[RPi_GPIO].rainbowCycle(20,1)
      time.sleep(1.0)
      self.neopixel_list[RPi_GPIO].blank_neopixel()
      return True
    return False

  def do_rainbow_chase(self,RPi_GPIO):
    if(NeopixelController.isRpiGpioValid(RPi_GPIO) and RPi_GPIO in self.neopixel_list):
      self.neopixel_list[RPi_GPIO].theaterChaseRainbow(20,256)
      time.sleep(1.0)
      self.neopixel_list[RPi_GPIO].blank_neopixel()
      return True
    return False

  def do_rainbow(self,RPi_GPIO):
    if(NeopixelController.isRpiGpioValid(RPi_GPIO) and RPi_GPIO in self.neopixel_list):
      self.neopixel_list[RPi_GPIO].rainbow()
      self.neopixel_list[RPi_GPIO].blank_neopixel()
      return True
    return False

  def do_rainbow_meter(self,RPi_GPIO):
    if(NeopixelController.isRpiGpioValid(RPi_GPIO) and RPi_GPIO in self.neopixel_list):
      self.neopixel_list[RPi_GPIO].rainbow_meter(10)
      return True
    return False

  def do_rainbow_meter_blank(self,RPi_GPIO):
    if(NeopixelController.isRpiGpioValid(RPi_GPIO) and RPi_GPIO in self.neopixel_list):
      self.neopixel_list[RPi_GPIO].rainbow_meter(10,True)
      return True
    return False
      
  def set_pixel_strip_brightness(self,RPi_GPIO,brightness):
    if(NeopixelController.isRpiGpioValid(RPi_GPIO) and RPi_GPIO in self.neopixel_list):
      self.neopixel_list[RPi_GPIO].pixel_strip.setBrightness(brightness)
      self.neopixel_list[RPi_GPIO].pixel_strip.show()
      return True
    return False

  def clear_neopixel(self,RPi_GPIO):
    if(NeopixelController.isRpiGpioValid(RPi_GPIO) and RPi_GPIO in self.neopixel_list):
      self.neopixel_list[RPi_GPIO].blank_neopixel()
      return True
    return False

  def set_single_pixel(self,RPi_GPIO,pixel_index,pixel_colour):
    if(NeopixelController.isRpiGpioValid(RPi_GPIO) and RPi_GPIO in self.neopixel_list):
      self.neopixel_list[RPi_GPIO].set_pixel(pixel_index,pixel_colour)
      return True
    return False

  def set_one_or_more_pixel(self,RPi_GPIO,pixel_index,pixel_colour,single_only):
    if(NeopixelController.isRpiGpioValid(RPi_GPIO) and RPi_GPIO in self.neopixel_list):
      self.neopixel_list[RPi_GPIO].set_pixel(pixel_index,pixel_colour,single_only)
      return True
    return False

  def isRpiGpioValid(RPi_GPIO:int):
    return RPi_GPIO > 0 and RPi_GPIO < 27
