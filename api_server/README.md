To run the API server use:

```
./start_server.sh
```

##### Configuration
This now uses a `.env` file to customise the environment
One parameter is the `DEVICE_CONFIG_FILE` which defines the hardware configuration of devices connected to Raspberry Pi inputs.

An example configuration file is found at `config/config_example.yaml`. Copy this file to `config/config.yaml` and use this with appropriate configuration.

###### Server API
To use the API see examples at [API documentation](../documentation/api_server/tABLE_server.html).

##### Run the following commands to play with Neopixel ring
Note that you need to use the GPIO number to access

###### Set the brightness to 100 (valid 0 to 255)

```
curl -si localhost:5000/brightness/18/100
```

###### Make a rainbow

```
curl -si localhost:5000/rainbow/18
```

###### Make a rainbow cycle

```
curl -si localhost:5000/rainbow_cycle/18
```

###### Make a rainbow chase

```
curl -si localhost:5000/rainbow_chase/18
```

###### Set pixel LED 9 to Red colour and blank all other pixels

```
curl -si localhost:5000/pixel/18/9/FF0000/1
```

###### Set pixel LED 23 to Green colour and keep all other lit pixels

```
curl -si localhost:5000/pixel/18/23/00FF00/0
```

###### Set all pixel LEDs to blank

```
curl -si localhost:5000/clear/18
```
