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
import Image
import cStringIO as StringIO


def main():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("NEED GLOBAL TO PUT HERE")
    while True:
        with picamera.PiCamera() as camera:
            with picamera.array.PiRGBArray(camera) as output:
                camera.resolution = (1280, 720)
                start = time.time()
                camera.capture(output, 'rgb')
                f = StringIO.StringIO()
                Image.fromarray(camera.capture(output, 'rgb')).save(f, "JPEG")
                socket.send_multipart(["", b"B", b"VF", f.getvalue()])
                stop = time.time()
                elapsed_time = stop - start
                return elapsed_time
                f.close()
