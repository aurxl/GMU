import RPi.GPIO as GPIO
import dht11

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# read data using pin 14
instance = dht11.DHT11(pin = 4)
result = instance.read()

while not result.is_valid():  # read until valid values
    result = instance.read()

print("Temperature: %-3.1f C" % result.temperature)
print("Humidity: %-3.1f %%" % result.humidity)
