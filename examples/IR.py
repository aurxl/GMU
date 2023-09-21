#!/usr/bin/env python3
"""IRModuleExample1, program to practice using the IRModule
Created Apr 30, 2018"""

"""
Copyright 2018 Owain Martin
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import RPi.GPIO as GPIO
import IRModule
import time

def remote_callback(code):        

    # Codes listed below are for the
    # Sparkfun 9 button remote

    if code == 0xffa25d:
        print("KEY_CH-")
    elif code == 0xff629d:
        print('KEY_CH')
    elif code == 0xffe21d:
        print('KEY_CH+')
    elif code == 0xff22dd:
        print('KEY_PREV')
    elif code == 0xff02fd:
        print('KEY_NEXT')
    elif code == 0xffc23d:
        print('KEY_PLAY/PAUSE')
    elif code == 0xffe01f:
        print('KEY_VOL-')
    elif code == 0xffa857:
        print('KEY_VOL+')
    elif code == 0xff906f:
        print('KEY_EQ')
    elif code == 0xff6897:
        print('KEY_0')
    elif code == 0xff9867:
        print('KEY_100+')
    elif code == 0xffb04f:
        print('KEY_200+')
    elif code == 0xff30cf:
        print('KEY_1')
    elif code == 0xff18e7:
        print('KEY_2')
    elif code == 0xff7a85:
        print('KEY_3')
    elif code == 0xff10ef:
        print('KEY_4')
    elif code == 0xff38c7:
        print('KEY_5')
    elif code == 0xff5aa5:
        print('KEY_6')
    elif code == 0xff42bd:
        print('KEY_7')
    elif code == 0xff4ab5:
        print('KEY_8')
    elif code == 0xff52ad:
        print('KEY_9')

    return

# set up IR pi pin and IR remote object
irPin = 20
ir = IRModule.IRRemote(callback='DECODE')
# using 'DECODE' option for callback will print out
# the IR code received in hexadecimal
# this can used to get the codes for whichever NEC
# compatable remote you are using

# set up GPIO options and set callback function required
# by the IR remote module (ir.pWidth)        
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)      # uses numbering outside circles
GPIO.setup(irPin,GPIO.IN)   # set irPin to input
GPIO.add_event_detect(irPin,GPIO.BOTH,callback=ir.pWidth)

ir.set_verbose() # verbose option prints outs high and low width durations (ms)
print('Starting IR remote sensing using DECODE function and verbose setting equal True ')
print('Use ctrl-c to exit program')

try:    
    #time.sleep(5)

    # turn off verbose option and change callback function
    # to the function created above - remote_callback()
    print('Turning off verbose setting and setting up callback')
    ir.set_verbose(False)
    ir.set_callback(remote_callback)

    # This is where you could do other stuff
    # Blink a light, turn a motor, run a webserver
    # count sheep or mine bitcoin
    
    while True:
        time.sleep(1)

except:
    print('Removing callback and cleaning up GPIO')
    ir.remove_callback()
    GPIO.cleanup(irPin)