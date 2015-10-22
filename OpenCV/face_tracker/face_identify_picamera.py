#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 cameron <cameron@Megatron-Virtual>
#
# Distributed under terms of the MIT license.

"""
This is the Raspberry Pi Version of the Face Tracker since video capture
does not work out of the box. Currently we are working to fix it.
"""

from picamera.array import PiRGBArray
from picamera import PiCamera

import cv2

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

for frame in camera.capture_continuous(rawCapture, format='bgr',
                                       use_video_port=True):
    image = frame.array
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray_image,
                                          scaleFactor=1.1,
                                          minNeighbors=5,
                                          minSize=(30, 30),
                                          flags=cv2.CASCADE_SCALE_IMAGE)
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
        center_point = ((x+(x+w))/2, (y+(y+h))/2)
        cv2.rectangle(image, center_point, center_point, (255, 0, 0), 8)

    cv2.imshow("Faces", image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
