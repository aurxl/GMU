#!/bin/env python
import RPi.GPIO as GPIO
import sensors
import time


class sensor:
    def __init__(self, pin: int = 4):
        self.pin = pin
        self.temp = 0
        self.hum = 0
        self.instance = sensors.DHT11(pin=self.pin)

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.cleanup()

    def update(self, timeout: int = 2) -> bool:
        result = self.instance.read()

        timeout = time.time() + self.timeout
        while not result.is_valid() and time.time() < timeout:
            result = self.instance.read()
            if result.is_valid():
                break
        else:
            return False

        self.temp = result.temperature
        self.hum = result.humidity
        return True

    def humidity(self) -> int:
        return int(self.temp)

    def temperature(self) -> int:
        return int(self.hum)
