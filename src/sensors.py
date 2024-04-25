#!/bin/env python
import RPi.GPIO as GPIO
import dht11
import time
import smbus 


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
            self.GPIO.cleanup()
        except Exception as exc:
            print(exc)
            return False


class BH1750():
    """class defining the bh1750 light sensor

    """
    def __init__(self):
        # class attr and func copied and from JoyPi example

        #define some constants from the datasheet
        self.DEVICE = 0x5c #default device I2C address
        self.POWER_DOWN = 0x00 #no active state
        self.POWER_ON = 0x01 #power on
        self.RESET = 0x07 #reset data register value
        #start measurement at 4 Lux
        self.CONTINUOUS_LOW_RES_MODE = 0x13
        #start measurement at 1 Lux
        self.CONTINUOUS_HIGH_RES_MODE_1 = 0x10
        #start measurement at 0.5 Lux
        self.CONTINUOUS_HIGH_RES_MODE_2 = 0x11
        #start measurement at 1 Lux
        #device is automatically set to power down mode after measurement
        self.ONE_TIME_HIGH_RES_MODE_1 = 0x20
        #start measurement at 0.5 Lux
        #device is automatically set to power down mode after measurement
        self.ONE_TIME_HIGH_RES_MODE_2 = 0x21
        #start measurement at 4 Lux
        #device is automatically set to power down mode after measurement
        self.ONE_TIME_LOW_RES_MODE = 0x23

        self.bus = smbus.SMBus(1)
    
    def convertToNumber(self, data):
        #Simple function to convert 2 Bytes of data
        #into a decimal number
        return ((data[1] + (256 * data[0])) / 1.2)
    
    def read(self):
        data = self.bus.read_i2c_block_data(self.DEVICE,self.ONE_TIME_HIGH_RES_MODE_1)
        return self.convertToNumber(data)
