To run the API server use:

```
start_server.sh
```


##### Run the following commands to play with Neopixel ring


###### Set the brightness to 100 (valid 0 to 255)

```
curl -si localhost:5000/brightness/100
```

###### Make a rainbow

```
curl -si localhost:5000/rainbow
```

###### Make a rainbow cycle

```
curl -si localhost:5000/rainbow_cycle
```

###### Make a rainbow chase

```
curl -si localhost:5000/rainbow_chase
```

###### Set pixel LED 9 to Red colour and blank all other pixels

```
curl -si localhost:5000/pixel/9/FF0000/1
```

###### Set pixel LED 23 to Green colour and keep all other lit pixels

```
curl -si localhost:5000/pixel/23/00FF00/0
```

###### Set all pixel LEDs to blank

```
curl -si localhost:5000/clear
```
