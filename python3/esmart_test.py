#!/usr/bin/python3
# -*- coding: utf-8 -*-

import esmart
import time

def handle_data(d):
	print ("Waiting...")
	# Correct error in readings
	d['bat_volt'] *= 1
	d['load_volt'] *= 1
	# Only correct if reading is not zero
	#if d['chg_cur']:
	#	d['chg_cur'] += 1

	# chg_power uses uncorrected voltage/current, so recalculate
	actual_power = d['bat_volt']*d['chg_cur']

	print("PV :  %.1f V, battery :  %.1f V" % (d['pv_volt'], d['bat_volt']))
	print("Charging :  %s, %.1f A, %.1f W" % (esmart.DEVICE_MODE[d['chg_mode']], d['chg_cur'], actual_power))
	print("Load :  %.1f V, %.1f A, %.1f W" % (d['load_volt'], d['load_cur'], d['load_power']))
	print("battery temp : {}".format(d['bat_temp']))
	print("internal temp : {}".format(d['int_temp']))
	print("battery level : {}".format(d['soc']))
e = esmart.esmart()
e.open("/dev/ttyUSB0")
e.set_callback(handle_data)

while 1:
	e.tick()
	time.sleep(0.001)


