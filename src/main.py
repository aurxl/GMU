#!/bin/env python
from sensors import sensor


if __name__ == "__main__":
    # initialize sensor class
    env_sensor = sensor(pin=4)
    

    env_sensor.update()
    print(env_sensor.humidity(), env_sensor.temperature())
