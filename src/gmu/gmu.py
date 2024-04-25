#!/bin/env python
from sensors import DHT11, BH1750
from output import Lcd, Segment, Matrix, Status8x8, Relay
import datetime 
import argparse
import time
import signal


DESCRIPTION = "Greenhouse Monitoring Utilty v1.6"
EXAMPLE = "gmu.py --loop --segment --lcd --matrix --hum --temp --light --relay -u 4"
PROG = "python3 gwh.py"

# those are just some low values for showcase
LX_MAX = 12000
LX_MID = 7000
LX_MIN = 4000

# times in wich the light house should be illuminated
DAY_START = datetime.time(hour=6)
DAY_END = datetime.time(hour=22)

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
    parser.add_argument('-li', '--light', help="light level in lx", dest='LIGHT', action='store_true')
    parser.add_argument('-u', '--update-time', help="time in seconds between each update", dest='UPDATETIME')
    parser.add_argument('-S', '--service-mode', help="when starting this program as systemd service to handle SIGTERM", dest='SERVICEMODE', action='store_true')
    parser.add_argument('-r', '--relay', help="Controling the relay based on current time and light level", dest='RELAY', action='store_true')
    return parser.parse_args()


def stop(lcd, segment, env_sensor, matrix):
    print("stopping ... ")
    if lcd: lcd.stop()
    if segment: segment.stop()
    if env_sensor: env_sensor.stop()
    if matrix: matrix.stop()
    exit(0)


def main(
            env_sensor = False,
            light_sensor = False,
            lcd = False,
            segment = False,
            matrix=False,
            relay=False,
            hum = False,
            temp = False
        ) -> None:
    """main func merging all the parts together"""
    hum_str = ""
    temp_str = ""
    line_break = ""
    light = 0
    light_status = None

    try:
        # gather data when option is defined
        if env_sensor: env_sensor.update(5)
        if light_sensor:
            light = light_sensor.read()
            if LX_MID <= light <= LX_MAX:
                light_status = Status8x8.GOOD
            elif LX_MIN <= light <= LX_MID:
                light_status = Status8x8.MID
            else:
                light_status = Status8x8.BAD
            
        # preparing strings to be shown on lcd
        if hum: hum_str = f"Hum :{int(env_sensor.humidity())}%"
        if temp: temp_str = f"Temp:{int(env_sensor.temperature())}C"
        if hum and temp: line_break = "\n"

        # setting faces on matrix based on light level
        if matrix:
            if light > 0:
                matrix.loading(on=False)
                matrix.show(status = light_status)
            else:
                matrix.loading(on=True)

        # show loading on matrix while values arent valid
        if ((hum == 0 and temp == 0) and matrix) and matrix:
            matrix.loading(on=True)
        elif matrix:
            matrix.loading(on=False)

        # building string and show on lcd
        if lcd: lcd.msg(f"{hum_str}{line_break}{temp_str}")
        if segment:
            # check currently shown value type at segment display
            # and switch to that other type to display
            if hum and segment.shown_type != "hum":
                segment.show(f"{int(env_sensor.humidity())}F")
                segment.shown_type = "hum"
            elif temp and segment.shown_type != "temp":
                segment.show(f"{int(env_sensor.temperature())}C")
                segment.shown_type = "temp"
        
        # Open Relay based in current light level and datetime
        if relay:
            curr_hour = datetime.time().hour()
            if (DAY_START < curr_hour < DAY_END) and light_sensor == Status8x8.BAD:
                relay.open()
            else:
                relay.close()


    except KeyboardInterrupt:
        # stop program nicely when Keyboard interrupts (^C)
        stop(lcd, segment, env_sensor, matrix)


if __name__ == "__main__":
    # init args / read args
    args = parse_args()

    # define some default vars that
    # will may be overitten by args
    iterations = 1
    update_time = 2
    lcd = False
    segment = False
    env_sensor = False
    light_sensor = False
    matrix = False
    relay = False

    # checking user args and
    # init objects based on them

    if args.LCD:
        # initialize lcd output
        lcd = Lcd()

    if args.SEGMENT:
        # initialize 7-Segment output
        segment = Segment()

    if args.MATRIX:
        matrix = Matrix()

    if args.ITER:
        iterations = int(args.ITER)

    if args.HUM or args.TEMP:
        # initialize sensor class
        env_sensor = DHT11(pin=4)
    
    if args.LIGHT:
        light_sensor = BH1750()
    
    if args.SERVICEMODE:
        # init our signal handler
        SignalHandler(lcd=lcd, segment=segment, env_sensor=env_sensor)

    if args.UPDATETIME:
        update_time = float(args.UPDATETIME)

    if args.RELAY:
        relay = Relay()


    try:
        """
        when user wants to run the program forever (--loop)
        start while loop otherwise iterate for given (--iteration)
        number
        """
        print("starting GMU!")
        if args.LOOP:
            while True:
                main(
                        env_sensor=env_sensor,
                        light_sensor=light_sensor,
                        lcd=lcd, segment=segment,
                        matrix=matrix,
                        hum=args.HUM,
                        temp=args.TEMP
                    )
                time.sleep(update_time)
        else:
            for _ in range(iterations):
                main(
                        env_sensor=env_sensor,
                        light_sensor=light_sensor,
                        lcd=lcd, segment=segment,
                        matrix=matrix,

                        hum=args.HUM,
                        temp=args.TEMP
                    )
                time.sleep(update_time)

    except KeyboardInterrupt:
        # stop program nicely when Keyboard interrupts (^C)
        print("Keyboard  Interrupt ... trying to stop ")
        stop(lcd, segment, env_sensor, matrix)

    stop(lcd, segment, env_sensor, matrix)
