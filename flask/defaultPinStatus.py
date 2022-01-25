import RPi.GPIO as GPIO
from time import sleep


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

powerBtn=10

def setPinRelay(pin):
	GPIO.setup(pin,GPIO.OUT)
	GPIO.output(pin, GPIO.HIGH)
#	GPIO.output(pin, GPIO.LOW)
	print("{} pin : {} on".format(pin,GPIO.input(pin)))

def setPinOff(pin):
	GPIO.setup(pin,GPIO.OUT)
	GPIO.output(pin, GPIO.LOW)
	print("{} pin : {} off".format(pin,GPIO.input(pin)))

def setInputPin(pin):
	GPIO.setup(pin,GPIO.IN)


#Reset relay board pin
#setPinRelay(12)
#setPinRelay(16)
#setPinRelay(20)
#setPinRelay(21)
#setPinOff(4)
setInputPin(powerBtn)

while True:
	if (GPIO.input(powerBtn) == True): # Physically read the pin now
		print('0')
	else:
		print('3.3v')
	sleep(1);
