#!/usr/bin/env python

import sys
from Spark_Control import HID_Comm, NET_ZMQ_Comm, Spark_Drive
import time

def main():
	addr = raw_input("Address of target (tcp://its.ip.add.ress:port) or hit enter for local USB:")
	if addr == "-":
		addr = "tcp://raspberrypi.local:4567"
	if addr == "":
		comm = HID_Comm()
		try:
			comm.open()
		except IOError, ex:
			print "Spark not found:",ex
			sys.exit()
	else:
		comm = NET_ZMQ_Comm()
		try:
			comm.open(addr)
		except:
			print "Error connecting to Spark"
			sys.exit()
	
	spark = Spark_Drive(comm)
	drive_loop(spark)
	
def drive_loop(spark):
	while(1):
		print("Driving forward")
		spark.set_motor_speed(6, 12500)
		spark.set_motor_speed(5, 12500)
		#repeat command to try and get more consistent sets on motor speed.
		spark.set_motor_speed(6, 12500)
		spark.set_motor_speed(5, 12500)
		
		time.sleep(3)
	
		#turn around #or for now, stop.
		print("stopping for 2")
		spark.set_motor_speed(6, 0)
		spark.set_motor_speed(5, 0)
		#repeat command
		spark.set_motor_speed(6, 0)
		spark.set_motor_speed(5, 0)	
		time.sleep(2)

		#turn around
		spark.set_motor_direction(6, 1)
		spark.set_motor_direction(6, 1)
		#spark.set_motor_direction(5, 1)
		#spark.set_motor_direction(5, 1)
		spark.set_motor_speed(6, 61000)
		spark.set_motor_speed(5, 61000)
		spark.set_motor_speed(6, 61000)
		spark.set_motor_speed(5, 61000)
		time.sleep(2)
	
		spark.set_motor_direction(5, 0)
		spark.set_motor_direction(6, 0)
		spark.set_motor_direction(5, 0)
		spark.set_motor_direction(6, 0)
		spark.set_motor_speed(5, 0)
		spark.set_motor_speed(6, 0)
		spark.set_motor_speed(5, 0)
		spark.set_motor_speed(6, 0)
		time.sleep(2)
		
	
if __name__ == '__main__':
	main()

	
#END
