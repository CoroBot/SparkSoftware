#!/usr/bin/env python

from cobs_serial import cobs_serial
import sys
import struct
import platform
import hid
import zmq


#USB Constants
coroware_VID = 0x2bd6 #Issued by USB-IF
spark_PID = 0xff02 #Development hardware - will change when device is released

#Servo Constants, for TowerPro MG995
servo_period = 2000 #period of PWM component (ie servo duty cycle) = 20ms
maxpulse = 214 # 10.7% of period
minpulse = 54 # 2.7% of period

def ordlist(x):
	"""Ordlist(x): takes a string or bytearray and returns a list of integers, each of which
       is the ordinal value of the same offest in the string.
	   Example:
	       ordlist("\x01\x02\x03") -> [1,2,3]"""
	return [ord(l) if type(l) == str else l for l in x]
  
  
class HID_Comm(object):
	"""HID_COMM Object:
	  The HID_COMM object is designed to be used from inside the Spark_Control object. 
	  Essentially, it abstracts the USB Human Interface (Generic) driver code to 
	  allow the Spark_Control interface to use any of several communications layers."""
	def __init__(self):
		"""Creates a HID_Comm object - initializing the underlying USB HID Generia device driver"""
		self.hiddev = hid.device()
		self.prefix = []
		if platform.system() == 'Windows':
			self.prefix=[0x80]
		self.isopen=False

	def open(self, vid=coroware_VID, pid=spark_PID):
		"""This call opens the HID Generic driver for reading and writing - and attaches it to a specific
		USB HID peripheral with vendor ID of vid and product ID of pid."""
		if self.isopen:
			raise ValueError, "Already Open"
		self.hiddev.open(vid,pid)
		self.sernum = self.hiddev.get_serial_number_string()
		self.isopen = True

	def close(self):
		"""Closes the underlying HIS peripheral and releases it back to the underlying OS."""
		if not self.isopen:
			raise ValueError, "Not Open"
		self.hiddev.close()
		self.isopen = False

	def send(self, data):
		"""Raw HID Generic send - this is a thin wrapper over the underlying library call to fix up isues
		on Windows and prevent avoidable segfaults inside the library"""
		if not self.isopen:
			raise IOError, "Not Open"
		prefix = self.prefix[:]
		prefix.extend(ordlist(data))
		self.hiddev.write(prefix)

	def receive(self, numbytes=64, blocking=True):
		"""Raw HID Generic receive - this is a thin wrapper over the underlying library call to fix up isues
		on Windows and prevent avoidable segfaults inside the library. Use blocking=False for a non-blocking read."""
		if not self.isopen:
			raise IOError, "Not Open"
		if not blocking:
			self.hiddev.set_nonblocking(1)
		data = self.hiddev.read(numbytes)
		if not blocking:
			self.hiddev.set_nonblocking(0)
		return data

	def send_frame(self, unit, subunit, command, data):
		"""send_frame(unit, subunit, command, data):
		    unit: Target unit # (byte)
			subunit: Target instance # (byte)
			command: Command to deliver to target (byte)
			data: additional data to send on channel to be delivered to target (bytearray)
		Formats a standard frame and sends it on the HID Generic channel. Uses the same data structure as we're
		using for COBS frames."""
		if not self.isopen:
			raise IOError, "Not Open"
		out = ordlist(struct.pack("BBB", unit, subunit, command))
		out.extend(ordlist(data))
		if len(out)>64:
			raise ValueError
		self.send(out)
		
	def set_value(self, unit, subunit, setting, value):
		"""Sends a 'set value' command to the target.
		set_value(unit, subunit, setting, value):
		     Unit: Target Unit # (byte)
			 Subunit: Target instance # (byte)
			 Setting: Which setting to change on the target (uint16)
			 Value: What to set the target setting to (uint16)"""
		command_set_value = 1 
		additional = struct.pack(">HH", setting, value)
		self.send_frame(unit, subunit, command_set_value, additional)
		

	def receive_frame(self, blocking=True):
		"""Receives a frame from the target. Returns a tuple containing the unit, subunit, and a bytestring
		with the remainder of the frame."""
		if not self.isopen:
			raise IOError, "Not Open"
		data = self.receive(64, blocking)
		if len(data) < 3:
			raise IOError, "Invalid Frame: Too short"
		unit = data[0] - 0x80
		if unit < 0:
			raise IOError, "Invalid Frame: Invalid Unit #"
		subunit = data[1]
		additional = data[2:]
		return (unit, subunit, additional)
		
	def get_value(self, unit, subunit, setting):
		"""Sends a 'get value' command to target. Waits for, and receives a return frame containing the requested value.
		get_value(unit, subunit, setting):
		     Unit: Target Unit # (byte)
			 Subunit: Target instance # (byte)
			 Setting: Which setting to change on the target (uint16)
		Returns: The requested value (uint16)"""
		command_get_value = 0 
		additional = struct.pack(">H", setting)
		self.send_frame(unit, subunit, command_get_value, additional)
		runit, rsubunit, radditional = self.receive_frame()
		rsetting, rvalue = struct.unpack(">HH", bytearray(radditional[:4]))
		if unit <> runit or subunit <> rsubunit or setting <> rsetting:		
			raise IOError, "Invalid Frame: data mismatch"			
		return rvalue
		
	def get_serial(self):
		return self.sernum


