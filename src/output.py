#!/bin/env python
import time
import threading
from enum import unique, Enum
import board
import busio
import adafruit_character_lcd.character_lcd_i2c as c_lcd
from adafruit_ht16k33.segments import Seg7x4
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas

class Lcd():
    """class defining the lcd display"""
    def __init__(self):
        self.text = "hier könnte ihre Werbung stehen"
        self.columns = 16
        self.rows = 2
        #self.stop = self.stop()
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.lcd = c_lcd.Character_LCD_I2C(
            self.i2c,
            self.columns,
            self.rows,
            0x21
        )
        self.backlight(True)

    def backlight(self, on: bool = True) -> (bool, Exception):
        """turning backlight on"""
        try:
            if on:
                self.lcd.backlight = True
            else:
                self.lcd.backlight = False
            return True, None
        except Exception as exc:
            return False, exc

    def msg(self, text: str = "hello world", cursor: bool = False) -> (bool, Exception):
        """func for showing messages on the lcd display"""
        self.text = text
        self.lcd.clear()
        try:
            if cursor: self.lcd.cursor = True
            self.lcd.message = self.text
            return True, None
        except Exception as exc:
            return False, exc

    def scroll(self, text: str = "", speed: float = 0.5) -> (bool, Exception):
        """TODO: func for scrolling text at the lcd display"""
        if not text:
            text = self.text
        else:
            self.text = text

        try:
            self.lcd.clear()
            for i in range(len(text)):
                time.sleep(speed)
                self.lcd.move_right()
            for i in range(len(text)):
                time.sleep(speed)
                self.lcd.move_left()
            return True, None
        except Exception:
            return False, Exception

    def stop(self) -> (bool, Exception):
        """clearing screen and turning backlight off"""
        try:
            self.lcd.clear()
            self.backlight(False)
            return True, None
        except Exception as exc:
            return False, exc

class Segment():
    """class defining the 7-Segment Display"""
    def __init__(self):
        # self.segment = SevenSegment.SevenSegment(address=0x70)
        self.address = 0x70
        self.i2c = board.I2C()
        self.segment = Seg7x4(self.i2c, address=self.address)
        self.shown_type = None
        self.colon = False
        
        self.segment.fill(0)

    def show(self, chars: str = "0000", colon: bool = False) -> (str, bool):
        """showing given string on display

        When there are dots to be printed, some magic is required.
        Dots are at the same position as the number. To display e.g.
        '20.5' which are 4 characters, only 3 numbers from the 4 available
        places at the display are needed. The dot has to be at the
        same position as '0', at index 1. Therefor '5' can move one
        index before to 2. The colon is controlled individually btw.

        [].[].:[].[].  <- display
         0  1   2  3   <- Index
         2  0.  5      <- number
        """
        written_chars = ""
        dot_control = 0

        for i, c in enumerate(chars):
            ii = i  - dot_control
            try:
                if c == "." or c == ",":
                    self.segment[ii - 1] = "."
                    dot_control += 1
                else:
                    self.segment[ii] = c
                written_chars += c
                self.segment.show()
            except Exception as exc:
                print(exc)
                return written_chars, False
        return written_chars, True

    def stop(self) -> bool:
        """turning display off"""
        try:
            self.segment.fill(0)
            return True
        except Exception:
            return False


