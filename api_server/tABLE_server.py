'''This is a python [flask server](https://pypi.org/project/Flask) that runs on a Raspberry Pi 3 and takes requests to read sensor data and set device states (such as a Neopixel Ring).
It has an API to control various devices and ports.

It uses a configuration file to define the devices connected to the Raspberry Pi.
The configuration file path is defined in a `.env` file with the `DEVICE_CONFIG_FILE` variable.
'''

import sys,os,errno,time,yaml
from functools import reduce
import threading,atexit
#import board
from dotenv import load_dotenv,find_dotenv
from flask import Flask, jsonify, abort, make_response
from yaml.constructor import ConstructorError
from models.sensors.analog_sensor import AnalogSensor
from models.sensors.digital_sensor import DigitalSensor
from models.sensors.sensor import Sensor

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from controllers.gpio.gpio_controller import GpioController
from controllers.neopixel.neopixel_controller import NeopixelController
from controllers.mcp3008.mcp3008_controller import Mcp3008Controller
from controllers.reactor.reactor_controller import ReactorController
from models.devices.neopixel import Neopixel
from models.sensors.analog_sensor import AnalogSensor
from models.sensors.digital_sensor import DigitalSensor
from controllers.reactor.custom import *

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

neopixel_controller = None
mcp3008_controller = None

controllers = []
valid_display_devices = ['neopixel']

app = Flask(__name__)

@app.route('/')
def index():
  return 'Come on in and sit round the tABLE!'

## Handle Neopixel requests
@app.route('/neopixel/<int:gpio>/rainbow_cycle', methods=['GET'])
def do_rainbow_cycle(gpio):
    result=neopixel_controller.do_rainbow_cycle(gpio)
    return jsonify({'rainbow_cycle': result})

@app.route('/neopixel/<int:gpio>/rainbow_chase', methods=['GET'])
def do_rainbow_chase(gpio):
    result=neopixel_controller.do_rainbow_chase(gpio)
    return jsonify({'rainbow_chase': result})

@app.route('/neopixel/<int:gpio>/rainbow', methods=['GET'])
def do_rainbow(gpio):
    print("Running neopixel rainbow using {}".format(neopixel_controller))
    result=neopixel_controller.do_rainbow(gpio)
    return jsonify({'rainbow': result})

# Rainbow meter
@app.route('/neopixel/<int:gpio>/rainbow_meter/<int:meter_level>', methods=['GET'])
def do_rainbow_meter(gpio,meter_level):
    result=neopixel_controller.do_rainbow_meter(gpio,meter_level)
    return jsonify({'rainbow_meter': result})

# Blank the Rainbow meter
@app.route('/neopixel/<int:gpio>/rainbow_meter_blank/<int:meter_level>', methods=['GET'])
def do_rainbow_meter_blank(gpio,meter_level):
    result=neopixel_controller.do_rainbow_meter_blank(gpio,meter_level)
    return jsonify({'rainbow_meter': result})

# Set the brightness for all pixels
@app.route('/neopixel/<int:gpio>/brightness/<int:brightness>', methods=['GET'])
def set_pixel_strip_brightness(gpio,brightness):
    '''API: **GET** `/brightness/int:gpio/int:brightness_value`

    Set the Neopixel ring brightness for all pixels for specific GPIO port.
    Valid values for brightness are 0-255
    For example:

    ```
    curl -si localhost:5000/brightness/18/100
    ```

    '''

    result=neopixel_controller.set_pixel_strip_brightness(gpio,brightness)
    response = {'brightness': brightness} if result else False
    return jsonify(response)

# set all pixels to blank
@app.route('/neopixel/<int:gpio>/clear', methods=['GET'])
def clear_neopixel(gpio):
    result=neopixel_controller.clear_neopixel(gpio)
    return jsonify({'clear': result})

