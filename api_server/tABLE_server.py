import time
from flask import Flask, jsonify, abort, make_response
import threading
import atexit

from models.Sensors.pressure_sensor_xc3738 import xc3738_sensor
from controllers.neopixel_controller import NeopixelController

ENABLE_PRESSURE_SENSOR=False
POOL_TIME = 5 #Seconds

# variables that are accessible from anywhere
commonDataStruct = "{'a','b'}"
# lock to control access to variable
dataLock = threading.Lock()
# thread handler
yourThread = None
pressure_sensor_controller=None

def create_app():
    global pressure_sensor_controller,ENABLE_PRESSURE_SENSOR

    app = Flask(__name__)
    pressure_sensor_controller = None
    pressure_sensor_controller = xc3738_sensor() if ENABLE_PRESSURE_SENSOR else None 
    neopixel_controller = NeopixelController()

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
        # Do initialisation stuff here
        #global yourThread
        # Create your thread
        print("startSensorMonitors")
        if (pressure_sensor_controller is not None):
            pressure_sensor_controller.start()

    # Initiate
    if(ENABLE_PRESSURE_SENSOR):
        startSensorMonitors()
        
        # When you kill Flask (SIGTERM), clear the trigger for the next thread
        atexit.register(interrupt)

    return app

app = create_app()          
