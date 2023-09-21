#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import board
import busio
import adafruit_character_lcd.character_lcd_i2c as character_lcd

# Definiere LCD Zeilen und Spaltenanzahl.
lcd_columns = 16
lcd_rows    = 2

# Initialisierung I2C Bus
i2c = busio.I2C(board.SCL, board.SDA)

# Festlegen des LCDs in die Variable LCD
lcd = character_lcd.Character_LCD_I2C(i2c, lcd_columns, lcd_rows, 0x21)

try:
    # Hintergrundbeleuchtung einschalten
    lcd.backlight = True

    # Zwei Worte mit Zeilenumbruch werden ausgegeben
    lcd.message = "Hallo\nWelt!"

    # 5 Sekunden warten
    time.sleep(5.0)

    # Cursor anzeigen lassen.
    lcd.clear()
    lcd.cursor = True
    lcd.message = "Show Cursor!"
    
    # 5 Sekunden warten
    time.sleep(5.0)

    # Cursor blinken lassen
    lcd.clear()
    lcd.blink = True
    lcd.message = "Blinky Cursor!"
    
    # 5 Sekunden warten, den blinkenden Cursor stoppen und Cursor ausblenden
    time.sleep(5)
    lcd.blink = False
    lcd.clear()
    
    
    
    # Nachricht von Rechts/Links scrollen lassen.
    lcd.clear()
    scroll_msg = "<-- Scroll -->"
    lcd.message = scroll_msg
    for i in range(len(scroll_msg)):
        time.sleep(0.5)
        lcd.move_right()
    for i in range(len(scroll_msg)):
        time.sleep(0.5)
        lcd.move_left()


    # Hintergrundbeleuchtung an und ausschalten.
    lcd.clear()
    lcd.message = "Flash backlight\nin 5 seconds..."
    time.sleep(5.0)
    # Hintergrundbeleuchtung ausschalten.
    lcd.backlight = False
    time.sleep(1.0)
    lcd.backlight = True
    time.sleep(1.0)
    lcd.backlight = False
    # Nachricht ändern.
    lcd.clear()
    lcd.message = "Goodbye"
    # Hintergrundbeleuchtung einschalten.
    lcd.backlight = True
    # Hintergrundbeleuchtung ausschalten.
    time.sleep(2.0)
    lcd.clear()
    lcd.backlight = False
    
    
    
except KeyboardInterrupt:
    # LCD ausschalten.
    lcd.clear()
    lcd.backlight = False
