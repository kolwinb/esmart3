import RPi.GPIO as GPIO

class Rpi:
	def __init__(self,pin):
		print('__init__ pin: {}'.format(pin))
		self.pin=pin
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.pin,GPIO.OUT)


	#enable/disable state of pin
	def setGpioOutState(self,state):
		GPIO.output(self.pin, state)

#ac=Rpi(18)
#pc=Rpi(17)
#on
#ac.setGpioOutState(0)
#pc.setGpioOutState(0)
