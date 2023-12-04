#!/bin/env python
from sensors import sensor
from output import out_lcd, out_segment
import time

if __name__ == "__main__":
    # initialize sensor class
    env_sensor = sensor(pin=4)

    # initialize lcd and 7-Segment output
    lcd = out_lcd()
    segment = out_segment()

    while True:
        try:
            env_sensor.update(5)
            
            # print(f"Temp: {env_sensor.temperature()}C \nHum : {env_sensor.humidity()}%")
            lcd.msg(f"Temp: {env_sensor.temperature()}C \nHum : {env_sensor.humidity()}%")
            segment.show(f"{env_sensor.temperature()}")

            time.sleep(1)
        except KeyboardInterrupt:
            print("stopping ... ")
            lcd.stop()
            segment.stop()
            exit(0)
