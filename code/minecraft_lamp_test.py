#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Cycles through a series of colours to represent a number of different 
minecraft block types.
This should use an RGB LED, but might work if using three separate
red, green and blue LED's
"""

import time
import MinecraftLampLed


if __name__ == "__main__":
    try:
        MCBOX = MinecraftLampLed.MinecraftLampLed(17, 27, 22)
        for x in xrange(8):
            MCBOX.next_colour()
            MCBOX.fade_in()
            time.sleep(1.0)
            MCBOX.fade_out()
    except KeyboardInterrupt:
        pass
    finally:
        MCBOX.cleanup()
