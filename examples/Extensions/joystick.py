import matplotlib.pyplot as plt
import numpy as np
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

Button_PIN = 6
GPIO.setup(Button_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)
ads.gain = 2/3
# Create single-ended input on channels
chan0 = AnalogIn(ads, ADS.P0)
chan1 = AnalogIn(ads, ADS.P1)

x = np.linspace(0, 6*np.pi, 100)
y = np.sin(x)

# You probably won't need this if you're embedding things in a tkinter plot...
plt.ion()

fig = plt.figure()
ax = fig.add_subplot(111)
#line1, = ax.plot(x, y, 'r-') # Returns a tuple of line objects, thus the comma

for phase in np.linspace(0, 10*np.pi, 500):
    plt.cla()
    plt.xlim(0, 3.3)
    plt.ylim(3.3, 0)
    plt.xlabel("Voltage X")
    plt.ylabel("Voltage Y")
    if GPIO.input(Button_PIN) == False:
        plt.title("Button pressed!")

    plt.plot(chan0.voltage,chan1.voltage,'ro') 
    fig.canvas.draw()
    fig.canvas.flush_events()