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
import platform
if platform.machine() == "armv6l" or platform.machine() == "armv7l":
    import RPi.GPIO as GPIO
else:
    import GPIOStub as GPIO

LOGGER = logging.getLogger("__main__.MinecraftLampLed")


class MinecraftLampLed(object):
    """
    Provides ability to control the motors on the robot.
    """

    START_FREQ = 1000
    RED_INDEX = 0
    GRN_INDEX = 1
    BLU_INDEX = 2
    NAME_INDEX = 3
    NUM_STEPS = 50
    FADE_TIME = 1.0

    def __init__(self, redgpio, greengpio, bluegpio):
        """
        Initialises GPIO pins and PWM.
        """
        LOGGER.info("Initialising Minecraft Lamp")

        self.colours = [[100, 0, 0, "Red (Redstone)"], 
                        [50, 100, 100, "Cyan (Diamond)"], 
                        [100, 25, 0, "Orange (Copper)"], 
                        [0, 100, 0, "Green (Emerald)"],
                        [0, 0, 100,"Blue (Lapis Lazuli)"], 
                        [100, 50, 0, "Yellow (Gold)"],
                        [100, 0, 100, "Magenta"], 
                        [100, 100, 100, "White"]]

        # Use board pin numbering
        GPIO.setmode(GPIO.BCM)

        # Disable warnings
        GPIO.setwarnings(False)

        # Setup the GPIO ports as outputs
        GPIO.setup(redgpio, GPIO.OUT)
        GPIO.setup(greengpio, GPIO.OUT)
        GPIO.setup(bluegpio, GPIO.OUT)

        # Setup the GPIO ports to use the PWM
        # so we can change the brightness and
        # therefore colour
        self.red_led = GPIO.PWM(redgpio, self.START_FREQ)
        self.green_led = GPIO.PWM(greengpio, self.START_FREQ)
        self.blue_led = GPIO.PWM(bluegpio, self.START_FREQ)

        # Set the PWM to off at the start
        self.red_led.start(0)
        self.green_led.start(0)
        self.blue_led.start(0)

        # Store the current index
        self.current_index = len(self.colours) - 1

    def cleanup(self):
        """
        Cleans up the GPIO pins.
        """
        LOGGER.info("Turning off and cleaning up")
        self.red_led.ChangeDutyCycle(0)
        self.green_led.ChangeDutyCycle(0)
        self.blue_led.ChangeDutyCycle(0)
        GPIO.cleanup()

    #pylint: disable-msg=R0913
    def __fade(self, red_level, r_step, green_level, g_step, blue_level, b_step):
        """
        Perform the fade operation
        """
        # For each step decreases or increase the level equally
        # until it reaches the number of steps
        for _ in xrange(self.NUM_STEPS):
            red_level += r_step
            green_level += g_step
            blue_level += b_step
            self.red_led.ChangeDutyCycle(red_level)
            self.green_led.ChangeDutyCycle(green_level)
            self.blue_led.ChangeDutyCycle(blue_level)
            time.sleep(self.FADE_TIME / self.NUM_STEPS)

    def fade_out(self):
        """
        Fade from the current colour to all off
        """
        # define the red starting point and red step size
        red_level = self.colours[self.current_index][self.RED_INDEX]
        red_step = float(red_level) / float(self.NUM_STEPS)

        # define the green starting point and red step size
        green_level = self.colours[self.current_index][self.GRN_INDEX]
        green_step = float(green_level) / float(self.NUM_STEPS)

        # define the blue starting point and red step size
        blue_level = self.colours[self.current_index][self.BLU_INDEX]
        blue_step = float(blue_level) / float(self.NUM_STEPS)

        self.__fade(red_level, -red_step, green_level, -green_step, blue_level,
                  -blue_step)

    def fade_in(self):
        """
        Fade from all off to the desired colour
        """
        red_step = float(self.colours[self.current_index][
            self.RED_INDEX]) / float(self.NUM_STEPS)
        green_step = float(self.colours[self.current_index][
            self.GRN_INDEX]) / float(self.NUM_STEPS)
        blue_step = float(self.colours[self.current_index][
            self.BLU_INDEX]) / float(self.NUM_STEPS)

        self.__fade(0, red_step, 0, green_step, 0, blue_step)

    def next_colour(self):
        """
        Cycles to the next colour.
        """
        # Update to the next colour
        self.current_index = (self.current_index + 1) % len(self.colours)
        LOGGER.info(
            'Colour =  %s', self.colours[self.current_index][self.NAME_INDEX])
