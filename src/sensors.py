#!/bin/env python
import RPi.GPIO as GPIO
import dht11
import time


class sensor:
    def __init__(self, pin: int = 4):
        self.pin = pin
        self.temp = 0.0
        self.hum = 0.0
        self.instance = dht11.DHT11(pin=self.pin)

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.cleanup()

    def update(self, timeout: int = 2) -> bool:
        result = self.instance.read()
        timeout = time.time() + timeout

        while not result.is_valid() and time.time() < timeout:
            result = self.instance.read()
            if result.is_valid():
                break
            else:
                return False

        self.temp = result.temperature
        self.hum = result.humidity
        return True

    def humidity(self) -> float:
        return float(self.hum)

    def temperature(self) -> float:
        return float(self.temp)
