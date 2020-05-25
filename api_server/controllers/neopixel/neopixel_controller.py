from models.devices.neopixel import Neopixel
import sys,errno,time

class NeopixelController:
    # List of Neopixels associated to GPIO ids
    # eg 18:object_id for GPIO18
    # used as a Class Variable
    neopixel_list = {}

    __instance = None
    
    @staticmethod 
    def Instance():
        """ Static access method. """
        if NeopixelController.__instance == None:
            NeopixelController()
            print("***** Created NeopixelController *****")
        return NeopixelController.__instance

    def __init__(self):
        if NeopixelController.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            NeopixelController.__instance = self
            print("***** Created NeopixelController NeopixelController.__instance *****")


    def addNeopixel(self,RPi_GPIO:int):
        try:
            assert Neopixel.getRPiPin(RPi_GPIO) is not None, "Incorrect Neopixel Pin"
        except AssertionError as error:
            print("Error in NeopixelController.addNeopixel() : Incorrect Pin error - attempted to use GPIO '{}' for Neopixel".format(RPi_GPIO))
            sys.exit(errno.EINTR)

        if (RPi_GPIO not in NeopixelController.neopixel_list):
            NeopixelController.neopixel_list[RPi_GPIO] = Neopixel(Neopixel.getRPiPin(RPi_GPIO))
            print("***** Created Neopixel for GPIO {}".format(RPi_GPIO))
            return NeopixelController.neopixel_list[RPi_GPIO]

        print("Neopixel exists for GPIO {}".format(RPi_GPIO))
        return None

    def do_rainbow_cycle(self,RPi_GPIO):
        print("NeopixelController.do_rainbow_cycle({})".format(RPi_GPIO))
        if(NeopixelController.isRpiGpioValid(RPi_GPIO) and RPi_GPIO in self.neopixel_list):
            print("Running NeopixelController.do_rainbow_cycle({})".format(RPi_GPIO))
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
        print("NeopixelController do_rainbow {}".format(RPi_GPIO))
        if(NeopixelController.isRpiGpioValid(RPi_GPIO) and RPi_GPIO in self.neopixel_list):
            print("NeopixelController do_rainbow running {}".format(self.neopixel_list[RPi_GPIO]))
            self.neopixel_list[RPi_GPIO].rainbow()
            self.neopixel_list[RPi_GPIO].blank_neopixel()
            return True
        return False

    def do_rainbow_meter(self,RPi_GPIO,meter_level):
        if(NeopixelController.isRpiGpioValid(RPi_GPIO) and RPi_GPIO in self.neopixel_list):
            self.neopixel_list[RPi_GPIO].rainbow_meter(meter_level)
            return True
        return False

    def do_rainbow_meter_blank(self,RPi_GPIO,meter_level):
        if(NeopixelController.isRpiGpioValid(RPi_GPIO) and RPi_GPIO in self.neopixel_list):
            self.neopixel_list[RPi_GPIO].rainbow_meter(meter_level,True)
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

    @staticmethod
    def isRpiGpioValid(RPi_GPIO:int):
        return RPi_GPIO > 0 and RPi_GPIO < 27

