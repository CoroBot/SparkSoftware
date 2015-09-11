#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 Coroware Robotics Solutions <www.corobot.net>
#
# Distributed under terms of the MIT license.

"""
The purpose of this module is to identify the platform a user is using
to better use the hardware they are deploying
"""

import sys
import platform
import re

# Supported Platform List
UNKNOWN = 0
RASPBERRY_PI = 1
BEAGLEBONE_BLACK = 2
MINOWBOARD = 3
CUBIEBOARD = 4


def get_operating_system():
    operating_sys = sys.platform
    return operating_sys


def get_python_version():
    python_version = sys.version
    if python_version[:1] != '3':
        print("WARNING: All CoroBot Python Code is designed for Python3 or newer")


def pi_revision():
    """
    Detects the revision number of a Raspberry Pi for changing
    functionality like default I2C bus based on revision.
    """
    with open('/proc/cpuinfo', 'r') as infile:
        for line in infile:
            match = re.match('Revision\s+:\s+.*(\w{4}$',
                             line, flags=re.IGNORECASE)
            if match and match.group(1) in ['0000', '0002', '0003']:
                return 1
            elif match:
                # Assume revision 2 if revision ends with any other 4 characters
                return 2
        # Error if can't find the version of Raspberry Pi
        raise RuntimeError("Could not determine Ras Pi revision.")


def pi_version():
    """
    Detect the version of the Raspberry Pi. Returns either 1, 2, or
    None depending on Raspberry Pi model number (A, B, A+, B+)
    """
    # Check /proc/cpuinfo for the Hardware Field
    # 2708 = Pi 1 & 2709 is Pi 2
    with open('/proc/cpuinfo', 'r') as infile:
        cpuinfo = infile.read()
    # Search for line matching 'Hardware  : BMCxxxx'
    match = re.search('^Hardware\s+:\s+(\w+)$', cpuinfo,
                      flags=re.MULTILINE | re.IGNORECASE)
    if not match:
        # Could not find hardware info and assume it's not a Pi.
        return None
    if match.group(1) == "BCM2708":
        return 1
    elif match.group(1) == "BCM2709":
        return 2
    else:
        # Something that is not a Pi
        return None
