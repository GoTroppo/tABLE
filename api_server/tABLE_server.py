import time
from flask import Flask, jsonify, abort, make_response
import threading
import atexit
import os
from dotenv import load_dotenv,find_dotenv

from models.sensors.pressure_sensor_xc3738 import Xc3738Sensor
from controllers.neopixel_controller import NeopixelController
from controllers.mcp3008_controller import Mcp3008Controller

# Check for a '.env' file to retrieve settings
# eg "export ENABLE_PRESSURE_SENSOR=1"
load_dotenv(find_dotenv())

ENABLE_PRESSURE_SENSOR=True if (os.environ.get("ENABLE_PRESSURE_SENSOR") is not None and int(os.environ.get("ENABLE_PRESSURE_SENSOR")) > 0) else False

POOL_TIME = 5 #Seconds

# lock to control access to variable
dataLock = threading.Lock()
# thread handler
yourThread = None

# Define the devices and sensors being used
neopixel_controller = NeopixelController()
mcp3008_controller = Mcp3008Controller()
pressure_sensor_controller = Xc3738Sensor(mcp3008_controller) if ENABLE_PRESSURE_SENSOR else None 

app = Flask(__name__)

@app.route('/')
def index():
    return 'Come on in and sit round the tABLE!'

## Handle Neopixel requests
@app.route('/rainbow_cycle', methods=['GET'])
def do_rainbow_cycle():
    neopixel_controller.do_rainbow_cycle()
    return jsonify({'rainbow_cycle': True})

@app.route('/rainbow_chase', methods=['GET'])
def do_rainbow_chase():
    neopixel_controller.do_rainbow_chase()
    return jsonify({'rainbow_chase': True})

@app.route('/rainbow', methods=['GET'])
def do_rainbow():
    neopixel_controller.do_rainbow()
    return jsonify({'rainbow': True})

# Rainbow meter
@app.route('/rainbow_meter', methods=['GET'])
def do_rainbow_meter():
    neopixel_controller.do_rainbow_meter()
    return jsonify({'rainbow_meter': True})

# Blank the Rainbow meter
@app.route('/rainbow_meter_blank', methods=['GET'])
def do_rainbow_meter_blank():
    neopixel_controller.do_rainbow_meter_blank()
    return jsonify({'rainbow_meter': True})

# Set the brightness for all pixels
@app.route('/brightness/<int:brightness>', methods=['GET'])
def set_pixel_strip_brightness(brightness):
    neopixel_controller.set_pixel_strip_brightness(brightness)
    return jsonify({'brightness': brightness})

# set all pixels to blank
@app.route('/clear', methods=['GET'])
def clear_neopixel():
    neopixel_controller.clear_neopixel()
    return jsonify({'clear': True})

@app.route('/pixel/<int:pixel_index>/<string:pixel_colour>', methods=['GET'])
def set_single_pixel(pixel_index,pixel_colour):
    neopixel_controller.set_single_pixel(pixel_index,pixel_colour)
    return jsonify({'pixel': {'set' : pixel_index}})

@app.route('/pixel/<int:pixel_index>/<string:pixel_colour>/<int:single_only>', methods=['GET'])
def set_one_or_more_pixel(pixel_index,pixel_colour,single_only):
    neopixel_controller.set_one_or_more_pixel(pixel_index,pixel_colour,single_only)
    return jsonify({'pixel': {'set' : pixel_index, 'single_only' :single_only }})

@app.route('/debug_on')
def set_debug_on():
    if (pressure_sensor_controller is not None):
        pressure_sensor_controller.DEBUG_MODE=True
    return 'DEBUG MODE ON'

@app.route('/debug_off')
def set_debug_off():
    if (pressure_sensor_controller is not None):
        pressure_sensor_controller.DEBUG_MODE=False
    return 'DEBUG MODE OFF'

##### This needs work!
"""
@app.route('/enable_pressure_sensor')
def set_pressure_sensor_on():
    global pressure_sensor_controller
    msg = 'Pressure Sensor enabled'
    if (pressure_sensor_controller is not None):
        pressure_sensor_controller=xc3738_sensor()
        startSensorMonitors()
    else:
        msg="Pressure Sensor all ready enabled!"
    return msg
"""

def interrupt():
    global yourThread
    if (yourThread is not None):
        yourThread.cancel()

def startSensorMonitors():
    # Create your thread
    print("startSensorMonitors")
    if (pressure_sensor_controller is not None):
        pressure_sensor_controller.start()

# Initiate
if(ENABLE_PRESSURE_SENSOR):
    startSensorMonitors()
    
    # When you kill Flask (SIGTERM), clear the trigger for the next thread
    atexit.register(interrupt)          

if __name__ == "__main__":
    app.run(host='127.0.0.1')