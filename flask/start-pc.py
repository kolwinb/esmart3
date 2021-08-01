import RPi.GPIO as GPIO
from time import sleep


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
gigabytePc=4

def press(pin):
	GPIO.setup(pin,GPIO.OUT)
	GPIO.output(pin, GPIO.HIGH)
	print("{} pin : {} press".format(pin,GPIO.input(pin)))

def unpress(pin):
	GPIO.setup(pin,GPIO.OUT)
	GPIO.output(pin, GPIO.LOW)
	print("{} pin : {} unpress".format(pin,GPIO.input(pin)))


#press shutdown button on the computer
press(gigabytePc)
sleep (1)
unpress(gigabytePc)
#time.sleep(5)
