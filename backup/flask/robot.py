from api import esmart
from Rpi import RpiPin
import logging
from time import sleep
from datetime import datetime, date, time
import switchon, switchoff

def runRobot(BatCap):
	rx570=16
	invtMode=17
	pc_ac=18
	fan=20
	hourArr=[8,9,10,11,12,13,14] #handling cloudy day
	
	print ("Battery Level: {}% (low < 50, high > 90)".format(BatCap))
	now=datetime.now()
	print ("Current Date :{}".format(now))
	print ("hour :{}, minute:{}, second:{}".format(now.hour,now.minute,now.second))
#	pinStatus=RpiPin().getPinStatus()

	if (( now.hour >= 9 ) and (now.hour < 15)):
		#inverter line

		if ( BatCap <= 50 ):
			RpiPin().setPinState({"inverter":0})
#			fanOn(0,1)
			RpiPin().setPinState({"fan":1})
			off=0
			on=1
			switchoff.setPin(invtMode) #inverter 230v line
			print ("INFO : batcap < 50 : switch off ac/pc,invtmod,rtx570")
			checkOtherSwitch(on,off)
#			sleep(5)
			print ("INFO : batcap < 50 : switch on ac/pc,invtmod,rtx570")
			checkOtherSwitch(off,on)
#			sleep(10)
#			switchoff.setPin(pc_ac)
#			switchoff.setPin(invtMode)
#			sleep(3)
#			switchon.setPin(pc_ac)

			if now.hour in hourArr: #handling cloudy day
				print("at time {} in cloudy time. wait until hour to recover",now.hour)
				sleep(3600)
#			print ("info : Battery Low ({}%)".format(BatCap))
			#send signal to inverter turn off (ongrid on)
		elif (BatCap > 98):
			RpiPin().setPinState({"inverter":1})
#			fanOn(0,1) #fan on state
			RpiPin().setPinState({"fan":1})
			off=0
			on=1
#			checkOtherSwitch(on,off)
			sleep(5) #delay for inverter initialize
			switchon.setPin(invtMode) #inverter 230v line
			sleep(5) #delay for automatic switch
			print("INFO:batcap > 98 : switch off ac/pc and rtx570")
			checkOtherSwitch(on,off)
#			sleep(5)
			print("INFO:batcap > 98 : switch on ac/pc, invertMode")
			checkOtherSwitch(off,on)
			print("waiting batcap < 98")
#			sleep(120)
#			switchoff.setPin(pc_ac)
#			sleep(5)
#			switchon.setPin(invtMode)
#			switchon.setPin(pc_ac)
#			print ("info : Battery High ({}%)".format(BatCap))
			#send signal to inverter turn on (ongrid off)
#		elif BatCap:
#			checkOtherSwitch()

	elif (( now.hour == 18 ) and ( now.minute == 28 ) and ( now.second == 0 )):
		#time off (6:28 pm)
		print ("18:28 pm will shutdown")
#		switchoff.setPin(invtMode)
#		switchoff.setPin(fan)
#		RpiPin().setPinState({"fan":0})
#		switchoff.setPin(pc_ac)
#		switchoff.setPinRelay(rx570)
	elif (( now.hour == 22 ) and ( now.minute == 31 ) and ( now.second == 0 )):
		print ("22:31 pm started")
		#time on (10:31 pm)
#		switchon.setPin(fan)
#		RpiPin().setPinState({"fan":1})
#		switchon.setPinRelay(rx570)
#		switchon.setPin(invtMode)
#		sleep(5)
#		switchon.setPin(pc_ac)
	else:
		pinStatus=RpiPin().getPinStatus()
		if (pinStatus["inverter_serial"] == 1):
			#inverter will off then ongrid on state.
			switchoff.setPin(invtMode) #inverter 230v line
			RpiPin().setPinState({"inverter":0}) #data link power controller
			#sleep(3)
			#checkOtherSwitch()
#		checkOtherSwitch(1,0)
		#fan controller
#		if (pinStatus["fan"] == 1): #cooling fan
#			RpiPin().setPinState({"fan":0})

def fanOn(off,on):
	pinStatus=RpiPin().getPinStatus()
	if (pinStatus["fan"] == off): #cooling fan
		RpiPin().setPinState({"fan":on})

def checkOtherSwitch(off,on):
	pinStatus=RpiPin().getPinStatus()

	#inverter line
#	if (pinStatus["pcpower"] == off): #pc_ac relay
#		RpiPin().setPinState({"pcpower":on})
#		sleep(5)

	if (pinStatus["rx570x4"] == off):
		RpiPin().setPinState({"rx570x4":on})

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
	sleep(1)

