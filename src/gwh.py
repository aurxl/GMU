#!/bin/env python
#from sensors import sensor
#from output import out_lcd, out_segment
import argparse
import time

DESCRIPTION = ""
EXAMPLE = ""
PROG = "python3 gwh.py"

def parse_args():
    parser = argparse.ArgumentParser(
        prog = PROG,
        description=DESCRIPTION,
        epilog=EXAMPLE,
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('-l', '--loop', help="running forever", dest='LOOP', action='store_true')
    parser.add_argument('-i', '--iterations', help=" (int)", dest='ITER',)
    parser.add_argument('-L', '--lcd', help="output to LCD Monitor", dest='LCD', action='store_true')
    parser.add_argument('-s', '--segment', help="output to the 7-Segment Display", dest='SEGMENT', action='store_true')
    parser.add_argument('-H', '--hum', help="check hum level", dest='HUM', action='store_true')
    parser.add_argument('-t', '--temp', help="check temp level", dest='TEMP', action='store_true')
    parser.add_argument('-u', '--update-time', help="time in seconds between each update", dest='UPDATETIME')
    #parser.add_argument('-', '--', help="", dest='LCD', action='store_true')
    return parser.parse_args()


def main(env_sensor = False, lcd = False, segment = False, hum = False, temp = False) -> None:
    hum_str = ""
    temp_str = ""
    line_break = ""

    try:
        if env_sensor: env_sensor.update(5)
        print("_")
        if hum: hum_str = f"Temp: {env_sensor.humidity()}C"
        if temp: temp_str = f"Hum :{env_sensor.temperature()}%"
        if hum and temp: line_break = "\n"

        if lcd: lcd.msg(hum_str + line_break + temp_str)
        if segment:
            if hum and segment.type != "hum":
                segment.show(f"{env_sensor.temperature()}")
                segment.shown_type = "hum"
            else:
                segment.show(f"{env_sensor.temperature()}")
                segment.shown_type = "temp"

    except KeyboardInterrupt:
        print("stopping ... ")
        if lcd: lcd.stop()
        if segment: segment.stop()
        exit(0)


if __name__ == "__main__":
    args = parse_args()
    iterations = 1
    env_sensor = False
    lcd = False
    segment = False
    update_time = 1

    """checking user args and setting options"""
    if args.ITER:
        iterations = int(args.ITER)

    if args.HUM or args.TEMP:
        # initialize sensor class
        env_sensor = sensor(pin=4)

    if args.LCD:
         # initialize lcd output
        lcd = out_lcd()

    if args.SEGMENT:
        # initialize 7-Segment output
        segment = out_segment()
    
    if args.UPDATETIME:
        update_time = float(args.UPDATETIME)

    try:
        if args.LOOP:
            while True:
                main(env_sensor=env_sensor, lcd=lcd, segment=segment)
                time.sleep(update_time)
        else:
            for _ in range(iterations):
                main(env_sensor=env_sensor, lcd=lcd, segment=segment)
                time.sleep(update_time)

    except KeyboardInterrupt:
        print("stopping ... ")
        if lcd: lcd.stop()
        if segment: segment.stop()
        exit(0)
