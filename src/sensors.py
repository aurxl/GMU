#!/bin/env python
import RPi.GPIO as GPIO
import dht11
import time


class DHT11:
    """
    DHT11 class defining DHT11 sensor
    and holding current values
    """
    def __init__(self, pin: int = 4):
        self.pin = pin
        self.temp = 0.0
        self.hum = 0.0
        self.instance = dht11.DHT11(pin=self.pin)

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        # GPIO.cleanup()

    def update(self, timeout: int = 2) -> bool:
        """func for 'pulling'/ updating the current values
        
        Timeout defines the max time in sec. to wait for
        valid values from the dht11 sensor.
        """
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
        """return class holded humidity value"""
        return float(self.hum)

    def temperature(self) -> float:
        """return class holded temperature value"""
        return float(self.temp)

    def stop(self) -> bool:
        try:
            GPIO.cleanup()
        except Exception as exc:
            print(exc)
            return False
