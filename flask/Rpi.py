import RPi.GPIO as GPIO
from time import sleep

class RpiPin():
	def __init__(self):
		self.acpin=18
		self.pcpin=17
		self.inverter=4
		self.rx570x4=16

	def setPinConfi(self,pin):
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(pin,GPIO.OUT)

	def setPinState(self,data):
		for key,val in data.items():
			if (key == "inverter"):
				self.setGpioOutState(self.inverter,val)
			elif (key == "acpower"):
				self.setGpioOutState(self.acpin,val)
			elif (key == "pcpower"):
				self.setGpioOutState(self.pcpin,val)
			elif (key == "rx570x4"):
				self.setGpioOutState(self.rx570x4,val)

		return self.getPinStatus()

	#enable/disable state of pin
	def setGpioOutState(self,pin,val):
		self.setPinConfi(pin)
		print(val)
		GPIO.output(pin,int(val))

	#read pin status
	def readPin(self,pin):
		self.setPinConfi(pin)
		return GPIO.input(pin)


	def getPinStatus(self):
		data = {
			'inverter':self.readPin(self.inverter),
			'acpower':self.readPin(self.acpin),
			'pcpower':self.readPin(self.pcpin)

			}
		return data
