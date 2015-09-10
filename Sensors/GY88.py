#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 CoroWare Robotics Solutoins <www.corobot.net>
#
# Distributed under terms of the MIT license.
# Author: Cameron Owens <cowens@coroware.com>

"""
This is the Python Driver for the GY-88 IMU Breakout board written in Python
"""

import logging
import time

# On this board there are 3 Primary Sensors
# 1) Digital Compass: HMC5883L
# 2) Barometric Pressor Sensor: BMP085
# 3) Three axix Gyro+Accelerometer: MPU6050


# Declaration of Sensor Address
HMC5883_I2CADDR = 0x1E
BMP8085_I2CADDR = 0x77
MPU6050_I2CADDR = 0x68

# HMC5883 Configuration Registers
HMC5883_CONFA = 0x00
HMC5883_CONFB = 0x01
HMC5883_MODE = 0x02
HMC5883_STATUS = 0x09
HMC5883_IDENTA = 0x10
HMC5883_IDENTB = 0x11
HMC5883_IDENTC = 0x12

# HMC5883 Command Registers
HMC5883_XMSB = 0x03  # X Axis MSB (Most significant bit)
HMC5883_XLSB = 0x04  # X Axis LSB (Least significant bit)
HMC5883_ZMSB = 0x05  # Z Axis MSB
HMC5883_ZLSB = 0x06  # Z Axis LSB
HMC5883_YMSB = 0x07  # Y Axis MSB
HMC5883_YLSB = 0x08  # Y Axis LSB

# BMP8085 Calibration Registers
BMP085_CAL_AC1 = 0xAA  # Calibration Data (16 Bits)
BMP085_CAL_AC2 = 0xAC  # Calibration Data (16 Bits)
BMP085_CAL_AC3 = 0xAE  # Calibration Data (16 Bits)
BMP085_CAL_AC4 = 0xB0  # Calibration Data (16 Bits)
BMP085_CAL_AC5 = 0xB2  # Calibration Data (16 Bits)
BMP085_CAL_AC6 = 0xB4  # Calibration Data (16 Bits)
BMP085_CAL_B1 = 0xB6   # Calibration Data (16 Bits)
BMP085_CAL_B2 = 0xBA   # Calibration Data (16 Bits)
BMP085_CAL_MB = 0xBC   # Calibration Data (16 Bits)
BMP085_CAL_MD = 0xBE   # Calibration Data (16 Bits)
BMP085_CONTROL = 0xF4
BMP085_TEMPDATA = 0xF6
BMP085_PRESSUREDATA = 0xF6

# BMP085 Command Registers
BMP085_READTEMPCMD = 0x2E  # Temperature Read Register
BMP085_READPRESCMD = 0x34  # Pressure Read Register

# MPU6050 Configuration/Calibration Registers
MPU6050_SELF_TEST_X = 0x0D
MPU6050_SELF_TEST_Y = 0x0E
MPU6050_SELF_TEST_Z = 0x0F
MPU6050_SELF_TEST_A = 0x10
MPU6050_CONFIG = 0x1A
MPU6050_GYRO_CONFIG = 0x1B
MPU6050_ACCL_CONFIG = 0x1C


# MPU6050 Command Registers
MPU6050_ACCEL_XOUT_H = 0x3B
MPU6050_ACCEL_XOUT_L = 0x3C
MPU6050_ACCEL_YOUT_H = 0x3D
MPU6050_ACCEL_YOUT_L = 0x3E
MPU6050_ACCEL_ZOUT_H = 0x3F
MPU6050_ACCEL_ZOUT_L = 0x40
MPU6050_TEMP_H = 0x41
MPU6050_TEMP_L = 0x42
MPU6050_GYRO_XOUT_H = 0x43
MPU6050_GYRO_XOUT_L = 0x44
MPU6050_GYRO_YOUT_H = 0x45
MPU6050_GYRO_YOUT_L = 0x46
MPU6050_GYRO_ZOUT_H = 0x47
MPU6050_GYRO_ZOUT_L = 0x48


class GY88():
    def __init__(self, mode=GBY88_STANDARD, compaddress=HMC5883_I2CADDR, baraddress=BMMP8085_I2CADDR, imuaddress=MPU6050_I2CADDR, i2c=None, **kwargs)
        self._logger = logging.getLogger('IMU_LOGGER')
        if mode not in [GY88_COMPASS, GY88_BAROMETER, GY88_IMU, GY88_STANDARD]:
            raise ValueError('Unexpected mode select {0}. Set mode to one of the available options')
        self._mode = mode

        self._load_calibration()

    def _load_calibration(self):
        self.cal_AC1 = self._device.reads16B
    def _load_datasheet_calibration_BMP085(self):
        self.cal_AC1 = 408
        self.cal_AC2 = -72
        self.cal_AC3 = -14383
        self.cal_AC4 = 32741
        self.
