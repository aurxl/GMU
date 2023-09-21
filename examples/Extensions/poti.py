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
import RPi.GPIO as GPIO 
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
led_pin = 13                 # LED Pin
V_Limit = 2.5				 # Voltage limit
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)
# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)
ads.gain = 2/3
# Create single-ended input on channels
chan0 = AnalogIn(ads, ADS.P0)
GPIO.output(led_pin, GPIO.LOW)


while True:
    if V_Limit > chan0.voltage:
      GPIO.output(led_pin, GPIO.LOW)
      print("Potentiometer Voltage: ","{:>5.3f}".format(chan0.voltage), "V / Limit reached!")
      print("---------------------------------------------------")
      time.sleep(1)
    else:
      GPIO.output(led_pin, GPIO.HIGH)
      print("Potentiometer Voltage: ","{:>5.3f}".format(chan0.voltage), "V / Limit not reached!")
      print("---------------------------------------------------")
      time.sleep(1)      