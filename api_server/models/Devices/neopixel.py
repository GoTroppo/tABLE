# Class to communicate with Neopixel
import time
import board
import neopixel
from rpi_ws281x import *

class Neopixel:
    # LED strip configuration:
    PIXEL_COUNT = 24      # Number of LED pixels.

    # Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
    # NeoPixels must be connected to D10, D12, D18 or D21 to work.
    PIXEL_PIN = board.D18      # GPIO pin connected to the pixels (must support PWM!).

    LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA = 10       # DMA channel to use for generating signal (try 10)
    LED_BRIGHTNESS = 100  # Set to 0 for darkest and 255 for brightest
    # True to invert the signal (when using NPN transistor level shift)
    LED_INVERT = False

    FLASK_PORT=5000

    # The number of NeoPixels
    NUM_PIXELS = 24

    # The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
    # For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.

    # Order is reversed for Duinotech RGB LED Ring so use GRB
    ORDER = neopixel.GRB

    # Create NeoPixel object with appropriate configuration.
    pixel_strip = Adafruit_NeoPixel(NUM_PIXELS, PIXEL_PIN.id, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)

    def __init__(self):
        self.pixel_strip.begin()
        #print("Created instance of NeoPixel")

    # Set specific pixel to colour
    # pixel_colour is a hexadecimal number
    # set_single is a boolean flag to either leave existing pixels showing or only show selected pixel
    def set_pixel(self,pixel_index: int, pixel_colour: str, set_single: bool = True):
        if set_single == 1 :
            # Clear all pixels
            self.blank_neopixel()

        pixel_color_tup = self.hex_to_rgb(pixel_colour)
        self.pixel_strip.setPixelColor(pixel_index, Color(pixel_color_tup[0], pixel_color_tup[1], pixel_color_tup[2]))    

        self.pixel_strip.show()

    # set all pixels to blank
    def blank_neopixel(self):
        for i in range(0, self.pixel_strip.numPixels(), 1):
            self.pixel_strip.setPixelColor(i, Color(0, 0, 0))
        self.pixel_strip.show()

    # Rainbow of colours
    def wheel(self,pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)

    #Draw rainbow that fades across all pixels at once.
    def rainbow(self,num_pixels=None,wait_ms=20,iterations=1):
        if(num_pixels is None):
            num_pixels=self.pixel_strip.numPixels()
        for j in range(256*iterations):
            for i in range(num_pixels):
                self.pixel_strip.setPixelColor(i, self.wheel((i+j) & 255))
            self.pixel_strip.show()
            time.sleep(wait_ms/1000.0)

    #Draw rainbow that fades across all pixels at once.
    def rainbow_meter(self,num_pixels=None,blank_pixels=False,wait_ms=20):
        if(num_pixels is None):
            num_pixels=self.pixel_strip.numPixels()

        if(blank_pixels):
            for i in range(num_pixels,-1,-1):
                self.pixel_strip.setPixelColor(i, 0)
                self.pixel_strip.show()
                time.sleep(wait_ms/1000.0)                
        else:
            #self.blank_neopixel()
            for i in range(num_pixels):
                self.pixel_strip.setPixelColor(i, self.wheel(i & 255))
                self.pixel_strip.show()
                time.sleep(wait_ms/1000.0)
            
    #Draw rainbow that uniformly distributes itself across all pixels.
    def rainbowCycle(self,wait_ms=20, iterations=5):
        for j in range(256*iterations):
            for i in range(self.pixel_strip.numPixels()):
                self.pixel_strip.setPixelColor(i, self.wheel((int(i * 256 / self.pixel_strip.numPixels()) + j) & 255))
            self.pixel_strip.show()
            time.sleep(wait_ms/1000.0)

    #Rainbow movie theater light style chaser animation.
    def theaterChaseRainbow(self,wait_ms=50, chase_range=256):
        for j in range(chase_range):
            for q in range(3):
                for i in range(0, self.pixel_strip.numPixels(), 3):
                    self.pixel_strip.setPixelColor(i+q, self.wheel((i+j) % 255))
                self.pixel_strip.show()
                time.sleep(wait_ms/1000.0)
                for i in range(0, self.pixel_strip.numPixels(), 3):
                    self.pixel_strip.setPixelColor(i+q, 0)

    #Return (red, green, blue) for the color given as hex form for rrggbb.
    def hex_to_rgb(self,value):
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
