from api import esmart
from Rpi import RpiPin
import logging
from time import sleep
from datetime import datetime, date, time
import switchon, switchoff

rx570=16
invtMode=17
pc_ac=18
fan=20
hourArr=[8,9,10,11,12,13,14] #handling cloudy day
off=0
on=1

def runRobot(BatCap):

#	chargeLowCycle=0
	
	print ("Battery Level: {}% (low < 50, high > 90)".format(BatCap))
	now=datetime.now()
	print ("Current Date :{}".format(now))
	print ("hour :{}, minute:{}, second:{}".format(now.hour,now.minute,now.second))
#	pinStatus=RpiPin().getPinStatus()
	startTime=now.replace(hour=9,minute=30,second=0,microsecond=0)
	endTime=now.replace(hour=15,minute=0,second=0,microsecond=0)
#	if (( now.hour >= 10 ) and (now.hour < 15)):
	if (( now >= startTime ) and (now < endTime)):
		#inverter line

		if ( BatCap <= 50 ):
#			chargeLowCycle += 1
			RpiPin().setPinState({"inv_serial_21":0})
#			fanOn(0,1)
			RpiPin().setPinState({"fan":1})
#			switchoff.setPin(invtMode) #inverter 230v line
			RpiPin().setPinState({"inv_line_17":0})
#			print ("INFO : batcap < 50 : switch off ac/pc,invtmod,rtx570")
#			checkOtherSwitch(on,off)
#			sleep(5)
			print ("INFO : batcap < 50 : switch on when off state(ac/pc,invtmod,rtx570)")
			checkOtherSwitch(off,on)
#			sleep(10)
#			switchoff.setPin(pc_ac)
#			switchoff.setPin(invtMode)
#			sleep(3)
#			switchon.setPin(pc_ac)

			if now.hour in hourArr: #handling cloudy day
#			if (now.hour < 10) and (chargeLowCycle = 2): #handling cloudy day
				print("at time {} in cloudy time. wait until hour to recover",format(now.hour))
#				chargeLowCycle=0
				sleep(3600)
#			print ("info : Battery Low ({}%)".format(BatCap))
			#send signal to inverter turn off (ongrid on)
		elif (BatCap >= 98):
			RpiPin().setPinState({"inv_serial_21":1})
#			fanOn(0,1) #fan on state
			RpiPin().setPinState({"fan":1})
#			off=0
#			on=1
#			checkOtherSwitch(on,off)
			sleep(5) #delay for inverter initialize
#			switchon.setPin(invtMode) #inverter 230v line
			RpiPin().setPinState({"inv_line_17":1})
			sleep(5) #delay for automatic switch
#			print("INFO:batcap > 98 : switch off ac/pc and rtx570")
#			checkOtherSwitch(on,off)
#			sleep(5)
			print("INFO:batcap > 98 : switch on when off state (ac/pc, invertMode)")
			checkOtherSwitch(off,on)
			print("waiting batcap < 98")
#			sleep(120)
#			switchoff.setPin(pc_ac)
#			sleep(5)
#			switchon.setPin(invtMode)origina
#			switchon.setPin(pc_ac)
#			print ("info : Battery High ({}%)".format(BatCap))
			#send signal to inverter turn on (ongrid off)
#		elif BatCap:
#			checkOtherSwitch()

#	elif (( now.hour == 18 ) and ( now.minute == 28 ) and ( now.second == 0 )):
		#time off (6:28 pm)
#		print ("18:28 pm will shutdown")
#		switchoff.setPin(invtMode)
#		switchoff.setPin(fan)
#		RpiPin().setPinState({"fan":0})
#		switchoff.setPin(pc_ac)
#		switchoff.setPinRelay(rx570)
#	elif (( now.hour == 22 ) and ( now.minute == 31 ) and ( now.second == 0 )):
#		print ("22:31 pm started")
		#time on (10:31 pm)
#		switchon.setPin(fan)
#		RpiPin().setPinState({"fan":1})
#		switchon.setPinRelay(rx570)
#		switchon.setPin(invtMode)
#		sleep(5)
#		switchon.setPin(pc_ac)
	else:
#		pinStatus=RpiPin().getPinStatus()
		#run when reboot the pi
		#this not run
		print ("inverter will not run this time")
		print ("======Inverter=======")
		print ("inverter serial status : {}".format (pinStatus["inv_serial_21"]))
		if (pinStatus["inv_serial_21"] == 1):
			print ("inverter has {} status, will be disabled at this time".format(pinStatus["inv_serial_21"]))

			#inverter will off then ongrid on state.
#			switchoff.setPin(invtMode) #inverter 230v line
#			switchoff.setPin(invSerial)
			RpiPin().setPinState({"inv_serial_21":0}) #data link power controller
#			RpiPin().setPinState({"inv_line_17":0}) #data link power controller
			print ("inverter serial status : {}".format (pinStatus["inv_serial_21"]))
		elif (pinStatus["inv_line_17"] == 1):
			RpiPin().setPinState({"inv_line_17":0}) #data link power controller

		else:
			checkOtherSwitch(0,1)

			#sleep(3)
			#checkOtherSwitch()
#		checkOtherSwitch(1,0)
		#fan controller
#		if (pinStatus["fan"] == 1): #cooling fan
#			RpiPin().setPinState({"fan":0})

def fanOn(off,on):
#	pinStatus=RpiPin().getPinStatus()
	if (pinStatus["fan_20"] == off): #cooling fan
		RpiPin().setPinState({"fan":on})

def checkOtherSwitch(off,on):
#	pinStatus=RpiPin().getPinStatus()

	#inverter line
#	if (pinStatus["pcpower"] == off): #pc_ac relay
#		RpiPin().setPinState({"pcpower":on})
#		sleep(5)

	if (pinStatus["rx570x4_16"] == off):
		RpiPin().setPinState({"rx570x4":on})

	#checing inverter mode enabled or disabled
	if (pinStatus["PC_AC_SSR_power_18"] == off):
		RpiPin().setPinState({"acpower":on}) #ac/pc


#	print ("Current Status: {}".format(pinStatus))

while True:
	pinStatus=RpiPin().getPinStatus()
	ChgSts=esmart()
	try:
		chgData=ChgSts.ctlEsmart(ChgSts.config.getChgSts)
	except:
		print ("array  exception error occured")
	print ("Data : {}".format(chgData))
	BatCap=chgData['BatCap']
	#run other switch if did not run
	#checkOtherSwitch()
	#automate base on battery level
#	runRobot(int(BatCap))
	if pinStatus["powerStatus_10"] == "OK":
		runRobot(int(BatCap))
		print("power ok")
#	elif pinStatus["powerStatus_10"] == "Failure":
#		print("power failure inverter will be switched off")
	elif pinStatus["inv_serial_21"] == 1:
		print("power failure inverter will be switched off")
#		switchoff.setPin(invtMode) #inverter 230v line
#		switchoff.setPin(invSerial) #inverter rs485 off
		RpiPin().setPinState({"inv_serial_21":0}) #data link power controller
		RpiPin().setPinState({"inv_line_17":0}) #data link power controller
	sleep(1)

