#!/bin/env python
import board
import busio
import adafruit_character_lcd.character_lcd_i2c as c_lcd
from adafruit_ht16k33.segments import Seg7x4
import time


class out_lcd():
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

class out_segment():
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
        dot_controll = 0

        for i, c in enumerate(chars):
            ii = i  - dot_controll
            try:
                if c == "." or c == ",":
                    self.segment[ii - 1] = c
                    dot_controll += 1
                else:
                    self.segment[ii] = c
                written_chars += c
                self.segment.show()
            except:
                return written_chars, False
        return written_chars, True

    def stop(self) -> bool:
        """turning display off"""
        try:
            self.segment.fill(0)
            return True
        except Exception:
            return False
