#import sys
#sys.path.append('./Devices')
#sys.path.append('./Sensors/')

import time
from flask import Flask, jsonify, abort, make_response
import threading
import atexit
from models.Sensors.pressure_sensor_xc3738 import xc3738_sensor
from models.Devices.table_neopixel import Neopixel

POOL_TIME = 5 #Seconds

# variables that are accessible from anywhere
commonDataStruct = {}
# lock to control access to variable
dataLock = threading.Lock()
# thread handler
yourThread = threading.Thread()


def create_app():
    app = Flask(__name__)
    press_sensor = xc3738_sensor()
    neopixel = Neopixel()
#    pressure_sensor_controller = 

    @app.route('/')
    def index():
        return 'Come on in and sit round the tAble!'

    ## Define API routes
    @app.route('/rainbow_cycle', methods=['GET'])
    def do_rainbow_cycle():
        neopixel.rainbowCycle(20,1)
        time.sleep(1.0)
        neopixel.blank_neopixel()
        return jsonify({'rainbow_cycle': True})

    @app.route('/rainbow_chase', methods=['GET'])
    def do_rainbow_chase():
        neopixel.theaterChaseRainbow(20,256)
        time.sleep(1.0)
        neopixel.blank_neopixel()
        return jsonify({'rainbow_chase': True})

    @app.route('/rainbow', methods=['GET'])
    def do_rainbow():
        neopixel.rainbow()
        neopixel.blank_neopixel()
        return jsonify({'rainbow': True})

    # Set the brightness for all pixels
    @app.route('/brightness/<int:brightness>', methods=['GET'])
    def set_pixel_strip_brightness(brightness):
        neopixel.pixel_strip.setBrightness(brightness)
        neopixel.pixel_strip.show()
        return jsonify({'brightness': brightness})

    # set all pixels to blank
    @app.route('/clear', methods=['GET'])
    def clear_neopixel():
        neopixel.blank_neopixel()
        return jsonify({'clear': True})

    @app.route('/pixel/<int:pixel_index>/<string:pixel_colour>', methods=['GET'])
    def set_single_pixel(pixel_index,pixel_colour):
        neopixel.set_pixel(pixel_index,pixel_colour)
        return jsonify({'pixel': {'set' : pixel_index}})

    @app.route('/pixel/<int:pixel_index>/<string:pixel_colour>/<int:single_only>', methods=['GET'])
    def set_one_or_more_pixel(pixel_index,pixel_colour,single_only):
        neopixel.set_pixel(pixel_index,pixel_colour,single_only)
        return jsonify({'pixel': {'set' : pixel_index, 'single_only' :single_only }})

    @app.route('/debug_on')
    def set_debug_on():
        press_sensor.DEBUG_MODE=True
        return 'DEBUG MODE ON'

    @app.route('/debug_off')
    def set_debug_off():
        press_sensor.DEBUG_MODE=False
        return 'DEBUG MODE OFF'

    def interrupt():
        global yourThread
        yourThread.cancel()

    def doStuff():
        global commonDataStruct
        global yourThread
        with dataLock:
        # Do your stuff with commonDataStruct Here
          #print("commonDataStruct")
          press_sensor.run_monitor()

        # Set the next thread to happen
        #yourThread = threading.Timer(POOL_TIME, doStuff, ())
        #yourThread.start()   

    def doStuffStart():
        # Do initialisation stuff here
        global yourThread
        # Create your thread
        yourThread = threading.Timer(POOL_TIME, doStuff, ())
        yourThread.start()

    # Initiate
    doStuffStart()
    # When you kill Flask (SIGTERM), clear the trigger for the next thread
    atexit.register(interrupt)
    return app

app = create_app()          
