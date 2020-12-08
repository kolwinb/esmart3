import RPi.GPIO as GPIO
import time

ledPin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin,GPIO.OUT)
GPIO.output(ledPin, GPIO.HIGH)

