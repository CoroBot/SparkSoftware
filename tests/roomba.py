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

LOOP_DELAY = 0.05
MINIMUM_INCHES = 3000
SMOOTH_FACTOR = 0.3

avgLeft = 6000
avgRight = 6000

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

	#if the spark was running before, stop it.
	spark.set_motor_speed(0, 0)
	spark.set_motor_speed(0, 0)
	spark.set_motor_speed(0, 0)

	roomba_loop(spark) #call the never ending "drive_loop" function

def roomba_loop(spark):
	print("roomba loop starting...")
	time.sleep(1.5)
	
	#set initial state and put into motion
	spark.set_motor_direction(0, 1)
	spark.set_motor_direction(0, 1)
	spark.set_motor_speed(0, 12500) #0 is all motors
	
	while(1):
		#read ultrasonics and turn if needed
		right_dist = getDistance(spark, US_RIGHT, INCHES)
		left_dist = getDistance(spark, US_LEFT, INCHES)
		updateAverages(left_dist, right_dist)

		#print("left(1) ultrasonic reads: " + repr(left_dist))

		print("right(2) ultrasonic avg: " + repr(avgRight))
		print("left(1) ultrasonic avg: " + repr(avgLeft))
		#if avgLeft < MINIMUM_INCHES:
			#turn(spark, RIGHT, 2)
		#print("right(2) ultrasonic reads: " + repr(right_dist))
		#if rightAvg < MINIMUM_INCHES:
			#turn(spark, LEFT, 2)
		if avgLeft < MINIMUM_INCHES or avgRight < MINIMUM_INCHES:
			turn(spark, LEFT, 2)

		spark.set_motor_speed(0, 12500) #0 is all motors
		time.sleep(LOOP_DELAY)

def updateAverages(left_dist, right_dist):
	global avgLeft
	global avgRight
	newLeftAvg = (left_dist*SMOOTH_FACTOR) + (avgLeft * (1-SMOOTH_FACTOR))
	newRightAvg = (right_dist*SMOOTH_FACTOR) + (avgRight * (1-SMOOTH_FACTOR))
	avgLeft = newLeftAvg
	avgRight = newRightAvg

def turn(spark, direction, turn_time):
	print("minimum distance detected, turning (1 for left, 2 for right)" + repr(direction))
	
	#stop for a half second
	spark.set_motor_speed(0, 0)
	spark.set_motor_speed(0, 0)
	time.sleep(0.3)
	
	#turn around (skid steer)
	spark.set_motor_direction(6, 0)
	spark.set_motor_direction(6, 0)
	spark.set_motor_speed(0, 61000)
	spark.set_motor_speed(0, 61000)
	time.sleep(turn_time)
	
	#stopping for a half second
	spark.set_motor_speed(0, 0)
	spark.set_motor_speed(0, 0)
	spark.set_motor_direction(6, 1)
	spark.set_motor_direction(6, 1)
	time.sleep(0.3)
	
		
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
