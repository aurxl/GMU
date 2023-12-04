#!/bin/env python
from sensors import sensor
import time

if __name__ == "__main__":
    # initialize sensor class
    env_sensor = sensor(pin=4)
    

    print(env_sensor.update(5))
    print(env_sensor.humidity(), env_sensor.temperature())
