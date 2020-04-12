import sys,os,errno,time,yaml
import threading,atexit
import board
from dotenv import load_dotenv,find_dotenv
from flask import Flask, jsonify, abort, make_response
from yaml.constructor import ConstructorError

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from controllers.neopixel.neopixel_controller import NeopixelController
from controllers.mcp3008.mcp3008_controller import Mcp3008Controller
from models.devices.neopixel import Neopixel
from models.sensors.xc3738_pressure_sensor import Xc3738Sensor
from models.sensors.xc4438_microphone_sound import Xc4438Sensor

# Check for a '.env' file to retrieve settings
# eg "export ENABLE_PRESSURE_SENSOR=1"
load_dotenv(find_dotenv())
DEVICE_CONFIG_FILE=os.environ.get("DEVICE_CONFIG_FILE") if (os.environ.get("DEVICE_CONFIG_FILE") is not None) else None
#DEVICE_CONFIG_FILE=None

DEBUG=False
START_SENSOR_MONITORING=True
POOL_TIME = 5 #Seconds

# lock to control access to variable
dataLock = threading.Lock()
# thread handler
yourThread = None

current_neopixel_controller = None
mcp3008_controller = None
controllers = []

app = Flask(__name__)

@app.route('/')
def index():
  return 'Come on in and sit round the tABLE!'

## Handle Neopixel requests
@app.route('/rainbow_cycle', methods=['GET'])
def do_rainbow_cycle():
  current_neopixel_controller.do_rainbow_cycle()
  return jsonify({'rainbow_cycle': True})

@app.route('/rainbow_chase', methods=['GET'])
def do_rainbow_chase():
  current_neopixel_controller.do_rainbow_chase()
  return jsonify({'rainbow_chase': True})

@app.route('/rainbow', methods=['GET'])
def do_rainbow():
  current_neopixel_controller.do_rainbow()
  return jsonify({'rainbow': True})

# Rainbow meter
@app.route('/rainbow_meter', methods=['GET'])
def do_rainbow_meter():
  current_neopixel_controller.do_rainbow_meter()
  return jsonify({'rainbow_meter': True})

# Blank the Rainbow meter
@app.route('/rainbow_meter_blank', methods=['GET'])
def do_rainbow_meter_blank():
  current_neopixel_controller.do_rainbow_meter_blank()
  return jsonify({'rainbow_meter': True})

# Set the brightness for all pixels
@app.route('/brightness/<int:brightness>', methods=['GET'])
def set_pixel_strip_brightness(brightness):
  current_neopixel_controller.set_pixel_strip_brightness(brightness)
  return jsonify({'brightness': brightness})

# set all pixels to blank
@app.route('/clear', methods=['GET'])
def clear_neopixel():
  current_neopixel_controller.clear_neopixel()
  return jsonify({'clear': True})

@app.route('/pixel/<int:pixel_index>/<string:pixel_colour>', methods=['GET'])
def set_single_pixel(pixel_index,pixel_colour):
  current_neopixel_controller.set_single_pixel(pixel_index,pixel_colour)
  return jsonify({'pixel': {'set' : pixel_index}})

@app.route('/pixel/<int:pixel_index>/<string:pixel_colour>/<int:single_only>', methods=['GET'])
def set_one_or_more_pixel(pixel_index,pixel_colour,single_only):
  current_neopixel_controller.set_one_or_more_pixel(pixel_index,pixel_colour,single_only)
  return jsonify({'pixel': {'set' : pixel_index, 'single_only' :single_only }})

@app.route('/debug_on/<string:device_name>/<int:id>')
def set_debug_on(device_name,id):
  if(device_name == 'mcp3008_input'):
    for controller in controllers:
      if(isinstance(controller, Mcp3008Controller)):
        for analog_input in controller.getAttachedAnalogInputsList():
          if (analog_input is not None and analog_input.channel_id == id):
            analog_input.DEBUG_MODE=True

  return 'DEBUG MODE ON'

