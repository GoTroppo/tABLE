# Server for accecpting requests for NeoPixels on Raspberry Pi

from flask import Flask, jsonify, abort, make_response
from flask import request

import time
import board
import neopixel

flask_port=5000
init_brightness = 0.2
#full_brightness_perc = 0.5

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 24

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.

# Order is reversed for Duinotech RGB LED Ring so use GRB
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=init_brightness, auto_write=False,
                           pixel_order=ORDER)

def set_pixel(pixel_index: int, pixel_colour: str, set_single: bool = True):
    if set_single == 1 :
        # Clear all pixels
        pixels.fill((0, 0, 0))

    pixels[pixel_index] = hex_to_rgb(pixel_colour)
    pixels.show()

def blank_neopixel():
    pixels.fill((0, 0, 0))
    pixels.show()

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos*3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos*3)
        g = 0
        b = int(pos*3)
    else:
        pos -= 170
        r = 0
        g = int(pos*3)
        b = int(255 - pos*3)
    return (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)

def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)


def hex_to_rgb(value):
    """Return (red, green, blue) for the color given as hex form for rrggbb."""
    #value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


app = Flask(__name__)

@app.route('/rainbow', methods=['GET'])
def rainbow():
    rainbow_cycle(0.0051)
    time.sleep(1.0)
    blank_neopixel()
    return jsonify({'rainbow': 'Pretty'})

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
    app.run(debug=True, host='0.0.0.0',port=flask_port)
