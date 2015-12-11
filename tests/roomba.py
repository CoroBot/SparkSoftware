#!/usr/bin/env python

import sys
from Spark_Control import HID_Comm, NET_ZMQ_Comm, Spark_Drive
import time
#import constants

'''
roomba.py

This script lets the spark drive itself over a small area autonomously, with basic
obstacle avoidance routines.

By looking at this example code, you can learn how to control the motors
on the spark kit, as well as use sensor data to make decisions.
'''

#Constants
LEFT = 1
RIGHT = 2

US_LEFT = 1
US_RIGHT = 2

INCHES = 0
CM = 1
RAW = 2

MINIMUM_INCHES = 2500

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
	roomba_loop(spark) #call the never ending "drive_loop" function
		
def roomba_loop(spark):
	print("roomba loop starting")
	time.sleep(1)
	
	#set initial state and put into motion
	spark.set_motor_direction(0, 0)
	spark.set_motor_speed(0, 12500) #0 is all motors
	
	while(1):
		#read ultrasonics and turn if needed

		left_dist = getDistance(spark, US_LEFT, INCHES)
		print("left(1) ultrasonic reads: " + repr(left_dist))
		if left_dist < MINIMUM_INCHES:
			turn(spark, RIGHT, 2)
	
		right_dist = getDistance(spark, US_RIGHT, INCHES)
		print("right(2) ultrasonic reads: " + repr(right_dist))
		if right_dist < MINIMUM_INCHES:
			turn(spark, LEFT, 2)
		
		spark.set_motor_speed(0, 12500) #0 is all motors
		time.sleep(0.1)

def turn(spark, direction, turn_time):
	print("minimum distance detected, turning (1 for left, 2 for right)" + repr(direction))
	
	#stop for a half second
	spark.set_motor_speed(0, 0)
	spark.set_motor_speed(0, 0)
	time.sleep(0.5)
	
	#turn around (skid steer)
	#print("Turning around for <turn_time> seconds...")
	spark.set_motor_direction(6, 1)
	spark.set_motor_direction(6, 1)
	spark.set_motor_speed(0, 61000)
	spark.set_motor_speed(0, 61000)
	time.sleep(turn_time)
	
	#stopping for a half second
	spark.set_motor_speed(0, 0)
	spark.set_motor_speed(0, 0)
	spark.set_motor_direction(6, 0)
	spark.set_motor_direction(6, 0)
	time.sleep(0.5)
	
		
def getDistance(spark, sensor_num, returnType = INCHES):		
	ret = 65535-spark.get_ultrasonic(sensor_num)	
	if returnType == INCHES:
		return ret #doesnt actually return inches at this point, needs that multiplier
	elif returnType == CM:
		return ret*0.5
	else:
		return ret

if __name__ == '__main__':
	main()

	
#END
