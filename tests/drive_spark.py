#!/usr/bin/env python

import sys
from Spark_Control import HID_Comm, NET_ZMQ_Comm, Spark_Drive
from readchar import readkey


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
	drive_spark(spark)


def drive_spark(spark):
	max_speed = 65000
	dir_l = 0
	dir_r = 0
	speed = 0
	vec = 0
	while (1):
		left = speed + (vec*speed)
		right = speed - (vec*speed)
		if (max(left,right)>1):
			left = left / 2.0
			right = right / 2.0

		if left < 0:
			dir_l = 1
			left = abs(left)
		else:
			dir_l = 0

		if right < 0:
			dir_r = 1
			right = abs(right)
		else:
			dir_r = 0
			
		lmotor = left * max_speed
		rmotor = right * max_speed
		spark.set_motor_speed(6, lmotor)
		spark.set_motor_speed(5, rmotor)
		spark.set_motor_direction(6, dir_l)
		spark.set_motor_direction(5, dir_r)
		
		k = readkey()
		if k == 'w':
			speed += 0.05
		if k == 's':
			speed -= 0.05
		if k == 'a':
			vec -= 0.1
		if k == 'd':
			vec += 0.1
		if k == ' ':
			speed = 0
			vec = 0
			dir_l = 0
			dir_r = 0
		if k == 'X':
			break
			
		vec = max(min(vec,1),-1)
		speed = max(min(speed,1),-1)
		
	spark.set_motor_direction(6, 0)
	spark.set_motor_direction(5, 0)
	spark.set_motor_speed(6, 0)
	spark.set_motor_speed(5, 0)
	
		
		



	
def do_motor(comm):
	#motor speed
	raw_motor_num = raw_input("Which motor? (Special values: 0 = Both, 6 = Left, 5 = Right)\n>>")
	try:
		motornum = int(raw_motor_num.strip())
	except:
		print "Error converting motornum"
		return
	
	try:
		raw_option = raw_input("Enter 0 for direction, 1 for speed\n>>")
		option = int(raw_option.strip())
	except:
		print "Error converting value"
		return	
	
	if option == 1:
		#do_speed(comm)
		try:
			raw_val = raw_input("Enter a new compare value for the motor duty cycle, 0-65535\n>>")
			val = int(raw_val.strip())
		except:
			print "Error converting speed value"
			return
		comm.set_motor_speed(motornum, val)		
	elif option == 0:
		#do_direction(comm)
		try:
			raw_val = raw_input("Enter 0 for forward, 1 for reverse\n>>")
			val = int(raw_val.strip())
		except:
			print "Error converting direction value"
			return
		comm.set_motor_direction(motornum, val)		

		

		
if __name__ == '__main__':
	main()

	
#END
