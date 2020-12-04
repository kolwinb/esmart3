#!/usr/bin/python3

import struct, time, serial, socket, requests
#REQUEST_MSG0 = b"\xaa\x01\x01\x01\x00\x03\x00\x00\x1e\x32"
REQUEST_MSG0 = b"\xaa\x01\x01\x01\x00\x03\x00\x00\x1e\x32"


ser = serial.Serial("/dev/ttyUSB0",9600,timeout=0.1)
ser.port="/dev/ttyUSB0"

print (format(ser.port))
ser.write(REQUEST_MSG0)
data=ser.read(120)

var_data=[]


print ("Serial Read Data : {}".format(data))
for c in data:
	var_data.append(c)
print ("c in data : {}".format(var_data))
fields = {}

print ("packet hex --> decimal 10 base --> decimal 256 base")
print ("x04\xf7 --> 00000100\11110111 --> 4")
print ("packet header : {}".format(var_data[0]))
print ("device id :  var_data[1] = {}".format(var_data[1]))
print ("device address :  var_data[2] = {}".format(var_data[2]))
print ("command : var_data[3] = {}".format(var_data[3]))
print ("data item : var_data[4] = {}".format(var_data[4]))
print ("total data byte length : var_data[5] = {}".format(var_data[5]))

fields['chg_mode'] = int.from_bytes(var_data[8:10], byteorder='little')
print ("chg_mode var_data[8:10]={} -> lowerbit left 0,1 -> 256 base 0*256^1 + 1*256^0 = {}".format(var_data[8:10],fields['chg_mode']))

fields['pv_volt'] = int.from_bytes(var_data[10:12], byteorder='little')/10.0
print ("pv_voltv var_data[10:12]={} --> lowerbit left --> 256 base (4*256^1 + 40*256^0)/10.0 = {}".format(var_data[10:12],fields['pv_volt']))



