#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 cameron <cameron@Megatron-Virtual>
#
# Distributed under terms of the MIT license.

"""
This is a basic Python application that introduces using the GPIO directly
on the Raspberry Pi. This Python Script blinks an LED connected to Pin 02.
"""

# Standard Module Imports
import RPi.GPIO as GPIO  # Importing GPIO Module for Python
import time


# Blinky Function
def blinky(pin):  # This function takes the input of the pin number
    GPIO.output(pin, GPIO.HIGH)  # Turns LED ON
    time.sleep(0.5)  # Delay of specified time in seconds (floats are ok)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.5)  # Turns LED OFF
    return
# Definition of Pin Numbers
GPIO.setmode(GPIO.BOARD)
GPIO.setup(2, GPIO.OUT)  # Configuring pin 2 as our ourtput
while True:
    blinky(2)
