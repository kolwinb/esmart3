from api import esmart
from Rpi import RpiPin
import logging
from time import sleep
from datetime import datetime, date, time


def runRobot(BatCap):
	print ("Battery Level: {}% (low < 50, high > 90)".format(BatCap))
	now=datetime.now()
	print ("Current Date :{}".format(now))
	print ("hour :{}, minute:{}, second:{}".format(now.hour,now.minute,now.second))
	if (( now.hour >= 8 ) and (now.hour < 15)):
		if ( BatCap < 52 ):
			print ("info : Battery Low ({}%)".format(BatCap))
			#send signal to inverter turn off (ongrid on)
			RpiPin().setPinState({"inverter":0})
		elif (BatCap > 90):
			print ("info : Battery High ({}%)".format(BatCap))
			#send signal to inverter turn on (ongrid off)
			RpiPin().setPinState({"inverter":1})
	else:
		pinStatus=RpiPin().getPinStatus()
		if (pinStatus["inverter_serial"] == 1):
			#inverter will off then ongrid on state.
			RpiPin().setPinState({"inverter":0})

def checkOtherSwitch():
	pinStatus=RpiPin().getPinStatus()
	if (pinStatus["acpower"] == 0):
		RpiPin().setPinState({"acpower":1})
	elif (pinStatus["pcpower"] == 0):
		RpiPin().setPinState({"pcpower":1})
	elif (pinStatus["rx570x4"] == 0):
		RpiPin().setPinState({"rx570x4":1})
	print ("Current Status: {}".format(pinStatus))

while True:
	ChgSts=esmart()
	chgData=ChgSts.ctlEsmart(ChgSts.config.getChgSts)
	print ("Data : {}".format(chgData))
	BatCap=chgData['BatCap']
	#run other switch if did not run
	checkOtherSwitch()
	#automate base on battery level
	runRobot(int(BatCap))
	sleep(2)

