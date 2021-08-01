import RPi.GPIO as GPIO
import time


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
inv=21
#invRelay=20
def setPin(pin):
	GPIO.setup(pin,GPIO.OUT)
	#	GPIO.output(pin, GPIO.HIGH)
	GPIO.output(pin, GPIO.LOW)
	print("{} pin : {} off".format(pin,GPIO.input(pin)))

def setPinRelay(pin):
	GPIO.setup(pin,GPIO.OUT)
	GPIO.output(pin, GPIO.HIGH)
#	GPIO.output(pin, GPIO.LOW)
	print("{} pin : {} off".format(pin,GPIO.input(pin)))

#inverter off
setPinRelay(invRelay)
setPinRelay(inv)
