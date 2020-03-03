#!/usr/bin/env python

"""
TaskLight - a notification light controller
Requires Adafruit's FT232H Breakout (https://www.adafruit.com/product/2264)
and a single NeoPixel.

Version:
    2.0.0

Copyright:
    2020, Tony Smith (@smittytone)

License:
    MIT (terms attached to this repo)
"""

# IMPORTS
import time
import sys
import os
import board
import neopixel_spi as neopixel


# CONSTANTS
FLASH_DELAY = 0.3
MAX_COLOURS = 3


# FUNCTIONS
def clear(ps):
    # Turn the NeoPixel off
    ps[0] = (0, 0, 0)
    ps.show()

def cycle(c):
    # Increment c and cycle to 0 if necessary
    c += 1
    if c >= MAX_COLOURS: c = 0
    return c


# START
if __name__ == '__main__':

    # Set up the NeoPixel array, as per the library and clear it
    # NOTE There's only one NeoPixel
    pixels = neopixel.NeoPixel_SPI(board.SPI(),
                                   1,
                                   pixel_order = neopixel.GRB,
                                   auto_write = False)
    clear(pixels)

    # Initialize key variables
    filename = os.path.expanduser("~") + '/.status'
    brightness = 30 # Brightness control as a percentage
    notification = [False, False, False]
    colour = [0, 0, 0]
    count = 0
    flashState = True

    # Run the loop
    while True:
        try:
            # Set the colours of each component in the NeoPixel
            # This will alternate between 2 and 3 colours, and
            # alternate one colour with black (off)
            numberOfAlerts = 0
            for i in range(0, MAX_COLOURS):
                colour[i] = 0
                if notification[i] is True:
                     numberOfAlerts += 1
                     if i == count and flashState is True:
                        colour[i] = 255

            if numberOfAlerts == 1:
                flashState = not flashState
                count = notification.index(True)
            elif numberOfAlerts > 1:
                if not flashState: flashState = True
                while True:
                    count = cycle(count)
                    if notification[count] is True: break

            # Draw and display the Neopixel (first and only item in 'pixels' array)
            pixels[0] = (int(colour[0] * brightness / 100), int(colour[1] * brightness / 100), int(colour[2] * brightness / 100))
            pixels.show()

            # Check the status file
            if os.path.exists(filename):
                file = open(filename)
                text = file.read()
                file.close()
                # File contains four values, eg. 0.0.0.0
                # First is a marker for the red light (1 = on; 0 = off), etc.
                # Fourth is a 'stop script' marker for debugging
                items = text.split('.')
                if len(items) > MAX_COLOURS:
                    if items[MAX_COLOURS] == '1':
                        # Halt called, so switch off the LED and bail
                        clear(pixels)
                        sys.exit(0)

                # Check each item -- can do better error checking here!
                for i in range(0, MAX_COLOURS):
                    if items[i] != '0':
                        # Status file indicates notification light should be on
                        # NOTE Any value other that '0' will work
                        if notification[i] is False:
                            notification[i] = True
                    else:
                        # Turn of the light if it's currently on
                        if notification[i] is True:
                            notification[i] = False
            else:
                # No status file - warn the user
                print('[ERROR] No .status file')
                sys.exit(1)

            time.sleep(FLASH_DELAY)
        except KeyboardInterrupt:
            clear(pixels)
sys.exit(-1)
