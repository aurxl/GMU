#!/usr/bin/python

import RPi.GPIO as GPIO
import time

# sound_pin wird definiert
sound_pin = 18
# GPIO mode wird auf GPIO.BOARD gesetzt
GPIO.setmode(GPIO.BOARD)
# sound_pin wird als Eingang festgelegt
GPIO.setup(sound_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        # ueberpruefe ob ein Geraeusch erkannt wird
        if(GPIO.input(sound_pin)==GPIO.LOW):
            print('Sound erkannt')
            time.sleep(0.1)
except KeyboardInterrupt:
    # Strg+c beendet das Programm
    GPIO.cleanup()
