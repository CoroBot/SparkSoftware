#!/usr/bin/env python

import zmq
import sys
from Spark_Control import HID_Comm

def main():
	ctx = zmq.Context()
	comm = HID_Comm()
	comm.open()
	zsock = ctx.socket(zmq.XREP)
	zsock.bind("tcp://*:4567")
	while (True):
		indat = zsock.recv_multipart()
		origin = indat[0]
		frame = bytearray(indat[1])
		replyflag = indat[2]
		comm.send(frame)
		print "B"
		if replyflag == "1":
			replydata = comm.receive()
			zsock.send_multipart([origin, bytearray(replydata)])

if __name__ == '__main__':
	main()

