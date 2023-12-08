#!/bin/env python
from sensors import DHT11
from output import Lcd, Segment, Matrix, Status8x8
import argparse
import time
import signal


DESCRIPTION = ""
EXAMPLE = "gmu.py --hum --temp --lcd --segment -u 2 -l"
PROG = "python3 gwh.py"


class SignalHandler:
    """custom signal handler
    
    Especially when gmu is running as a systemd service,
    handling signals come in handy. When you want to
    manually stop the service eg. with `systemctl stop gmu`
    systemd is sending a SIGTERM signal to that process.
    With the build-in signal lib we can catch those signals
    and perform actions such as turning off the displays etc.

    Note: SIGKILL signals cant be catched by the process itself
    """
    def __init__(self, lcd, segment, env_sensor) -> None:
        signal.signal(signal.SIGTERM, self.sigterm_stop)
        self.lcd = lcd
        self.segment = segment
        self.env_sensor = env_sensor

    def sigterm_stop(self, _signo, _stack_frame):
        print("stopping ... ")
        if self.lcd: self.lcd.stop()
        if self.segment: self.segment.stop()
        if self.env_sensor: self.env_sensor.stop()
        exit(0)


def parse_args():
    """initialize argparse and setting some args"""
    parser = argparse.ArgumentParser(
        prog = PROG,
        description=DESCRIPTION,
        epilog=EXAMPLE,
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('-L', '--loop', help="running forever", dest='LOOP', action='store_true')
    parser.add_argument('-i', '--iterations', help=" (int)", dest='ITER',)
    parser.add_argument('-l', '--lcd', help="output to LCD Monitor", dest='LCD', action='store_true')
    parser.add_argument('-m', '--matrix', help="output to LED Matrix", dest='MATRIX', action='store_true')
    parser.add_argument('-s', '--segment', help="output to the 7-Segment Display", dest='SEGMENT', action='store_true')
    parser.add_argument('-H', '--hum', help="check hum level", dest='HUM', action='store_true')
    parser.add_argument('-t', '--temp', help="check temp level", dest='TEMP', action='store_true')
    parser.add_argument('-u', '--update-time', help="time in seconds between each update", dest='UPDATETIME')
    parser.add_argument('-S', '--service-mode', help="when starting this program as systemd service to handle SIGTERM", dest='SERVICEMODE', action='store_true')
    #parser.add_argument('-', '--', help="", dest='', action='store_true')
    return parser.parse_args()


def stop(lcd, segment, env_sensor, matrix):
    print("stopping ... ")
    if lcd: lcd.stop()
    if segment: segment.stop()
    if env_sensor: env_sensor.stop()
    if matrix: matrix.stop()
    exit(0)


def main(env_sensor = False, lcd = False, segment = False, matrix=False, hum = False, temp = False) -> None:
    """main func merging all the parts together"""
    hum_str = ""
    temp_str = ""
    line_break = ""

    try:
        if env_sensor: env_sensor.update(5)
        if hum: hum_str = f"Hum :{env_sensor.humidity()}%"
        if temp: temp_str = f"Temp:{env_sensor.temperature()}C"
        if hum and temp: line_break = "\n"

        if lcd: lcd.msg(f"{hum_str}{line_break}{temp_str}")
        if segment:
            if hum and segment.shown_type != "hum":
                segment.show(f"{env_sensor.humidity()}")
                segment.shown_type = "hum"
                matrix.show(Status8x8.GOOD)
            elif temp and segment.shown_type != "temp":
                segment.show(f"{env_sensor.temperature()}")
                segment.shown_type = "temp"
                matrix.show(Status8x8.BAD)

    except KeyboardInterrupt:
        # stop program nicely when Keyboard interrupts (^C)
        stop(lcd, segment, env_sensor, matrix)


if __name__ == "__main__":
    # init args
    args = parse_args()

    # define some default vars
    iterations = 1
    update_time = 1
    lcd = False
    segment = False
    env_sensor = False
    matrix = False

    # checking user args and setting options

    if args.LCD:
        # initialize lcd output
        lcd = Lcd()

    if args.SEGMENT:
        # initialize 7-Segment output
        segment = Segment()

    if args.MATRIX:
        matrix = Matrix()
        matrix.loading(on=True)
        time.sleep(5)
        matrix.loading(on=False)

    if args.ITER:
        iterations = int(args.ITER)

    if args.HUM or args.TEMP:
        # initialize sensor class
        env_sensor = DHT11(pin=4)
    
    if args.SERVICEMODE:
        # init our signal handler
        SignalHandler(lcd=lcd, segment=segment, env_sensor=env_sensor)

    if args.UPDATETIME:
        update_time = float(args.UPDATETIME)

    try:
        """
        when user wants to run the program forever (--loop)
        start while loop otherwise iterate for given (--iteration)
        number
        """
        print("starting GMU!")
        if args.LOOP:
            while True:
                main(env_sensor=env_sensor, lcd=lcd, segment=segment, matrix=matrix, hum=args.HUM, temp=args.TEMP)
                time.sleep(update_time)
        else:
            for _ in range(iterations):
                main(env_sensor=env_sensor, lcd=lcd, segment=segment, matrix=matrix, hum=args.HUM, temp=args.TEMP)
                time.sleep(update_time)

    except KeyboardInterrupt:
        # stop program nicely when Keyboard interrupts (^C)
        print("Keyboard  Interrupt ... trying to stop ")
        stop(lcd, segment, env_sensor, matrix)

    stop(lcd, segment, env_sensor, matrix)
