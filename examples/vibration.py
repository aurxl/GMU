#!/usr/bin/python

import RPi.GPIO as GPIO
import time

# definieren des Vibrationspins
vibration_pin = 13

# setze Boardmodus zu GPIO.BOARD
GPIO.setmode(GPIO.BOARD)

# lege Vibrationspin als Ausgang fest
GPIO.setup(vibration_pin, GPIO.OUT)

# schalte Vibration ein
GPIO.output(vibration_pin, GPIO.HIGH)
# warte eine Sekunde
time.sleep(1)
# schalte Vibration aus
GPIO.output(vibration_pin, GPIO.LOW)

GPIO.cleanup()
