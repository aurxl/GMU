#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017-18 Richard Hull and contributors
# License: https://github.com/rm-hull/luma.led_matrix/blob/master/LICENSE.rst
# Github link: https://github.com/rm-hull/luma.led_matrix/

# Alle benötigten Module importieren 
import re
import time
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT


def main(cascaded, block_orientation, rotate):
    
    # Matrix Gerät festlegen und erstellen.
    serial = spi(port=0, device=1, gpio=noop())
    device = max7219(serial, cascaded=cascaded or 1, block_orientation=block_orientation,
    rotate=rotate or 0)
    # Matrix Initialisierung in der Konsole anzeigen
    print("[-] Matrix initialized")

    # Hallo Welt in der Matrix anzeigen
    msg = "Hallo Welt"
    # Ausgegebenen Text in der Konsole Anzeigen
    print("[-] Printing: %s" % msg)
    show_message(device, msg, fill="white", font=proportional(CP437_FONT), scroll_delay=0.1)


if __name__ == "__main__":
    
    # cascaded = Anzahl von MAX7219 LED Matrixen, standart=1
    # block_orientation = choices 0, 90, -90, standart=0
    # rotate = choices 0, 1, 2, 3, Rotate display 0=0°, 1=90°, 2=180°, 3=270°, standart=0
   
    try:
        main(cascaded=1, block_orientation=90, rotate=0)
    except KeyboardInterrupt:
        pass
