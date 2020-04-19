EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:switches
LIBS:relays
LIBS:motors
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
LIBS:Logic_LevelTranslator
LIBS:tABLE
LIBS:LED
LIBS:tABLE_example-cache
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L MCP3008 U?
U 1 1 5E9BAE52
P 5300 4900
F 0 "U?" H 5100 5425 50  0000 R CNN
F 1 "MCP3008" H 5100 5350 50  0000 R CNN
F 2 "" H 5400 5000 50  0001 C CNN
F 3 "" H 5400 5000 50  0001 C CNN
	1    5300 4900
	1    0    0    -1  
$EndComp
$Comp
L Raspberry_Pi_2_3 J?
U 1 1 5E9BAF49
P 2600 4100
F 0 "J?" H 3300 2850 50  0000 C CNN
F 1 "Raspberry_Pi_2_3" H 2200 5000 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_2x20" H 3600 5350 50  0001 C CNN
F 3 "" H 2650 3950 50  0001 C CNN
	1    2600 4100
	-1   0    0    -1  
$EndComp
$Comp
L +5V #PWR?
U 1 1 5E9BB53A
P 4550 1850
F 0 "#PWR?" H 4550 1700 50  0001 C CNN
F 1 "+5V" H 4550 1990 50  0000 C CNN
F 2 "" H 4550 1850 50  0001 C CNN
F 3 "" H 4550 1850 50  0001 C CNN
	1    4550 1850
	1    0    0    -1  
$EndComp
$Comp
L TXB0102DCT U?
U 1 1 5E9BB8BB
P 5250 3200
F 0 "U?" H 5450 3700 50  0000 C CNN
F 1 "TXB0102DCT" H 5550 2700 50  0000 C CNN
F 2 "Housings_SSOP:TSSOP-8_3x3mm_Pitch0.65mm" H 6200 2600 50  0001 C CNN
F 3 "" H 5250 3170 50  0001 C CNN
	1    5250 3200
	1    0    0    -1  
$EndComp
$Comp
L +3.3V #PWR?
U 1 1 5E9BB9B2
P 2700 1450
F 0 "#PWR?" H 2700 1300 50  0001 C CNN
F 1 "+3.3V" H 2700 1590 50  0000 C CNN
F 2 "" H 2700 1450 50  0001 C CNN
F 3 "" H 2700 1450 50  0001 C CNN
	1    2700 1450
	1    0    0    -1  
$EndComp
$Comp
L GNDREF #PWR?
U 1 1 5E9BB9CC
P 5500 6900
F 0 "#PWR?" H 5500 6650 50  0001 C CNN
F 1 "GNDREF" H 5500 6750 50  0000 C CNN
F 2 "" H 5500 6900 50  0001 C CNN
F 3 "" H 5500 6900 50  0001 C CNN
	1    5500 6900
	1    0    0    -1  
$EndComp
Text Label 5550 2800 0    60   ~ 0
LogicLevelConverter
$Comp
L XC3738_Pressure_Sensor U?
U 1 1 5E9BFC44
P 8950 5250
F 0 "U?" H 8950 5150 60  0000 C CNN
F 1 "XC3738_Pressure_Sensor" H 8950 5300 60  0000 C CNN
F 2 "" H 8950 5250 60  0001 C CNN
F 3 "" H 8950 5250 60  0001 C CNN
	1    8950 5250
	1    0    0    1   
$EndComp
Connection ~ 4550 1850
Connection ~ 2700 1450
Wire Wire Line
	1550 1450 7000 1450
Wire Wire Line
	2400 1850 10350 1850
Connection ~ 2700 2800
Connection ~ 2400 2800
Connection ~ 5600 1850
Connection ~ 4150 1450
Connection ~ 5150 1450
Connection ~ 5350 1850
Wire Wire Line
	2800 2800 2800 1850
Connection ~ 2800 1850
Wire Wire Line
	2500 2800 2500 1450
Connection ~ 2500 1450
Wire Wire Line
	3500 3600 3800 3600
Wire Wire Line
	3800 3600 3800 3100
Wire Wire Line
	5150 2700 5150 1450
Wire Wire Line
	5150 1450 5200 1450
Connection ~ 5200 1450
Wire Wire Line
	5350 2700 5350 1850
Wire Wire Line
	3800 3100 4850 3100
Wire Wire Line
	2300 6900 8900 6900
Connection ~ 5500 6900
Wire Wire Line
	5250 3700 5250 3800
Wire Wire Line
	5250 3800 4000 3800
Wire Wire Line
	4000 3800 4000 6900
Connection ~ 4000 6900
Wire Wire Line
	3000 5400 3000 6900
Connection ~ 3000 6900
Wire Wire Line
	5200 4400 7200 4400
Wire Wire Line
	7200 4400 7200 1850
Connection ~ 7200 1850
Connection ~ 5500 4400
Wire Wire Line
	5200 5500 5500 5500
Wire Wire Line
	5200 5500 5200 6900
Connection ~ 5200 6900
Wire Wire Line
	5900 4800 6900 4800
Wire Wire Line
	1200 4300 1700 4300
Wire Wire Line
	5900 4900 6600 4900
Wire Wire Line
	1400 4100 1700 4100
Wire Wire Line
	1700 4000 1500 4000
Wire Wire Line
	1500 4000 1500 5800
Wire Wire Line
	1500 5800 5900 5800
Wire Wire Line
	5900 5800 5900 5100
Wire Wire Line
	5900 5000 6200 5000
Wire Wire Line
	6200 5000 6200 6000
Wire Wire Line
	6200 6000 1600 6000
Wire Wire Line
	1600 6000 1600 4200
Wire Wire Line
	1600 4200 1700 4200
Wire Wire Line
	6600 4900 6600 6200
Wire Wire Line
	6600 6200 1400 6200
Wire Wire Line
	1400 6200 1400 4100
Wire Wire Line
	6900 4800 6900 6500
Wire Wire Line
	6900 6500 1200 6500
Wire Wire Line
	1200 6500 1200 4300
Wire Wire Line
	4700 4600 4400 4600
Wire Wire Line
	4400 4600 4400 5700
Wire Wire Line
	4400 5700 7800 5700
Wire Wire Line
	8300 1850 8300 5100
Connection ~ 8300 1850
Connection ~ 8200 6900
Wire Wire Line
	8300 5100 8450 5100
Wire Wire Line
	8200 6900 8200 5150
Wire Wire Line
	8200 5150 8450 5150
Wire Wire Line
	8450 5050 7800 5050
Wire Wire Line
	7800 5050 7800 5700
$Comp
L Neopixel U?
U 1 1 5E9C094D
P 8850 3350
F 0 "U?" H 8850 3350 60  0000 C CNN
F 1 "Neopixel" H 8850 3350 414 0000 C CNN
F 2 "" H 8850 3350 60  0001 C CNN
F 3 "" H 8850 3350 60  0001 C CNN
	1    8850 3350
	1    0    0    -1  
$EndComp
Wire Wire Line
	7400 4150 7400 1850
Connection ~ 7400 1850
Wire Wire Line
	7400 4250 7300 4250
Wire Wire Line
	7300 4250 7300 6900
Connection ~ 7300 6900
Wire Wire Line
	7400 4350 7400 4600
Wire Wire Line
	7400 4600 6900 4600
Wire Wire Line
	6900 4600 6900 3100
Wire Wire Line
	6900 3100 5650 3100
Text Notes 9550 950  2    138  ~ 28
Raspberry Pi 3 B+ with XC3738 Presssure Sensor and 24 x LED Neopixel Ring
$EndSCHEMATC