class NET_ZMQ_Comm(object):
	"""NET_ZMQ_Comm Object:
	  The NET_ZMQ_Comm object is designed to be used from inside the Spark_Control object. 
	  Essentially, it abstracts the ZeroMQ Network communications code to 
	  allow the Spark_Control interface to use any of several communications layers."""
	def __init__(self):
		"""Creates a NET_ZMQ_Comm object - initializing the underlying ZMQ libraty. Creates a ZeroMQ Context"""
		self.context = zmq.Context()
		self.prefix = []
		self.isopen=False

	def open(self, addr):
		"""Opens the underlying ZeroMQ socket and connects to the 'server' end."""
		if self.isopen:
			raise ValueError, "Already Open"
		self.socket = self.context.socket(zmq.XREQ)
		self.socket.connect(addr)
		self.isopen = True

	def close(self):
		"""Closes/Disconnects the underlying ZeroMQ socket and releases the socket to the underlying OS."""
		if not self.isopen:
			raise ValueError, "Not Open"
		self.socket.close()
		self.isopen = False

	def send(self, data, recv=False):
		"""Raw ZMQ send - this is a thin wrapper over the underlying library call. The approach taken
		here fixes up the impedance mismatch between the Spark_Control implementation and the underlying
		communications layer."""
		if not self.isopen:
			raise IOError, "Not Open"
		recvflag = "0"
		if recv == True:
			recvflag = "1"
		base = self.prefix[:]
		base.extend(ordlist(data))
		out = bytearray(base)
		self.socket.send_multipart([out, recvflag])

	def receive(self):
		"""receive(): This is a thin wrapper over the underlying library call. """
		if not self.isopen:
			raise IOError, "Not Open"
		data = self.socket.recv_multipart()
		return data[0]

	def send_frame(self, unit, subunit, command, data, recv = False):
		"""send_frame(unit, subunit, command, data):
		    unit: Target unit # (byte)
			subunit: Target instance # (byte)
			command: Command to deliver to target (byte)
			data: additional data to send on channel to be delivered to target (bytearray)
			recv: Whether to wait for a return frame (True/False)
		Formats a standard frame and sends it on the ZMQ. Uses the same data structure as we're
		using for COBS frames."""
		if not self.isopen:
			raise IOError, "Not Open"
		out = ordlist(struct.pack("BBB", unit, subunit, command))
		out.extend(ordlist(data))
		if len(out)>64:
			raise ValueError
		self.send(out, recv = recv)
		
	def set_value(self, unit, subunit, setting, value):
		"""Sends a 'set value' command to the target.
		set_value(unit, subunit, setting, value):
		     Unit: Target Unit # (byte)
			 Subunit: Target instance # (byte)
			 Setting: Which setting to change on the target (uint16)
			 Value: What to set the target setting to (uint16)"""
		command_set_value = 1 
		additional = struct.pack(">HH", setting, value)
		self.send_frame(unit, subunit, command_set_value, additional)
		
	def receive_frame(self):
		"""Receives a frame from the target. Returns a tuple containing the unit, subunit, and a bytestring
		with the remainder of the frame."""
		if not self.isopen:
			raise IOError, "Not Open"
		data = self.receive()
		if len(data) < 3:
			raise IOError, "Invalid Frame: Too short"
		unit = ord(data[0]) - 0x80
		if unit < 0:
			raise IOError, "Invalid Frame: Invalid Unit #"
		subunit = ord(data[1])
		additional = ordlist(data[2:])
		return (unit, subunit, additional)
		
	def get_value(self, unit, subunit, setting):
		"""Sends a 'get value' command to target. Waits for, and receives a return frame containing the requested value.
		get_value(unit, subunit, setting):
		     Unit: Target Unit # (byte)
			 Subunit: Target instance # (byte)
			 Setting: Which setting to change on the target (uint16)
		Returns: The requested value (uint16)"""
		command_get_value = 0 
		additional = struct.pack(">H", setting)
		self.send_frame(unit, subunit, command_get_value, additional, recv = True)
		runit, rsubunit, radditional = self.receive_frame()
		rsetting, rvalue = struct.unpack(">HH", bytearray(radditional[:4]))
		if unit <> runit or subunit <> rsubunit or setting <> rsetting:		
			raise IOError, "Invalid Frame: data mismatch"			
		return rvalue

		
		
