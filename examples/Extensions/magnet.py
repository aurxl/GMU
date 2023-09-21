#!/usr/bin/python
# coding=utf-8
 
#############################################################################################################
### Copyright by Joy-IT
### Published under Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License
### Commercial use only after permission is requested and granted
###
### KY-053 Analog Digital Converter - Raspberry Pi Python Code Example
###
#############################################################################################################
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

# Create single-ended input on channels
chan0 = AnalogIn(ads, ADS.P0)

delayTime = 1
Digital_PIN = 5 #GPIO 5 (Pin29)

GPIO.setup(Digital_PIN, GPIO.IN, pull_up_down = GPIO.PUD_OFF)

while True:
                analog = '%.2f' % chan0.voltage
 
                # Ausgabe auf die Konsole
                if GPIO.input(Digital_PIN) == False:
                        print ("Analog Voltage:", analog,"V, ","Limit not reached")
                else:
                        print ("Analog Voltage:", analog, "V, ", "Limit reached")
                print ("---------------------------------------")
 
                # Reset + Delay
                button_pressed = False
                time.sleep(delayTime)