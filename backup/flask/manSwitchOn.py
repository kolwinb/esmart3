import RPi.GPIO as GPIO
from time import sleep


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
ac=18
rx570=16
pc=17
fan=20
def setPin(pin):
	GPIO.setup(pin,GPIO.OUT)
	GPIO.output(pin, GPIO.HIGH)
	#GPIO.output(pin, GPIO.LOW)
#	print("{} pin : {} off".format(pin,GPIO.input(pin)))

def setPinRelay(pin):
	GPIO.setup(pin,GPIO.OUT)
#	GPIO.output(pin, GPIO.HIGH)
	GPIO.output(pin, GPIO.LOW)
#	print("{} pin : {} off".format(pin,GPIO.input(pin)))


#setPin(pc)
#sleep (5)
#rx570
setPinRelay(rx570)
#time.sleep(5)
#pc
#ac
setPin(ac)
setPinRelay(fan)