# Stub communications layer
#   The only parts of this class that actualld do anything are the set value and get value functions.
#   set_value sets an internal hash map entry which associates (unit, subunit, setting) with a value.
#   given the same (unit, subunit, setting), get_value returns the value so stored.
#   Useful only for testing/development.

class STUB_Comm(object):
	"""STUB_Comm Object:
	  The STUB_Comm object is designed to be used from inside the Spark_Control object. 
	  Essentially, it fills the role of a communications layer without requiring real hardware."""
	def __init__(self):
		self.prefix = []
		self.vals = {}
		self.isopen=False

	def open(self, addr):
		if self.isopen:
			raise ValueError, "Already Open"
		self.isopen = True

	def close(self):
		if not self.isopen:
			raise ValueError, "Not Open"
		self.isopen = False

	def send(self, data, recv=False):
		pass
		
	def receive(self):
		pass
	
	def send_frame(self, unit, subunit, command, data, recv = False):
		pass
	
	def set_value(self, unit, subunit, setting, value):
		self.vals[(unit, subunit, setting)] = value
	
	def receive_frame(self):
		pass
		
	def get_value(self, unit, subunit, setting):
		return self.vals[(unit, subunit, setting)]

		
class Spark_Drive(object):
	def __init__(self, comm):
		self.comm = comm
		self.unit_loopback = 0
		self.unit_motor = 1
		self.unit_led = 2
		self.unit_servo = 3
		self.unit_adc = 4
		self.unit_ultrasonic = 5
		
		self.setting_pwm = 1
		self.setting_direction = 2
		self.setting_ADC = 3 
		self.setting_USonic = 4 

		self.value_stopped = 0
		self.value_forward = 1
		self.value_reverse = 2
		
		self.command_set = 1
		self.command_read = 0
		
	def set_motor_speed(self, motornum, speed):
		self.comm.set_value(self.unit_motor, motornum, self.setting_pwm, speed) #unit, subu, sett, value
	
	def set_motor_direction(self, motornum, direction):
		self.comm.set_value(self.unit_motor, motornum, self.setting_direction, direction)

	def set_led_brightness(self, lednum, brightness):
		self.comm.set_value(self.unit_led, lednum, self.setting_pwm, brightness)
		
	def set_servo_width(self, servonum, width):
		self.comm.set_value(self.unit_servo, servonum, self.setting_pwm, width)
	
	def get_adc(self, adcnum):
		return self.comm.get_value(self.unit_adc, adcnum, self.setting_ADC)
	
	def get_ultrasonic(self, ultrasonic_num):
		return self.comm.get_value(self.unit_ultrasonic, ultrasonic_num, self.setting_USonic)
