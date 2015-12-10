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
	
def us_loop(spark):
	while(1):
		print(65535-spark.get_ultrasonic(1))
		print(65535-spark.get_ultrasonic(2))
		time.sleep(1)	
		
def roomba_loop(spark):
	time.sleep(1)
	
	#set initial state and put into motion
	spark.set_motor_speed(0, 12500) #0 is all motors
	
	while(1)
		#read ultrasonics
		left_dist = getDistance(US_LEFT, INCHES)
		right_dist = getDistance(US_RIGHT, INCHES)
		
		if left_dist < MINIMUM_INCHES:
			#turn_until_clear(RIGHT)
			turn(spark, RIGHT, 2)	
		if right_dist < MINIMUM_INCHES:
			turn(spark, LEFT, 2)
		
		spark.set_motor_speed(0, 12500) #0 is all motors
		
def turn(spark, direction, time):
	print("minimum distance detected, turning (1 for left, 2 for right)" + repr(direction))
	spark.set_motor_speed(0, 0)
	spark.set_motor_speed(0, 0)
	time.sleep(0.5)
	
	#turn around (skid steer)
	#print("Turning around for 2 seconds...")
	spark.set_motor_direction(6, 1)
	spark.set_motor_direction(6, 1)
	spark.set_motor_speed(0, 61000)
	spark.set_motor_speed(0, 61000)
	#spark.set_motor_speed(6, 61000)
	#spark.set_motor_speed(6, 61000)
	#spark.set_motor_speed(5, 61000)
	#spark.set_motor_speed(5, 61000)
	time.sleep(time)
	
	#stopping for a half second
	spark.set_motor_speed(0, 0)
	spark.set_motor_speed(0, 0)
	spark.set_motor_direction(6, 0)
	spark.set_motor_direction(6, 0)
	time.sleep(0.5)
	
		
def getDistance(sensor_num, returnType = INCHES)		
	ret = 65535-spark.get_ultrasonic(sensor_num)	
	if returnType == INCHES:
		return ret #doesnt actually return inches at this point, needs that multiplier
	elif returnType == CM:
		return ret*0.5
	else:
		return ret
		
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
