#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 CoroWare Robotics Solutions <corobot.net>
#
# Author: Cameron Owens <cowens@coroware.com>
# Developer: CoroWare Robotics Solutions
# Distributed under terms of the MIT license.

"""
This Python Application takes images from the Raspberry Pi Camera and sends
over ZMQ
"""

# Standard importing of required modules
import io
import time
import picamera

camera_stream = io.BytesIO()
with picamera.PiCamera() as camera:
    camera.start_preview()
    #Allow for Camera to Warm Up
    time.sleep(2) # Units are in seconds. Two seconds is a little long but...
    camera.capture(camera_stream, 'jpeg')