@app.route('/neopixel/<int:gpio>/pixel/<int:pixel_index>/<string:pixel_colour>', methods=['GET'])
def set_single_pixel(gpio,pixel_index,pixel_colour):
    result=neopixel_controller.set_single_pixel(gpio,pixel_index,pixel_colour)
    response = {'pixel': {'set' : pixel_index}} if result else False
    return jsonify(response)

@app.route('/neopixel/<int:gpio>/pixel/<int:pixel_index>/<string:pixel_colour>/<int:single_only>', methods=['GET'])
def set_one_or_more_pixel(gpio,pixel_index,pixel_colour,single_only):
    result=neopixel_controller.set_one_or_more_pixel(gpio,pixel_index,pixel_colour,single_only)
    response = {'pixel': {'set' : pixel_index, 'single_only' :single_only }} if result else False
    return jsonify(response)

@app.route('/debug_on/<string:device_name>/<int:id>')
def set_debug_on(device_name,id):
    '''
    TODO: Add in the reference to MCP3008/SPI
    '''

    if(device_name == 'mcp3008_input'):
        print("/debug_on/{}/{}".format(device_name,id))
        controller = getController(Mcp3008Controller,id)
        if(controller is not None):
            for analog_input in controller.getAttachedAnalogInputsList():
                if (analog_input is not None and analog_input.channel_id == id):
                  analog_input.DEBUG_MODE=True
    if(device_name == 'gpio'):
        controller = GpioController.Instance()
        if(controller is not None):
            for gpio_port in controller.getAttachedInputPortsList():
                if (gpio_port is not None and gpio_port.gpio_id == id):
                    gpio_port.DEBUG_MODE=True
    return 'DEBUG MODE ON'

@app.route('/debug_off/<string:device_name>/<int:id>')
def set_debug_off(device_name,id):
    '''
    TODO: Add in the reference to MCP3008/SPI
    '''
    if(device_name == 'mcp3008_input'):
        controller = getController(Mcp3008Controller,id)
        if(controller is not None):
            for analog_input in controller.getAttachedAnalogInputsList():
                if (analog_input is not None and analog_input.channel_id == id):
                    analog_input.DEBUG_MODE=False
    if(device_name == 'gpio'):
        controller = GpioController.Instance()
        if(controller is not None):
            for gpio_port in controller.getAttachedInputPortsList():
                if (gpio_port is not None and gpio_port.gpio_id == id):
                    gpio_port.DEBUG_MODE=False

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

def getController(type,controller_id=None):
  global controllers
  
  #print("###### getController {}".format(type))
  
  for controller in controllers:
    if(isinstance(controller, type)):
      if(type is Mcp3008Controller):
        if(controller_id is not None):
          if(controller.getSPI_ID() == controller_id):
            #print("####### controller {}".format(controller))
            return controller
      else:
        #print("####### controller {}".format(controller))
        return controller
    
  return None

def startSensorMonitors():
  global controllers

  # Create your thread
  print("startSensorMonitors")
  for controller in controllers:
    #print("Controller Type: ", type(controller))
    if(isinstance(controller, Mcp3008Controller)):
      for analog_input in controller.getAttachedAnalogInputsList():
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

def print_config_error(msg):
  print("Configuration File Error in '{}' :".format(DEVICE_CONFIG_FILE))
  print(msg)
  sys.exit(errno.EINTR)

