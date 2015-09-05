#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 cameron <cameron@Megatron-Virtual>
#
# Distributed under terms of the MIT license.

"""
This is a basic test recipe from picamear docs for a network stream
"""

import socket
import time
import picamera

with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    camera.framerate = 24

    server_socket = socket.socket()
    server_socket.bind(('192.168.1.130', 8000))
    server_socket.listen(0)

    connection = server_socket.accept()[0].makefile('wb')
    while True :
        camera.start_recording(connection, format='h264')
        camear
