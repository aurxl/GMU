#!/usr/bin/python

import time
import RPi.GPIO as GPIO

#tilt_pin wird definiert
tilt_pin = 15

#GPIO Modus wird auf GPIO.BOARD gesetzt
GPIO.setmode(GPIO.BOARD)

# Pin wird als Eingang festgelegt
GPIO.setup(tilt_pin, GPIO.IN)

try:
	while True:
		#positiv ist nach rechts, negativ ist nach links geneigt
		if GPIO.input(tilt_pin):
			print ("[-] Left Tilt")
		else:
			print ("[-] Right Tilt")
		time.sleep(1)
except KeyboardInterrupt:
	#Strg+c beendet das Programm
	GPIO.cleanup()