@unique
class Status8x8(Enum):
    SMILEYGOOD = [
        [1,1,0,0,0,0,1,1],
        [1,0,1,1,1,1,0,1],
        [0,1,0,1,1,0,1,0],
        [0,1,1,1,1,1,1,0],
        [0,1,0,1,1,0,1,0],
        [0,1,1,0,0,1,1,0],
        [1,0,1,1,1,1,0,1],
        [1,1,0,0,0,0,1,1]
    ]
    SMILEYBAD = [
        [1,1,0,0,0,0,1,1],
        [1,0,1,1,1,1,0,1],
        [0,1,0,1,1,0,1,0],
        [0,1,1,1,1,1,1,0],
        [0,1,1,1,1,1,1,0],
        [0,1,1,0,0,1,1,0],
        [1,0,0,1,1,0,0,1],
        [1,1,0,0,0,0,1,1]
    ]
    SMILEYMID = [
        [1,1,0,0,0,0,1,1],
        [1,0,1,1,1,1,0,1],
        [0,1,0,1,1,0,1,0],
        [0,1,1,1,1,1,1,0],
        [0,1,1,1,1,1,1,0],
        [0,1,0,0,0,0,1,0],
        [1,0,1,1,1,1,0,1],
        [1,1,0,0,0,0,1,1]
    ]
    MCGOOD = [
        [0,0,0,0,0,0,0,0],
        [0,1,1,1,1,1,1,0],
        [0,1,0,1,1,0,1,0],
        [0,1,1,1,1,1,1,0],
        [0,1,1,1,1,0,1,0],
        [0,1,1,0,0,1,1,0],
        [0,1,1,1,1,1,1,0],
        [0,0,0,0,0,0,0,0]
    ]
    MCBAD = [
        [1,1,0,0,0,0,1,1],
        [1,1,1,1,1,1,0,1],
        [0,1,0,1,1,0,1,0],
        [0,1,1,1,1,1,1,0],
        [0,1,1,1,1,1,1,0],
        [0,1,1,0,0,1,1,0],
        [1,0,0,1,1,0,0,1],
        [1,1,0,0,0,0,1,1]
    ]
    MCMID = [
        [1,1,0,0,0,0,1,1],
        [1,1,1,1,1,1,0,1],
        [0,1,0,1,1,0,1,0],
        [0,1,1,1,1,1,1,0],
        [0,1,1,1,1,1,1,0],
        [0,1,0,0,0,0,1,0],
        [1,0,1,1,1,1,0,1],
        [1,1,0,0,0,0,1,1]
    ]
    GOOD = [
        [1,1,1,1,1,1,1,1],
        [1,0,0,1,1,0,0,1],
        [1,0,0,1,1,0,0,1],
        [1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1],
        [1,1,0,1,1,0,1,1],
        [1,1,1,0,0,1,1,1],
        [1,1,1,1,1,1,1,1]
    ]
    BAD = [
        [1,1,1,1,1,1,1,1],
        [1,0,0,1,1,0,0,1],
        [1,1,0,1,1,0,1,1],
        [1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1],
        [1,1,1,0,0,1,1,1],
        [1,1,0,1,1,0,1,1],
        [1,1,1,1,1,1,1,1]
    ]
    MID = [
        [1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1],
        [1,0,0,1,1,0,0,1],
        [1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1],
        [1,1,0,0,0,0,1,1],
        [1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1]
    ]
    LOADING = [
        [
            [1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1],
            [1,1,0,1,1,1,1,1],
            [1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1]
        ],
        [
            [1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1],
            [1,1,1,0,1,1,1,1],
            [1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1]
        ],
        [
            [1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1],
            [1,1,1,1,0,1,1,1],
            [1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1]
        ]
    ]


class Matrix():
    def __init__(self, orientation = 0, rotation = 3, contrast = 20 ) -> None:
        self.serial = spi(port=0, device=1, gpio=noop())
        self.device = max7219(
            self.serial,
            cascaded=1,
            block_orientation=orientation,
            rotate=rotation
        )
        self.device.contrast(contrast)
        self._loading_on = False
        # self._current_status = None

    def show(self, status: Status8x8):
        self.device.show()
        self._current_status = status
        self._control_led_matrix(status.value)

    def stop(self):
        self.device.hide()
        self.device.cleanup()
    
    def loading(self, on: bool):
        if not on:
            self._loading_on = False
            return
        self._loading_on = True
        t = threading.Thread(target=self._laoding_thread, args=[Status8x8.LOADING])
        t.start()

    def _laoding_thread(self, status: Status8x8):
        while self._loading_on:
            for screen in status.value:
                if not self._loading_on: return
                self._control_led_matrix(screen)
                time.sleep(1)

    def _control_led_matrix(self, status: list):
        with canvas(self.device, dither = True) as draw:
            for y, x_row in enumerate(status):
                for x, bit in enumerate(x_row):
                    if bit == 0:
                        draw.point((x, y), fill='white')
