from models.devices.neopixel import Neopixel
import time

class NeopixelController:

    neopixel = Neopixel()

    def do_rainbow_cycle(self):
        self.neopixel.rainbowCycle(20,1)
        time.sleep(1.0)
        self.neopixel.blank_neopixel()
        return True

    def do_rainbow_chase(self):
        self.neopixel.theaterChaseRainbow(20,256)
        time.sleep(1.0)
        self.neopixel.blank_neopixel()
        return True

    def do_rainbow(self):
        self.neopixel.rainbow()
        self.neopixel.blank_neopixel()
        return True

    def do_rainbow_meter(self):
        self.neopixel.rainbow_meter(10)
        return True

    def do_rainbow_meter_blank(self):
        self.neopixel.rainbow_meter(10,True)
        return True
        
    def set_pixel_strip_brightness(self,brightness):
        self.neopixel.pixel_strip.setBrightness(brightness)
        self.neopixel.pixel_strip.show()
        return True

    def clear_neopixel(self):
        self.neopixel.blank_neopixel()
        return True

    def set_single_pixel(self,pixel_index,pixel_colour):
        self.neopixel.set_pixel(pixel_index,pixel_colour)
        return True

    def set_one_or_more_pixel(self,pixel_index,pixel_colour,single_only):
        self.neopixel.set_pixel(pixel_index,pixel_colour,single_only)
        return True


