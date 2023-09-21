#!/usr/bin/env python
# -*- coding: utf-8 -*-


from RPi import GPIO	# Bibliotheken einfügen
import signal			

TOUCH = 11				# TOUCH pin 11 zuweisen (Variablendeklaration).

def setup_gpio():		# Funktion setup_gpio erstellen
    GPIO.setmode(GPIO.BOARD)	# Benutze GPIO Pins nach GPIO Board Schema.
    GPIO.setup(TOUCH, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def do_smt(channel):
    print("Touch wurde erkannt")

def main():
    setup_gpio()
    try:
        GPIO.add_event_detect(TOUCH, GPIO.FALLING, callback=do_smt, bouncetime=200)
        signal.pause()
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()
