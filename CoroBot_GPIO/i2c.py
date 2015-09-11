#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 CoroWare Robotics Solutions <www.corobot.net>
#
# Distributed under terms of the MIT license.

"""
This Python Module provide user several methods to more easily interface with
I2C devices using any embedded ARM SBC; typically the Raspberry Pi.

This module was first based off the Adafruit I2C.py module and then changes
were made to fit the needs of the various robotics projects based on the CoroBot
Spark and other CoroBot platforms.
"""

import logging
import subprocess
import smbus

def reverseByteOrder(data):
    """
    This method provides the means for reversing the byte order depending on
    system architecture. See 'Big Endian' vs 'Little Endian'
    """
    byteCount = len(hex(data)[2:].replace('L', '')[::2])
    val = 0
    for i in range(byteCount):
        val = (val << 8) | (data & 0xff)
        data >>= 8
    return val


def get_I2C_device(address, busnum=None, **kwargs):
    """
    Returns an I2C device for the specified address and on the specified bus.
    If 'busnum is not specified, the default I2C bus for the platform will
    attempt to be detected.
    """
    if busnum is None:
        busnum = get_default_bus()
    return Device(address, busnum, **kwargs)

def