@app.route('/debug_off/<string:device_name>/<int:id>')
def set_debug_off(device_name,id):
  if(device_name == 'mcp3008_input'):
    for controller in controllers:
      if(isinstance(controller, Mcp3008Controller)):
        for analog_input in controller.getAttachedAnalogInputsList():
          if (analog_input is not None and analog_input.channel_id == id):
            analog_input.DEBUG_MODE=False

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
  global controllers

  # Create your thread
  print("startSensorMonitors")
  for controller in controllers:
    print("Controller Type: ", type(controller))
    if(isinstance(controller, Mcp3008Controller)):
    #  print("AnalogInputs :" ,controller.getAttachedAnalogInputsList())
      for analog_input in controller.getAttachedAnalogInputsList():
        print("Analog Input Type: ", type(analog_input))
        if (analog_input is not None):
          analog_input.start()

# Reference: https://gist.github.com/pypt/94d747fe5180851196eb
def no_duplicates_constructor(loader, node, deep=False):
  """Check for duplicate keys."""

  mapping = {}
  for key_node, value_node in node.value:
    key = loader.construct_object(key_node, deep=deep)
    value = loader.construct_object(value_node, deep=deep)
    if key in mapping:
      raise ConstructorError("while constructing a mapping", node.start_mark,
                              "found duplicate key (%s)" % key, key_node.start_mark)
    mapping[key] = value

  return loader.construct_mapping(node, deep)

def validate_config():
  try:
    assert DEVICE_CONFIG_FILE != "config/config_example.yaml", "Using example configuration file. Please copy this and customise the copy."
  except  yaml.YAMLError as error_str:
    print("validate_config Error in configuration file:", error_str)
    sys.exit(errno.EINTR)

  with open(DEVICE_CONFIG_FILE) as f:
    try:
      config = yaml.load(f, Loader=yaml.FullLoader)
    except  yaml.YAMLError as error_str:
      print("validate_config Error in configuration file:", error_str)
      sys.exit(errno.EINTR)

    try:
      assert "raspberry_pi" in config, "Configuration File Error: No 'raspberry_pi' item exists!"
    except AssertionError as error:
        # Output expected AssertionErrors.
        print(error)
        sys.exit(errno.EINTR)

    spi_list = []
    gpio_list = []
    mcp3008_list = []

    for pi_input, pi_input_values in config['raspberry_pi'].items() :
      # Check for SPI connected devices
      if(pi_input.find('spi') != -1):
        try:
          assert pi_input == 'spi0' or pi_input == 'spi1', "Configuration File Error: SPI input must be 'spi0' or 'spi1'!"
        except AssertionError as error:
            # Output expected AssertionErrors.
            print(error)
            sys.exit(errno.EINTR)

        try:
          assert pi_input not in spi_list, "Configuration File Error: SPI exists - SPI input must be unique!"
        except AssertionError as error:
            # Output expected AssertionErrors.
            print(error)
            print("SPI = ",pi_input)
            sys.exit(errno.EINTR)

        spi_list.append(pi_input)

        if('mcp3008' in pi_input_values['sensors']):
          for mcp3008_key, mcp3008_values in pi_input_values['sensors']['mcp3008'].items() :
            try:
              assert mcp3008_key not in mcp3008_list, "Configuration File Error: MCP3008 ID exists - MCP3008 ID input must be unique!"
            except AssertionError as error:
                # Output expected AssertionErrors.
                print(error)
                print("MCP3008 ID = ",mcp3008_key)
                sys.exit(errno.EINTR)

            mcp3008_list.append(mcp3008_key)

      # Check for any GPIO pins with devices
      if(pi_input.find('gpio') != -1):
        try:
          assert pi_input not in gpio_list, "Configuration File Error: GPIO exists - GPIO input must be unique!"
        except AssertionError as error:
          # Output expected AssertionErrors.
          print(error)
          print("GPIO = ",pi_input)
          sys.exit(errno.EINTR)

        gpio_list.append(pi_input)
      
  return True

