#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author : Original author WindVoiceVox
# Original Author Github: https://github.com/WindVoiceVox/Raspi_SG90
import RPi.GPIO as GPIO
import time
import sys

class sg90:
  def __init__( self, pin, direction ): 
    GPIO.setmode( GPIO.BOARD )
    GPIO.setup( pin, GPIO.OUT )
    self.pin = int( pin )
    self.direction = int( direction )
    self.servo = GPIO.PWM( self.pin, 50 )
    self.servo.start(0.0)
  def cleanup( self ): #Funktion zum Stoppen und GPIO Pins Freigeben

    self.servo.ChangeDutyCycle(self._henkan(0))
    time.sleep(0.3)
    self.servo.stop()
    GPIO.cleanup()

  def currentdirection( self ): #Funktion die die Momentane Position feststellt.

    return self.direction

  def _henkan( self, value ):

    return 0.05 * value + 7.0

  def setdirection( self, direction, speed ): #Funktion um die Richtung anzugeben

    for d in range( self.direction, direction, int(speed) ):
      self.servo.ChangeDutyCycle( self._henkan( d ) )
      self.direction = d
      time.sleep(0.1)
    self.servo.ChangeDutyCycle( self._henkan( direction ) )
    self.direction = direction

def main():
    servo_pin = 22
    s = sg90(servo_pin,0) #Deklaration von Pin und Motor
    try:
        while True:
            print ("Turn left ...")
            s.setdirection( 100, 10 )   #Links Herum drehen
            time.sleep(0.5)             #0,5 Sekunden warten
            print ("Turn right ...")
            s.setdirection( -100, -10 ) #Rechts Herum drehen
            time.sleep(0.5)             #0,5 Sekunden warten
    except KeyboardInterrupt:
        s.cleanup()

if __name__ == "__main__":
    main()
