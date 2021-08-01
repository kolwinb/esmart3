import RPi.GPIO as GPIO
import time


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

def setPinRelay(pin):
	GPIO.setup(pin,GPIO.OUT)
	GPIO.output(pin, GPIO.HIGH)
#	GPIO.output(pin, GPIO.LOW)
	print("{} pin : {} on".format(pin,GPIO.input(pin)))

def setPinOff(pin):
	GPIO.setup(pin,GPIO.OUT)
	GPIO.output(pin, GPIO.LOW)
	print("{} pin : {} off".format(pin,GPIO.input(pin)))

#Reset relay board pin
setPinRelay(12)
setPinRelay(16)
setPinRelay(20)
setPinRelay(21)
setPinOff(4)
