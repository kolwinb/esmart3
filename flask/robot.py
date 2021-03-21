from api import esmart
from Rpi import RpiPin
import logging
from time import sleep
from datetime import datetime, date, time
import switchon, switchoff

def runRobot(BatCap):
	rx570=16
	pc=17
	ac=18
	
	print ("Battery Level: {}% (low < 50, high > 90)".format(BatCap))
	now=datetime.now()
	print ("Current Date :{}".format(now))
	print ("hour :{}, minute:{}, second:{}".format(now.hour,now.minute,now.second))
	if (( now.hour >= 8 ) and (now.hour < 15)):
		checkOtherSwitch()
		if ( BatCap < 52 ):
			print ("info : Battery Low ({}%)".format(BatCap))
			#send signal to inverter turn off (ongrid on)
			RpiPin().setPinState({"inverter":0})
		elif (BatCap > 90):
			print ("info : Battery High ({}%)".format(BatCap))
			#send signal to inverter turn on (ongrid off)
			RpiPin().setPinState({"inverter":1})
	elif (( now.hour == 18 ) and (now.minute == 28) and ( now.second == 0 )):
		#time off (6:28 pm)
		print ("18:28 pm will shutdown")
		switchoff.setPinRelay(rx570)
		switchoff.setPin(pc)
		switchoff.setPin(ac)
	elif (( now.hour == 22 ) and ( now.minute == 31 ) and ( now.second == 0 )):
		print ("22:31 pm started")
		#time on (10:31 pm)
		switchon.setPinRelay(rx570)
		sleep(5)
		switchon.setPin(pc)
		switchon.setPin(ac)
	else:
		pinStatus=RpiPin().getPinStatus()
		if (pinStatus["inverter_serial"] == 1):
			#inverter will off then ongrid on state.
			RpiPin().setPinState({"inverter":0})
			checkOtherSwitch()

def checkOtherSwitch():
	pinStatus=RpiPin().getPinStatus()
	if (pinStatus["acpower"] == 0):
		RpiPin().setPinState({"acpower":1})
	elif (pinStatus["pcpower"] == 0):
		RpiPin().setPinState({"pcpower":1})
	elif (pinStatus["rx570x4"] == 0):
		RpiPin().setPinState({"rx570x4":1})
#	print ("Current Status: {}".format(pinStatus))

while True:
	ChgSts=esmart()
	chgData=ChgSts.ctlEsmart(ChgSts.config.getChgSts)
	print ("Data : {}".format(chgData))
	BatCap=chgData['BatCap']
	#run other switch if did not run
	#checkOtherSwitch()
	#automate base on battery level
	runRobot(int(BatCap))
	sleep(1)