def validate_reactors(config,reactors_list):
    # Check that reactors set for mcp3008 or GPIO match those set up as GPIO
    if('reactors' in reactors_list):
          for reactor_class, reactor_items in reactors_list['reactors'].items():
              if(type(reactor_class) is not str):
                  print_config_error("Invalid Reactor Class - Found '{}'".format(reactor_class))
          
              check = reduce(getattr, reactor_class.split("."), sys.modules[__name__])
              #print_config_error("Check Reactor Class - Found '{}'".format(check))
              
              if(type(reactor_items) is not dict):
                  print_config_error("Invalid Reactor input and device pair - Found '{}'".format(reactor_items))

              for rpi_connect, device_name in reactor_items.items():
                  if(rpi_connect.find('gpio') != -1):
                      # Check if GPIO number is valid
                      gpio_number=int(rpi_connect[len('gpio'):])
                      if(gpio_number < 1 or gpio_number > 26):
                          print_config_error("Invalid GPIO number\nFound '{}'".format(rpi_connect))
                      
                      # Check if neopixel set up is valid
                      if(device_name == 'neopixel'):
                          if(rpi_connect not in config['raspberry_pi']):
                              print_config_error("Reactor for {}, is missing.".format(reactors_list))
                          if('display_device' not in config['raspberry_pi'][rpi_connect]):
                              print_config_error("Invalid type used for GPIO.\nFound '{}':'{}'".format(rpi_connect,next(iter(config['raspberry_pi'][rpi_connect]))))
                          if(device_name not in config['raspberry_pi'][rpi_connect]['display_device']):
                              print_config_error("Reactor for {}, missing.".format(reactors_list))
                      else:
                          print_config_error("Invalid type used for Reactor for {}".format(reactors_list))

def validate_config():
  global valid_display_devices
  try:
    assert DEVICE_CONFIG_FILE != "config/config_example.yaml", "Using example configuration file. Please copy this and customise the copy."
  except yaml.YAMLError as error:
    print_config_error(error)

  with open(DEVICE_CONFIG_FILE) as f:
    try:
      config = yaml.load(f, Loader=yaml.FullLoader)
    except  yaml.YAMLError as error:
      print_config_error(error)

    try:
      assert "raspberry_pi" in config, "No 'raspberry_pi' item exists!"
    except AssertionError as error:
      # Output expected AssertionErrors.
      print_config_error(error)

    spi_list = []
    mcp3008_list = []

    for pi_input, pi_input_values in config['raspberry_pi'].items() :
      # Check for SPI connected devices
      if(pi_input.find('spi') != -1):
        try:
          assert pi_input == 'spi0' or pi_input == 'spi1', "SPI input must be 'spi0' or 'spi1'!\nFound SPI = '{}'".format(pi_input)
        except AssertionError as error:
          print_config_error(error)

        spi_list.append(pi_input)

        if('mcp3008' in pi_input_values['sensors']):
          for mcp3008_id, mcp3008_values in pi_input_values['sensors']['mcp3008'].items():
            if('input_channels' in mcp3008_values):
              for mcp3008_channel_id, sensor_item in mcp3008_values['input_channels'].items():
                print("Input Channel: '{}' - '{}'".format(mcp3008_channel_id,sensor_item))
                print("sensor_item Type: {}".format(type(sensor_item)))
                if(type(sensor_item) is dict):  # If we have not defined 'reactors' then we only get a string
                  sensor_type = next(iter(sensor_item))
                  # Check valid sensor types
                  if(sensor_type not in Sensor.valid_sensor_types["Analog"]):
                    print_config_error("Invalid Sensor Type - '{}'".format(sensor_type))

                  # Check that reactors set for mcp3008 match those set up as gpio
                  if('reactors' in sensor_item[sensor_type]):
                    validate_reactors(config,sensor_item[sensor_type])

      # Check for any Invalid GPIO pin numbers
      #https://www.raspberrypi.org/documentation/usage/gpio/
      if(pi_input.find('gpio') != -1):
        gpio_number=int(pi_input[len('gpio'):])
        if(gpio_number < 1 or gpio_number > 26):
          print_config_error("Invalid GPIO number\nFound '{}'".format(pi_input))
        if('display_device' not in pi_input_values and 'sensor' not in pi_input_values):
          print_config_error("Invalid type used for GPIO.\nFound '{}':'{}'".format(pi_input,next(iter(pi_input_values))))
        if('display_device' in pi_input_values):
          if(pi_input_values['display_device'] not in valid_display_devices):
            print_config_error("Invalid display_device used for GPIO.\nFound '{}':'{}'".format(pi_input,pi_input_values['display_device']))
        else:
          if('sensor' in pi_input_values):
            if(type(pi_input_values['sensor']) is dict):  # If we have not defined 'reactors' then we only get a string
              sensor_type = next(iter(pi_input_values['sensor']))
              # Check valid sensor types
              if(sensor_type not in Sensor.valid_sensor_types["Digital"]):
                print_config_error("Invalid Sensor Type - '{}'".format(sensor_type))

              # Check that reactors set for gpio match those set up as gpio
              if('reactors' in pi_input_values['sensor'][sensor_type]):
                validate_reactors(config,pi_input_values['sensor'][sensor_type])
            else:
              # Is is a valid GPIO sensor ?
              if(pi_input_values['sensor'] not in Sensor.valid_sensor_types["Digital"]):
                print_config_error("Invalid Sensor type used for GPIO.\nFound '{}':'{}'".format(pi_input,pi_input_values['sensor']))



