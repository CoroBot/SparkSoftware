#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 CoroWare Robotics Solutions <www.corobot.net>
#
# Distributed under terms of the MIT license.

"""
This is a basic script to remote control the CoroBot Spark from your computer
"""

import sys
from Spark_Control import HID_Comm, NET_ZMQ_Comm, Spark_Drive
from readchar import readkey

def main():
    address = raw_input("Address of Spark or press 'return' if using board")
    if address == "-":
        address == "tcp://CoroBotSpark.local:4567"
    elif address == "":
        comm = HID_Comm()
        try:
            comm.open()
        except IOError, ex:
            print("Spark not found:", ex)
            sys.exit()
    else:
        comm = NET_ZMQ_Comm()
        try:
            comm.open(address)
        except:
            print("Error connecting to Spark")
            sys.exit()
    spark = Spark_Drive(comm)
    drive_spark(spark)
