from Rpi import RpiPin
import time

pinStatus=RpiPin().getPinStatus()
print ("{}".format(pinStatus))

