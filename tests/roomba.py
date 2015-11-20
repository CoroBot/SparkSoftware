#!/usr/bin/env python

import sys
from Spark_Control import HID_Comm, NET_ZMQ_Comm, Spark_Drive
import time
#import constants

'''
CoroBot spark test script - "drive_loop.py"

This script lets the spark drive itself over a small area autonomously.

By looking at this example code, you can learn how to control the motors
on the spark kit, as well as insert software delays between actions.
'''

def main():
	#This is how you should connect to your spark. This code must execute
	#before the raspberry pi can talk to the spark hat.
	
	addr = "tcp://raspberrypi.local:4567"
	comm = NET_ZMQ_Comm()
	try:
		comm.open(addr)
	except:
		print "Error connecting to Spark"
		sys.exit()
	
	spark = Spark_Drive(comm)
	drive_loop(spark) #call the never ending "drive_loop" function
	

def drive_loop(spark):
	while(1):
		#drive forward
		print("Driving forward for 3 seconds...")
		spark.set_motor_speed(6, 12500) #lets give the user these controls: named motor constants, percentage of speed 0-1).
		spark.set_motor_speed(5, 12500)
		#repeat command to try and get more consistent sets on motor speed.
		spark.set_motor_speed(6, 12500)
		spark.set_motor_speed(5, 12500)
		
		time.sleep(3)
	
		#stop
		print("Stopping for 1 second...")
		spark.set_motor_speed(6, 0)
		spark.set_motor_speed(5, 0)
		#repeat command
		spark.set_motor_speed(6, 0)
		spark.set_motor_speed(5, 0)	
		time.sleep(1)

		#turn around (skid steer)
		print("Turning around for 2 seconds...")
		spark.set_motor_direction(6, 1)
		spark.set_motor_direction(6, 1)
		spark.set_motor_speed(6, 61000)
		spark.set_motor_speed(5, 61000)
		spark.set_motor_speed(6, 61000)
		spark.set_motor_speed(5, 61000)
		time.sleep(2)
	
		#stop turning and set motors back to forward direction
		print("Stopping for 1 second and then repeating...")
		spark.set_motor_direction(5, 0)
		spark.set_motor_direction(6, 0)
		spark.set_motor_direction(5, 0)
		spark.set_motor_direction(6, 0)
		spark.set_motor_speed(5, 0)
		spark.set_motor_speed(6, 0)
		spark.set_motor_speed(5, 0)
		spark.set_motor_speed(6, 0)
		time.sleep(1)
		
	
if __name__ == '__main__':
	main()

	
#END
