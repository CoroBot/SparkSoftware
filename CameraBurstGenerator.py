#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 cameron <cameron@Megatron-Virtual>
#
# Distributed under terms of the MIT license.

"""

"""

import time
import picamera

frames = 60  # Number of frames to capture

with picamera.PiCamera() as camera:
    camera.resolution = (1024, 768)
    camera.framerate = 30
    camera.start_preview()
    time.sleep(2)
    start = time.time()
    camera.capture_sequence([
        'image%02d.jpg' % i
        for i in range(frames)
    ], use_video_port=True)
    finish = time.time()
print('Captured %d frames at %.2ffps' % (
    frames, frames/(finish - start)))
