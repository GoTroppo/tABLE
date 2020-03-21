# Server for accecpting requests for NeoPixels on Raspberry Pi

from flask import Flask, jsonify, abort, make_response
from flask import request

import time
#import board
import neopixel
from rpi_ws281x import *

# LED strip configuration:
PIXEL_COUNT = 24      # Number of LED pixels.

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
#PIXEL_PIN = board.D18      # GPIO pin connected to the pixels (must support PWM!).
# Needed to change the 
PIXEL_PIN = 18      # GPIO pin connected to the pixels (must support PWM!).

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
pixel_strip = Adafruit_NeoPixel(NUM_PIXELS, PIXEL_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
pixel_strip.begin()

def set_pixel(pixel_index: int, pixel_colour: str, set_single: bool = True):
    if set_single == 1 :
        # Clear all pixels
        blank_neopixel()

    pixel_color_tup = hex_to_rgb(pixel_colour)
    pixel_strip.setPixelColor(pixel_index, Color(pixel_color_tup[0], pixel_color_tup[1], pixel_color_tup[2]))    

    pixel_strip.show()

def blank_neopixel():
    for i in range(0, pixel_strip.numPixels(), 1):
        pixel_strip.setPixelColor(i, Color(0, 0, 0))
    pixel_strip.show()

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50, chase_range=256):
    """Rainbow movie theater light style chaser animation."""
    for j in range(chase_range):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def hex_to_rgb(value):
    """Return (red, green, blue) for the color given as hex form for rrggbb."""
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


app = Flask(__name__)

@app.route('/rainbow_cycle', methods=['GET'])
def do_rainbow_cycle():
    rainbowCycle(pixel_strip,20,1)
    time.sleep(1.0)
    blank_neopixel()
    return jsonify({'rainbow_cycle': True})

@app.route('/rainbow_chase', methods=['GET'])
def do_rainbow_chase():
    theaterChaseRainbow(pixel_strip,20,256)
    time.sleep(1.0)
    blank_neopixel()
    return jsonify({'rainbow_chase': True})

@app.route('/rainbow', methods=['GET'])
def do_rainbow():
    rainbow(pixel_strip)
    blank_neopixel()
    return jsonify({'rainbow': True})

@app.route('/brightness/<int:brightness>', methods=['GET'])
def set_pixel_strip_brightness(brightness):
    pixel_strip.setBrightness(brightness)
    pixel_strip.show()
    return jsonify({'brightness': brightness})

@app.route('/clear', methods=['GET'])
def clear_neopixel():
    blank_neopixel()
    return jsonify({'clear': True})

@app.route('/pixel/<int:pixel_index>/<string:pixel_colour>', methods=['GET'])
def set_single_pixel(pixel_index,pixel_colour):
    set_pixel(pixel_index,pixel_colour)
    return jsonify({'pixel': {'set' : pixel_index}})

@app.route('/pixel/<int:pixel_index>/<string:pixel_colour>/<int:single_only>', methods=['GET'])
def set_one_or_more_pixel(pixel_index,pixel_colour,single_only):
    set_pixel(pixel_index,pixel_colour,single_only)
    return jsonify({'pixel': {'set' : pixel_index, 'single_only' :single_only }})

@app.route('/')
def index():
    return 'Come on in and sit round the tAble!'

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=FLASK_PORT)
