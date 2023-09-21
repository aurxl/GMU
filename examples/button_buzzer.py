#!/#!/usr/bin/python

import RPi.GPIO as GPIO
import time

#definiere Pins
button_pin = 37
buzzer_pin = 12

#setze Board Modus zu GPIO.BOARD
GPIO.setmode(GPIO.BOARD)

#lege button_pin als Eingang und buzzer_pin als Ausgang fest
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buzzer_pin, GPIO.OUT)

try:
    while True:
        #ueberpruefe ob Knopf gedrueckt wird
        if(GPIO.input(button_pin) == 0):
            #Buzzer ein
            GPIO.output(buzzer_pin, GPIO.HIGH)
        else:
            #Buzzer aus
            GPIO.output(buzzer_pin, GPIO.LOW)

except KeyboardInterrupt:
    GPIO.cleanup()