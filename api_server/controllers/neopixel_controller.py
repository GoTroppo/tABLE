from models.devices.neopixel import Neopixel
import time

class NeopixelController:

  current_neopixel = None
  neopixel_list = {}

  def __init__(self,RPi_GPIO:int):
    #self.neopixel = Neopixel(RPi_GPIO)
    if (RPi_GPIO not in NeopixelController.neopixel_list):
      print("***** Creating NeopixelController for GPIO ", RPi_GPIO)
      NeopixelController.neopixel_list[RPi_GPIO] = Neopixel(Neopixel.getRPiPin(RPi_GPIO))
      print("***** Creating NeopixelController neopixel_list ", NeopixelController.neopixel_list)
      self.current_neopixel = NeopixelController.neopixel_list[RPi_GPIO]
      print("***** Creating NeopixelController current_neopixel ", self.current_neopixel)
      print("***** Created NeopixelController for GPIO ", RPi_GPIO)
    else:
      print("NeopixelController exists!")

  def do_rainbow_cycle(self):
    self.current_neopixel.rainbowCycle(20,1)
    time.sleep(1.0)
    self.current_neopixel.blank_neopixel()
    return True

  def do_rainbow_chase(self):
    self.current_neopixel.theaterChaseRainbow(20,256)
    time.sleep(1.0)
    self.current_neopixel.blank_neopixel()
    return True

  def do_rainbow(self):
    self.current_neopixel.rainbow()
    self.current_neopixel.blank_neopixel()
    return True

  def do_rainbow_meter(self):
    self.current_neopixel.rainbow_meter(10)
    return True

  def do_rainbow_meter_blank(self):
    self.current_neopixel.rainbow_meter(10,True)
    return True
      
  def set_pixel_strip_brightness(self,brightness):
    self.current_neopixel.pixel_strip.setBrightness(brightness)
    self.current_neopixel.pixel_strip.show()
    return True

  def clear_neopixel(self):
    self.current_neopixel.blank_neopixel()
    return True

  def set_single_pixel(self,pixel_index,pixel_colour):
    self.current_neopixel.set_pixel(pixel_index,pixel_colour)
    return True

  def set_one_or_more_pixel(self,pixel_index,pixel_colour,single_only):
    self.current_neopixel.set_pixel(pixel_index,pixel_colour,single_only)
    return True


