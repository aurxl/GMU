#!/usr/bin/python

import time
import RPi.GPIO as GPIO

#definiere LED Pin
led_pin = 37

#setze GPIO Modus auf GPIO.BOARD	
GPIO.setmode(GPIO.BOARD)
#lege Pin als Ausgang fest
GPIO.setup(led_pin, GPIO.OUT)

try:
	while True:
		#LED an
		GPIO.output(led_pin, GPIO.HIGH)
		#warte 0,2 Sekunden
		time.sleep(0.2)
		#LED aus
		GPIO.output(led_pin, GPIO.LOW)
		#warte 0,2 Sekunden
		time.sleep(0.2)

except KeyboardInterrupt:
	#STRG+C zum Beenden des Programms
	GPIO.cleanup()
