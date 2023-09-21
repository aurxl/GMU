#!/usr/bin/python

import RPi.GPIO as GPIO
import time

# definiere relay pin
relay_pin = 40

# Board Modus GPIO.BOARD
GPIO.setmode(GPIO.BOARD)
# relay_pin als Ausgang
GPIO.setup(relay_pin, GPIO.OUT)

# Oeffne Relais
GPIO.output(relay_pin, GPIO.LOW)
# warte eine halbe Sekunde
time.sleep(0.5)
# schliesse Relais
GPIO.output(relay_pin, GPIO.HIGH)
GPIO.cleanup()
