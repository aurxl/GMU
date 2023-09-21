#!/bin/env python
import board
import busio
import adafruit_character_lcd.character_lcd_i2c as c_lcd
import time


class out_lcd():
    def __init__(self):
        self.text = "hier könnte ihre Werbung stehen"
        self.columns = 16
        self.rows = 2
        self.stop = self.stop()
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.lcd = c_lcd.Character_LCD_I2C(self.i2c,
                                           self.columns,
                                           self.rows,
                                           0x21)
        self.backlight(True)

    def backlight(self, on: bool = True) -> (bool, Exception):
        try:
            self.lcd.backlight = True
            return True, None
        except Exception:
            return False, Exception

    def msg(self, text: str = "hello world", cursor: bool = False) -> (bool, Exception):
        self.text = text
        self.lcd.clear()
        try:
            if cursor: self.lcd.cursor = True
            self.lcd.message = self.text
            return True, None
        except Exception:
            return False, Exception

    def scroll(self, speed: float = 0.5, text: str = "") -> (bool, Exception):
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
        try:
            self.lcd.clear()
            self.backlight(False)
            return True, None
        except Exception:
            return False, Exception
