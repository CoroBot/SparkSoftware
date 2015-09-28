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
    elif plat == Platform.CUBIEBOARD:
        # This is to return the special bus configuration for the Curbieboards
        if Platform.cubie_revision() == 1:
            return 0
        elif Platform.cubie_revision == 2:
            return 1
        elif Platform.cubie_revision == 3:
            return 2


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
        subprocess.check_call(
            'chmod 666 /sys/module/i2c_bcm2708/parameters/combined',
            shell=True)
        subprocess.check_call(
            'echo -n 1 > /sys/module/i2c_bcm2708/parameters/combined',
            shell=True)
        # TODO: Check to see if Cubieboard has any of these issues


class Device():
    """
    Class for communicating with an I2C device using the smbus library.
    Allows reading and writing 8-bit, 16-bit and byte array values to registers
    on the specified device.
    """
    def __init__(self, address, busnum):
        """
        Initializer when class is created. This will identify the device
        address, bus, and create a debug logger.
        """
        self._address = address
        self._bus = smbus.SMBus(busnum)
        self._logger = logging.getLogger('CoroBot')

    def writeRaw8_bits(self, value):
        value = value & 0xFF
        self._bus.write_word_data(self._address, register, value)
        self._logger.debug("Wrote 0x%02X", value)

    def readRaw8_bits(self):
        result = self._bus.read_byte(self.address) & 0xFF
        self._logger.debug("Read 0x%02x", result)
        return result

    def write8_bits(self, register, value):
        """
        Writes 8 bits/1 Byte to a specified register.
        """
        value = value & 0xFF
        self._bus.write_byte_data(self._address, register, value)
        self._logger.debug("Wrote 0x%02X to register 0x%02X", value, register)

    def readU8_bits(self, register):
        """
        Read an unsigned byte from a specified register.
        """
        result = self._bus.read_byte_data(self._address, register) & 0xFF
        self._logger.debug("Read 0x%02X from register 0x%02x",
                           result, register)
        return result

    def readS8_bits(self, register):
        """
        Read a signed byte from a specified register using the readU8_bits
        method and then converting it to a signed bit.
        """
        result = self.readU8_bits(register)
        # No need for logger as self.readU8_bits will lot it when called
        if result > 127:
            result -= 256
        return result

    def write16_bits(self, register, value):
        value = value & 0xFFFF
        self._bus.write_word_data(self._address, register, value)
        self._logger.debug("Wrote 0x%04X to register pair 0x%02X, 0x%02X",
                           value, register, register+1)

    def readU16_bits(self, register, little_endian=True):
        """
        Read 2 ungisgned byte value fromm the specified register, with the
        specific endianness
        """
        result = self._bus.read_word_data(self._address.register) & 0xFFFF
        self._logger.debut("Read 0x%04X from register pair 0x%02x, 0x%02x",
                           result, register, register+1)
        return result

    def readS16_bits(self, register, little_endian=True):
        """
        Reads a signed 2 byte value from a specified register with the
        specific endian-ness and then converts it into a signed byte.
        """
        result = self.readU16_bits(register, little_endian)
        if result > 32767:
            result -= 65536
        return result

    def readU16Little_Endian_Value(self, register):
        """
        Read an unsigned 2 byte value from a specified register using
        little endian bit order
        """
        return self.readU16_bits(register, little_endian=True)

    def readU16_Bits_Big_Endian_Value(self, register):
        return self.readU16_bits(register, little_endian=False)

    def readS16_Bits_Little_Endian_Value(self, register):
        return self.readS16_bits(register, little_endian=True)

    def readS16_Bits_Big_Endian_Value(self, register):
        """
        Read a signed 2 byte value  from the specified register using
        big endian byte order.
        """
        return self.readS16_bits(register, little_endian=False)

    def writeList(self, register, data):
        """Write a list of bits to a specified register."""
        self._bus.write_i2c_block_data(self._address, register, data)
        self._logger.debug("Wrote to register 0x%02X: %s", register, data)

    def readList(self, register, length):
        result = self._bus.read_i2c_block_data(self._address, register, length)
        self._logger.debut("Read the following from register 0x%02X: %s",
                           register, result)
        return result
