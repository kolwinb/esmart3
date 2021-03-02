import RPi.GPIO as GPIO
import time


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
ac=18
rx570=16
pc=17
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

#ac
setPin(ac)
#rx570
setPinRelay(rx570)
#pc
setPin(pc)
