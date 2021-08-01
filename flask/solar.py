from api import esmart
from Rpi import RpiPin
import logging
from time import sleep
from datetime import datetime, date, time
import switchon, switchoff

interval=5

def runRobot(BatCap):
	rx570=16
	invtMode=17
	pc_ac=18
	fan=20
	hourArr=[8,9,10,11,12,13,14,15] #handling cloudy day
	invCutOff=50
	invOver=80
	print ("Battery Level: {}% (low < 50, high > 90)".format(BatCap))
	now=datetime.now()
	print ("Current Date :{}".format(now))
	print ("hour :{}, minute:{}, second:{}".format(now.hour,now.minute,now.second))
#	pinStatus=RpiPin().getPinStatus()
	index=0
	if (( now.hour >= 11 ) and (now.hour < 16)):
		#inverter line

		if ( BatCap <= invCutOff ):
			index=0
			RpiPin().setPinState({"inverter":0})
#			RpiPin().setPinState({"fan":1})
			off=0
			on=1
			switchoff.setPin(invtMode) #inverter 230v line
			fanOn(0,1)
#			print ("INFO : batcap < 50 : switch off ac/pc,invtmod,rtx570")
#			checkOtherSwitch(on,off)
#			sleep(5)
			print ("INFO : batcap < 50 : switch on ac/pc,invtmod,rtx570")
			checkOtherSwitch(off,on)

			if now.hour in hourArr: #handling cloudy day
				print("at time {} in cloudy time. wait until hour to recover",now.hour)
				sleep(3600)

		elif (BatCap > invOver):
#			if ( index == 0 ):
				RpiPin().setPinState({"inverter":1})
#				RpiPin().setPinState({"fan":1})
				off=0
				on=1
	#			checkOtherSwitch(on,off)
#				sleep(5) #delay for inverter initialize
				switchon.setPin(invtMode) #inverter 230v line
				fanOn(0,1) #fan on state
#				sleep(5) #delay for automatic switch
#				print("INFO:batcap > 98 : switch off ac/pc and rtx570")
#				checkOtherSwitch(on,off)
#				sleep(5)
				print("INFO:batcap > 80 : switch on ac/pc, invertMode")
				checkOtherSwitch(off,on)
				print("waiting batcap < 80")
#				sleep(600)
#			else:
#				index=index+1
	else:
		fanOn(1,0)
#		RpiPin().setPinState({"fan":1})
		pinStatus=RpiPin().getPinStatus()
		if (pinStatus["inverter_serial"] == 1):
			#inverter will off then ongrid on state.
			switchoff.setPin(invtMode) #inverter 230v line
			RpiPin().setPinState({"inverter":0}) #data link power controller

def fanOn(off,on):
	pinStatus=RpiPin().getPinStatus()
	if (pinStatus["fan"] == off): #cooling fan
		RpiPin().setPinState({"fan":on})
	if (pinStatus["rx570x4"] == off):
		RpiPin().setPinState({"rx570x4":on})

def checkOtherSwitch(off,on):
	pinStatus=RpiPin().getPinStatus()
	#checing inverter mode enabled or disabled
	if (pinStatus["acpower"] == off):
		RpiPin().setPinState({"acpower":on}) #ac/pc


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
	sleep(interval)

