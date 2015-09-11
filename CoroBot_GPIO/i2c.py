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
import CoroBot_GPIO.Platform as Platform


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


def get_default_bus():
    """
    Returns the default I2C Bus number based on the platform being used .
    Example: Raspberry Pi will either use bus 0 or 1 (Depending on Pi Revision)
    """
    plat = Platform.platform_detect()
    if plat == Platform.RASPBERRY_PI:
        if Platform.pi_revision() == 1:
            # Revision 1 uses I2C bus 0.
            return 0
        else:
            # Revision 2 Uses I2C Bus 1
            return 1
    elif plat == Platform.BEAGLEBONE_BLACK:
        # The Beaglebone Black has multiple I2C Busses. Default is set for bus1
        # Bus two is for EEPROM and has rules of how it can be used
        return 1


def get_I2C_device(address, busnum=None, **kwargs):
    """
    Returns an I2C device for the specified address and on the specified bus.
    If 'busnum is not specified, the default I2C bus for the platform will
    attempt to be detected.
    """
    if busnum is None:
        busnum = get_default_bus()
    return Device(address, busnum, **kwargs)


def require_repeated_start():
    """
    Enable repeated start conditions for I2C register reads. This is the normal
    behaviour for I2C, but some platforms such as the Raspi have issues with
    this feature and often require explicitly enabliing this feature
    """
    plat = Platform.platform_detetct()
    if plat == Platform.RASPBERRY_PI:
        subprocess.check_call('chmod 666 /sys/module/i2c_bcm2708/parameters/combined', shell=True)
        subprocess.check_call('echo -n 1 > /sys/module/i2c_bcm2708/parameters/combined', shell=True)
        #TODO: Check to see if Cubieboard has any of these issues

class Device():
    """
    Class for communicating with an I2C device using the smbus library.
    Allows reading and writing 8-bit, 16-bit and byte array values to registers
    on the specified device.
    """
    def __init__(self, address, busnum):
        self._address = address
        self._bus = smbus.SMBus(busnum)
        self._logger = logging.getLogger('CoroBot')

    def writeRaw8(self, value):
        value = value & 0xFF
        self._bus.write_word_data(self._address, register, value)
        self._logger.debug("Wrote 0x%02X", value)


    def write8(self, register, value):
        value = value & 0xFF
        self._bus.write_byte_data(self._address, register, value)
        self._logger.debug("Wrote 0x%02X to register 0x%02X" value, register)


    def write16(self, register, value):
        value = value & 0xFFFF
