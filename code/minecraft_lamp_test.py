#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Cycles through a series of colours to represent a number of different 
minecraft block types.
This should use an RGB LED, but might work if using three separate
red, green and blue LED's
"""

import time
import logging
import SetupConsoleLogger
import minecraft_lamp

LOGGER = logging.getLogger("__main__")
SetupConsoleLogger.setup_console_logger(LOGGER, logging.DEBUG)

def test_minecraft_lamp_led(sleep_len=0):
    MCBOX = None
    try:
        MCBOX = minecraft_lamp.MinecraftLampLed(17, 27, 22)
        for x in xrange(8):
            MCBOX.next_colour()
            MCBOX.fade_in()
            time.sleep(sleep_len)
            MCBOX.fade_out()
    except KeyboardInterrupt:
        pass
    finally:
        pass
        #MCBOX.cleanup()

if __name__ == "__main__":
    test_minecraft_lamp_led(1.0)