def load_devices_from_config():
  global controllers,current_neopixel_controller
  validate_config()

  with open(DEVICE_CONFIG_FILE) as f:
    try:
      config = yaml.load(f, Loader=yaml.FullLoader)
    except yaml.YAMLError as error_str:
      print("Error in configuration file: {}", error_str)
      sys.exit(errno.EINTR)
    except ConstructorError as err:
      sys.exit(errno.EINTR)

    if "raspberry_pi" in config:
      for pi_input, pi_input_values in config['raspberry_pi'].items() :
        # Check for SPI connected devices
        if(pi_input.find('spi') != -1):
          try:
            assert pi_input == 'spi0' or pi_input == 'spi1', "Configuration File Error: SPI input must be 'spi0' or 'spi1'."
          except AssertionError as error:
              # Output expected AssertionErrors.
              print(error)
              sys.exit(errno.EINTR)
          except Exception as exception:
              # Output unexpected Exceptions.
              print(exception, False)
              sys.exit(errno.EINTR)

          # Found the SPI connections on the Pi
          # Find the associated sensors
          # Loop through each of the MCP3008 and get sensors
          if('mcp3008' in pi_input_values['sensors']):
            sensor_items=[]
            for mcp3008_key, mcp3008_values in pi_input_values['sensors']['mcp3008'].items() :
              if('input_channels' in mcp3008_values):
                sensor_items=mcp3008_values['input_channels']

            if(len(sensor_items) != 0):
              # We have items associated with MCP3008
              # Let's create Mcp3008Controller and associated Sensors
              print("**** Creating Mcp3008Controller for ", pi_input)
              is_mcp_controller_exists=False
              mcp3008_controller=None
              for controller in controllers:
                if(isinstance(controller, Mcp3008Controller)):
                  if(controller.getSPI_ID == pi_input):
                    is_mcp_controller_exists=True
              if(not is_mcp_controller_exists):
                mcp3008_controller=Mcp3008Controller(pi_input)
                controllers.append(mcp3008_controller)

              for sensor_item in mcp3008_values['input_channels']:
                mcp3008_input_id = next(iter(sensor_item))
                sensor_type = sensor_item[mcp3008_input_id]

                if('Xc3738Sensor' in sensor_type):
                  if(mcp3008_controller is not None):
                    print("***** Create Xc3738Sensor *****")
                    mcp3008_controller.addSensor(mcp3008_input_id, Xc3738Sensor())

                if('Xc4438Sensor' in sensor_type):
                  if(mcp3008_controller is not None):
                    print("***** Create Xc4438Sensor *****")
                    mcp3008_controller.addSensor(mcp3008_input_id, Xc4438Sensor())

        # Check for any GPIO pins with devices
        if(pi_input.find('gpio') != -1):
          if('display_device' in pi_input_values):
            display_id = next(iter(pi_input_values['display_device']))
            display_type = pi_input_values['display_device'][display_id]

            if('neopixel' in display_type):
              print("***** Create Neopixel *****")
              gpio_pin=int(pi_input[len('gpio'):])
              if(Neopixel.getRPiPin(gpio_pin) is not None):
                current_neopixel_controller = NeopixelController(gpio_pin)

                #ToDo: Take this out when  we manage triggers better
                for controller in controllers:
                  if(isinstance(controller, Mcp3008Controller)):
                    for sensor in controller.getSensorList():
                      if(isinstance(sensor, Xc3738Sensor)):
                        sensor.addNeopixelController(current_neopixel_controller)

    else:
      print('Configuration File Error: ')
      print('Error in "',DEVICE_CONFIG_FILE,'"')
      print("- No 'raspberry_pi' item exists!")
      sys.exit(errno.EINTR)


    # While Testing exit gunicorn
    if(DEBUG):
      sys.exit(errno.EINTR)

# Add in check for Duplicate Keys
yaml.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, no_duplicates_constructor)

if(DEVICE_CONFIG_FILE is not None):
  load_devices_from_config()

# Initiate
if(DEVICE_CONFIG_FILE is not None and START_SENSOR_MONITORING):
    startSensorMonitors()
    
    # When you kill Flask (SIGTERM), clear the trigger for the next thread
    atexit.register(interrupt)

if __name__ == "__main__":
    app.run(host='127.0.0.1')