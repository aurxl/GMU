#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author : Original author ludwigschuster
# Original Author Github: https://github.com/ludwigschuster/RasPi-GPIO-Stepmotor

import time
import RPi.GPIO as GPIO
import math

class Stepmotor:

    def __init__(self):
        # GPIO modus Festlegen
        GPIO.setmode(GPIO.BOARD)
        # Das Sind die Pins Ihres RasperryPis die benutzt werden.
        self.pin_A = 29
        self.pin_B = 31
        self.pin_C = 33
        self.pin_D = 35
        self.interval = 0.010
        
        # Pins als Output Deklarieren
        GPIO.setup(self.pin_A,GPIO.OUT)
        GPIO.setup(self.pin_B,GPIO.OUT)
        GPIO.setup(self.pin_C,GPIO.OUT)
        GPIO.setup(self.pin_D,GPIO.OUT)
        GPIO.output(self.pin_A, False)
        GPIO.output(self.pin_B, False)
        GPIO.output(self.pin_C, False)
        GPIO.output(self.pin_D, False)

    def Step1(self):

        GPIO.output(self.pin_D, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_D, False)

    def Step2(self):
        
        GPIO.output(self.pin_D, True)
        GPIO.output(self.pin_C, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_D, False)
        GPIO.output(self.pin_C, False)

    def Step3(self):

        GPIO.output(self.pin_C, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_C, False)

    def Step4(self):

        GPIO.output(self.pin_B, True)
        GPIO.output(self.pin_C, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_B, False)
        GPIO.output(self.pin_C, False)

    def Step5(self):

        GPIO.output(self.pin_B, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_B, False)

    def Step6(self):

        GPIO.output(self.pin_A, True)
        GPIO.output(self.pin_B, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_A, False)
        GPIO.output(self.pin_B, False)

    def Step7(self):

        GPIO.output(self.pin_A, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_A, False)

    def Step8(self):

        GPIO.output(self.pin_D, True)
        GPIO.output(self.pin_A, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_D, False)
        GPIO.output(self.pin_A, False)

    def turn(self,count):
        for i in range (int(count)):
            self.Step1()
            self.Step2()
            self.Step3()
            self.Step4()
            self.Step5()
            self.Step6()
            self.Step7()
            self.Step8()

    def close(self):
        # Die GPIO Pins fuer andere Aktivitaeten freigeben.
        GPIO.cleanup()

    def turnSteps(self, count):
        # Bewegen um n schritte
        # (n wird von Ihnen festgelegt.)
        for i in range (count):
            self.turn(1)

    def turnDegrees(self, count):
        # Bewegen um n Grad (Kleine Werte koennen zu Ungenauigkeit fuehren.)
        # (Gradnummer die gedreht werden soll angeben.)
        self.turn(round(count*512/360,0))

    def turnDistance(self, dist, rad):
        self.turn(round(512*dist/(2*math.pi*rad),0))

def main():

    print("Bewegung gestartet.")
    motor = Stepmotor()
    print("Ein Schritt")
    motor.turnSteps(1)
    time.sleep(0.5)
    print("20 Schritte")
    motor.turnSteps(20)
    time.sleep(0.5)
    print("Viertel Umdrehung")
    motor.turnDegrees(90)
    print("Bewegung gestoppt.")
    motor.close()

if __name__ == "__main__":
    main()
