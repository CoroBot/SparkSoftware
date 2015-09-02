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
import time
import picamera
import zmq

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("NEED GLOBAL TO PUT HERE")

try:
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.start_preview()
        time.sleep(2)  # Two seconds is a little long but....
        start = time.time()

