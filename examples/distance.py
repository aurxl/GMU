#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author : www.modmypi.com
# Link: https://www.modmypi.com/blog/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD) # Setze die GPIO Boardkonfiguration ein.

TRIG = 36    # Variablendeklaration 
ECHO = 32    # Variablendeklaration

print ("Entfernung wird ermittelt.") # Ausgabe von Text in der Konsole

GPIO.setup(TRIG,GPIO.OUT) # Variable TRIG als Output festlegen.
GPIO.setup(ECHO,GPIO.IN)  # Variable ECHO als Input festlegen.

GPIO.output(TRIG, False)
print ("Warte auf den Sensor.")
time.sleep(2) # 2 Sekunden Wartezeit.

GPIO.output(TRIG, True)  # Sendet ein Ultraschallsignal
time.sleep(0.00001)      # Wartet 0,00001 Sekunden
GPIO.output(TRIG, False) # Beendet das senden des Ultraschallsignals

while GPIO.input(ECHO)==0:
  pulse_start = time.time()

while GPIO.input(ECHO)==1:
  pulse_end = time.time()

pulse_duration = pulse_end - pulse_start # Berechnung für die Dauer Des Pulses

distance = pulse_duration * 17150  # Berechnung zur Bestimmung der Entfernung.

distance = round(distance, 2)      # Ergebnis wird auf 2 Nachkommastellen gerundet.

print ("Distance:",distance,"cm")    # Konsolenausgabe der Distanz in cm.

GPIO.cleanup() # Gibt GPIO Ports wieder frei.
