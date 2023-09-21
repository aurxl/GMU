#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import datetime

from Adafruit_LED_Backpack import SevenSegment


segment = SevenSegment.SevenSegment(address=0x70) #segment der I2C Adresse 0x70 und die Displaydefinition zuweisen

segment.begin() # Initialisierung des Displays. Muss einmal ausgeführt werden bevor das Display benutzt wird.

print ("STRG+C Druecken zum beenden.") #print Befehl für Ausgabe zum beenden des Scriptes

#Schleife welche dauerhaft die Zeit updated und sie auf dem Display anzeigt.
try:
  while(True):
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    second = now.second

    segment.clear()
    # Anzeige für die Stunden.
    segment.set_digit(0, int(hour / 10))     # Zehnerzahlen
    segment.set_digit(1, hour % 10)          # Einerzahlen
    # Anzeige für die Minuten.
    segment.set_digit(2, int(minute / 10))   # Zehnerzahlen
    segment.set_digit(3, minute % 10)        # Einerzahlen
    
    segment.set_colon(second % 2)              

    segment.write_display() # Wird benötigt um die Display LEDs zu updaten.

    time.sleep(1) # Warte eine Sekunde
except KeyboardInterrupt:
    segment.clear()
    segment.write_display()
