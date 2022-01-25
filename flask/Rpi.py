import RPi.GPIO as GPIO
from time import sleep

class RpiPin():
	def __init__(self):
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		self.pc_ac_ssr_pin=18
		self.inv_ssr_pin=17
		self.inv_serial=21
		self.fan=20
		self.rx570x4=16
		self.pcShutdown=4
		self.powerStatus=10
		GPIO.setup(self.powerStatus,GPIO.IN)
		self.setGpioOutState(self.pc_ac_ssr_pin,1)
		#default position this will refresh if you browser refresh
		#put crontab to default 1 in inverter and rx570x4
#		self.data={"inverter":"0","rx570x4":"0"}
#		self.setPinState(self.data)


	def setPinConfi(self,pin):
		GPIO.setup(pin,GPIO.OUT)

	def setPinState(self,data):
		for key,val in data.items():
			if (key == "inv_line_17"):
				#this pin should be inverse
				#invt mode on
				self.setGpioOutState(self.inv_ssr_pin,int(val))
#				self.setGpioOutState(self.fan,int(val))
				#delay to swith relay between interter-->load
#				if (val == 1):
#					self.setGpioOutState(self.invRelay,self.setRelayPinOut(int(val)))
#				else:
				#sleep(5)
			elif (key == "inv_serial_21"):
				self.setGpioOutState(self.inv_serial,self.setRelayPinOut(int(val)))
			elif (key == "acpower"):
				self.setGpioOutState(self.pc_ac_ssr_pin,int(val))
			elif (key == "pcpower"):
				self.setGpioOutState(self.inv_ssr_pin,int(val))
			elif (key == "rx570x4"):
				#this pin should be inverse
				self.setGpioOutState(self.rx570x4,self.setRelayPinOut(int(val)))
			elif (key == "fan"):
				#this pin should be inverse
				self.setGpioOutState(self.fan,self.setRelayPinOut(int(val)))
			elif (key == "shutdownPc"):
				#this pin should be inverse
				self.setGpioOutState(self.pcShutdown,int(val))
				sleep(4)
				self.setGpioOutState(self.pcShutdown,0)

			elif (key == "startPc"):
				#this pin should be inverse
				self.setGpioOutState(self.pcShutdown,int(val))
				sleep(1)
				self.setGpioOutState(self.pcShutdown,0)

		return self.getPinStatus()

	#enable/disable state of pin
	def setGpioOutState(self,pin,val):
		self.setPinConfi(pin)
		print("Rpi:GPIO "+str(pin)+" : "+str(val))
		GPIO.output(pin,val)

	#read pin status
	def readPin(self,pin):
		self.setPinConfi(pin)
		return GPIO.input(pin)

	def getPowerStatus(self):
		if GPIO.input(self.powerStatus) == False:
			return "OK"
		else:
			return "Failure"

	def getPinStatus(self):
		data = {
			'PC_AC_SSR_power_18':self.readPin(self.pc_ac_ssr_pin),
			'inv_line_17':self.readPin(self.inv_ssr_pin),
			'inv_serial_21':self.setRelayPinOut(self.readPin(self.inv_serial)),
			'fan_20':self.setRelayPinOut(self.readPin(self.fan)),
			'rx570x4_16':self.setRelayPinOut(self.readPin(self.rx570x4)),
			'shutdownPc_4':self.readPin(self.pcShutdown),
			'startPc_4':self.readPin(self.pcShutdown),
			'powerStatus_10':self.getPowerStatus()
			}
		return data

	#mechanical relay board only switch on when input 0 (zero)
	#we need to change 0 to 1 to front end to show switch status
	def setRelayPinOut(self, pinStatus):
		if (pinStatus == 0):
			return 1
		elif (pinStatus == 1):
			return 0