def load_devices_from_config():
  global controllers,neopixel_controller
#  global valid_sensor_types
  global valid_display_devices

  validate_config()

  with open(DEVICE_CONFIG_FILE) as f:
    try:
      config = yaml.load(f, Loader=yaml.FullLoader)
    except yaml.YAMLError as error:
      print_config_error(error)
    except ConstructorError as err:
      sys.exit(errno.EINTR)

    mcp3008_controller=None
    if "raspberry_pi" in config:
      for pi_input, pi_input_values in config['raspberry_pi'].items() :
        # Check for SPI connected devices
        if(pi_input.find('spi') != -1):
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
              #print("**** Creating Mcp3008Controller for ", pi_input)
              
              # We need to check if there is an existing controller for the SPI
              # We can only have one each of SPI0 and SPI1
              mcp3008_controller=getController(Mcp3008Controller,pi_input)
              print("***** mcp3008_controller {}".format(mcp3008_controller))
              if(mcp3008_controller is None):
                print("**** Creating Mcp3008Controller for {}".format(pi_input))
                mcp3008_controller=Mcp3008Controller(pi_input)
                controllers.append(mcp3008_controller)

              for mcp3008_input_id,sensor_item in sensor_items.items():
                sensor_type = None
                reactors=None
                if(type(sensor_item) is dict):  # If we have not defined 'reactors' then we only get a string
                  sensor_type = next(iter(sensor_item))
                else:
                  sensor_type=sensor_item

                sensor_obj=None
                if(sensor_type in Sensor.valid_sensor_types["Analog"]):
                  sensor_obj = AnalogSensor(sensor_type)
                  mcp3008_controller=getController(Mcp3008Controller,pi_input)
                  print("***** mcp3008_controller {} pi_input {}".format(mcp3008_controller,pi_input))
  
                  if(mcp3008_controller is not None and sensor_obj is not None):
                      mcp3008_controller.addSensor(mcp3008_input_id, sensor_obj)
                else:
                  print_config_error("Invalid Sensor Type.\nFound '{}'".format(sensor_type))
                
                # Add in reactors to Sensors
                if(type(sensor_item) is dict):
                  print("Attempting to add Reactors")
                  print("Sensor Item: {}".format(sensor_item))
                  print("Reactors: {}".format(sensor_item[sensor_type]['reactors']))

                  '''
                    for gpio_id, reactor in sensor_item[sensor_type]['reactors'].items():
                      if(sensor_obj is not None):
                        # Set as None until we have created instance associated with GPIO
                        sensor_obj.addReactor(gpio_id,None)
                  '''
                    
                  for reactor_class, reactor_items in sensor_item[sensor_type]['reactors'].items():
                    #print("reactor_items {}".format(reactor_items))
                    
                    for gpio_id, device in reactor_items.items():
                      if(sensor_obj is not None):
                        react_controller=ReactorController.Instance()
                        if(react_controller is None):
                          react_controller=ReactorController.Instance()
                        # Set as None until we have created instance associated with GPIO
                        #sensor_obj.addReactor(gpio_id,None)
                        #print("reactor_items {}".format(reactor_items))
                        #print("***** mcp3008_controller {}".format(mcp3008_controller))
                        input=mcp3008_controller.getInput(mcp3008_input_id)
                        print("Add in reactors to Sensors device: {} {}".format(device,gpio_id))
                        if(gpio_id.find('gpio') != -1):
                          gpio_reactor_id=int(gpio_id[len('gpio'):])
                          if(gpio_reactor_id is not None):
                            print("Adding Reactor: {} {} {}".format(input,reactor_class,gpio_reactor_id))
                            # Create Reactor instance                          
                            react_controller.addReactor(input,reactor_class,gpio_reactor_id)
                              
                  #print("Sensor instances: {}".format(Sensor.instances))

        # Check for any GPIO pins with devices
        if(pi_input.find('gpio') != -1):
          # Check that there is only one device connected
          if('display_device' in pi_input_values):
            display_type = pi_input_values['display_device']

            if(display_type =='neopixel'):
              #print("***** Create Neopixel *****")
              gpio_pin=int(pi_input[len('gpio'):])
              if(Neopixel.getRPiPin(gpio_pin) is not None):
                if(neopixel_controller is None):
                  neopixel_controller = NeopixelController.Instance()
                neopixel_obj=neopixel_controller.addNeopixel(gpio_pin)
                if (neopixel_obj is not None):
                  #print("@@@@@ Adding in neopixel_obj {}".format(neopixel_obj))
                  #print("@@@@@ Adding in neopixel_obj ReactorController.Instance().reactor_input_map {}".format(ReactorController.Instance().reactor_input_map))
                  
                  reactor_input_map = ReactorController.Instance().reactor_input_map
                  for input_obj in reactor_input_map:
                    if(gpio_pin in reactor_input_map[input_obj].rpi_ports):
                      reactor_input_map[input_obj].setRpiPort(gpio_pin,neopixel_obj)

                #Get all sensors and add to reactors if gpio matches
                for sensor in Sensor.get_instances():
                  for gpio in sensor.reactors:
                    if(sensor.reactors[gpio] is None):
                      sensor.reactors[gpio]=NeopixelController.neopixel_list[gpio_pin]

                #ToDo: Take this out when  we manage triggers better
                #for controller in controllers:
                #  if(isinstance(controller, Mcp3008Controller)):
                #    for sensor in controller.getSensorList():
                #      if(isinstance(sensor, Xc3738Sensor)):
                #        sensor.addNeopixelController(neopixel_controller)

          if('sensor' in pi_input_values):
            # Attaching in Sensor to GPIO Port 
            print("%%%%%% Adding Sensors %%%%%%")
           
            sensor_item = pi_input_values['sensor']
            sensor_obj=None
            sensor_type=None
            reactors=None

            if(type(sensor_item) is dict):  # If we have not defined 'reactors' then we only get a string
              sensor_type = next(iter(sensor_item))
              sensor_obj=addSensorToGpioController(sensor_type,int(pi_input[len('gpio'):]))

              #Create sensor object and Add in reactors to Sensors
              for gpio_id, reactor in sensor_item[sensor_type]['reactors'].items():
                if(sensor_obj is not None):
                    # Set as None until we have created instance associated with GPIO
                  sensor_obj.addReactor(gpio_id,None)

            else:
              sensor_type=sensor_item
              sensor_obj=addSensorToGpioController(sensor_type,int(pi_input[len('gpio'):]))

    # While Testing, exit gunicorn
    if(DEBUG):
      sys.exit(errno.EINTR)

# Add in check for Duplicate Keys
yaml.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, no_duplicates_constructor)

if(DEVICE_CONFIG_FILE is not None):
    # Create all Singleton Controllers
    GpioController.Instance()
    ReactorController.Instance()
    NeopixelController.Instance()
    load_devices_from_config()

# Initiate
if(DEVICE_CONFIG_FILE is not None and START_SENSOR_MONITORING):
    startSensorMonitors()
    
    # When you kill Flask (SIGTERM), clear the trigger for the next thread
    atexit.register(interrupt)

if __name__ == "__main__":
    app.run(host='127.0.0.1')