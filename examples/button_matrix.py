#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author : original author stenobot
# Original Author Github: https://github.com/stenobot/SoundMatrixPi

import RPi.GPIO as GPIO
import time

class ButtonMatrix():

    def __init__(self):

        GPIO.setmode(GPIO.BOARD)

        # Die IDs der Buttons werden festgelegt
        self.buttonIDs = [[4,3,2,1],[8,7,6,5],[12,11,10,9],[16,15,14,13]]
        # GPIO Pins für die Zeilen werden deklariert.
        self.rowPins = [13,15,29,31]
        # GPIO Pins für die Spalte werden deklariert.
        self.columnPins = [33,35,37,22]

        # Definiere Vier Inputs mit pull up Widerständen.
        for i in range(len(self.rowPins)):
            GPIO.setup(self.rowPins[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)

        # Definiere Vier Outputs und setze sie auf high.
        for j in range(len(self.columnPins)):
            GPIO.setup(self.columnPins[j], GPIO.OUT)
            GPIO.output(self.columnPins[j], 1)

    def activateButton(self, rowPin, colPin):
        # Erhalte die Button Nummer
        btnIndex = self.buttonIDs[rowPin][colPin] - 1
        print("button " + str(btnIndex + 1) + " pressed")
        # Verhindert mehrere Knopfdrücke in zu kurzer zeit
        time.sleep(.3)

    def buttonHeldDown(self,pin):
        if(GPIO.input(self.rowPins[pin]) == 0):
            return True
        return False
		
def main():

    # Initialisierung der Button Matrix
    buttons = ButtonMatrix()
    try:
        while(True):
            for j in range(len(buttons.columnPins)):
                # Jeder Output Pin wird auf low gesetzt.
                GPIO.output(buttons.columnPins[j],0)
                for i in range(len(buttons.rowPins)):
                    if GPIO.input(buttons.rowPins[i]) == 0:
                        buttons.activateButton(i,j)
                        # Nichts tun solange der Button gedrückt gehalten wird.
                        while(buttons.buttonHeldDown(i)):
                            pass
                GPIO.output(buttons.columnPins[j],1)
    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
