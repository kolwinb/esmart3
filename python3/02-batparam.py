#!/usr/bin/python3

from settings import Config
import struct, time, serial, socket, requests
import logging

class esmart:
	def __init__(self):
		logging.basicConfig(filename='esmart3.log', level=logging.INFO)
		self.logger = logging.getLogger('esmart3')
		#self.logger.setLevel(logging.DEBUG)
		self.logger.info('Started')

		self.chgMode=["IDLE", "CC", "CV", "FLOAT", "STARTING"]
		self.batType=["User-defined", "Flooded", "Sealed", "Gel"]
		self.fault=[
			"Battery voltage over",
			"PV voltage over",
			"Charge current over",
			"Dis-charge over",
			"Battery temperature alarm",
			"Internal temperature alarm",
			"PV voltage low",
			"Battery voltage low",
			"Trip zero protection trigger",
			"In the control of manual switchgear"
			]
		self.config=Config()
		self.ser = serial.Serial(self.config.dev,9600,timeout=0.1)
		self.ser.port=self.config.dev
#	def __del__(self):
#		self.ser.close()


	def ctlEsmart(self,content):
		MESSAGE=self.readContent(content)
		self.logger.info("MESSAGE : {}".format(MESSAGE))
		self.ser.write(MESSAGE)
		data=self.ser.read(100)
		arrData=[]
		#read each decimal value in recieve message
		for c in data:
			arrData.append(c)
		self.logger.info("recieved data : {}".format(data))
		self.logger.info("value of recieved data : {}".format(arrData))

		#ChgSts Information
		if (arrData[4] == 0):
			'''
			tem=''
			a=ord(b'\xFE')
			b=ord(b'\x04')
			print ("a={},b={}".format(a,b))
			if (a > b):
				temp=a
				a=b
				b=temp
			print ("a={},b={}".format(a,b))
			aa=a*256
			bb=b*1
			c=(aa+bb)/10.0
			print ("c={} V".format(c))
			print ("ChgMode : {}".format(self.chgMode[self.getValue(arrData[8:10])]))
			print ("PV : {} v".format(self.getValue(arrData[10:12])/10.0))
			'''
			print (self.getChgStsJson(arrData))

		elif (arrData[4] == 1):
			print ("BatType : {}".format(self.batType[self.getValue(arrData[10:12])]))

	#build restful json document 
	def getChgStsJson(self,arrData):
		ChargerStatus= {
			"ChgMode" : self.chgMode[self.getValue(arrData[8:10])],
			"InnerTemp" : "{} C".format(self.getValue(arrData[28:30])),
			"CO2" : "{} kg".format(self.getValue(arrData[32:36])/10),
			"PV" : "{} V".format(self.getValue(arrData[10:12])/10),
			"OutVolt" : "{} V".format(self.getValue(arrData[16:18])/10),
			"Fault" : "{}".format(self.getFault(arrData[36:38])),
			"SystemReminder" : "{}".format(self.getValue(arrData[38:40])),
			"Battery" : {
				"BatVolt":"{} V".format(self.getValue(arrData[12:14])/10),
				"ChgCurr":"{} A".format(self.getValue(arrData[14:16])/10),
				"ChgPwr":"{} W".format(self.getValue(arrData[22:24])),
				"BatTemp":"{} C".format(self.getValue(arrData[26:28])),
				"BatCap":"{} %".format(self.getValue(arrData[30:32])),
				},
			"Load" : {
				"LoadVolt":"{} V".format(self.getValue(arrData[18:20])/10),
				"LoadCurr":"{} A".format(self.getValue(arrData[20:22])/10),
				"LoadPower":"{} W".format(self.getValue(arrData[24:26])),
				}
		}
		return ChargerStatus

	#find fault
	def getFault(self,arrData):
		#get Decimal value
		wFault=self.getValue(arrData)
		#convert binary from 'ob100000'
		binary=bin(wFault)[2:]
		print (binary)
		print (len(binary))
		#array begin with 0
		return self.fault[len(binary)-1]

	#convert decimal
	def getValue(self,element):
		return int.from_bytes(element,byteorder='little')

	def readContent(self,content):
		#return content with checksum value
		content=self.addChecksum(content)
		#byte conversion
		byteArray=self.getBytes(content)
		#return content
		self.logger.info("write bit message : {}".format(byteArray))
		return byteArray

	#bytes conversion
	def addChecksum(self,content):
		byteArray=self.getBytes(content)
		checksum=self.getChecksum(byteArray)
		self.logger.info("checksum value : {}".format(checksum))
		#append content array
		content.append(checksum)
		self.logger.info("new content array with checksum value : {}".format(content))
		return content

	#calculate checksum equation
	def getChecksum(self,bytesArray):
		ubChecksum=(0-(sum(bytearray(bytesArray))))&0xFF
		#print(ubChecksum)
		hexChecksum=hex(ubChecksum)
		self.logger.info("sum of hex elements : {} --> {}".format(ubChecksum,hexChecksum))
		return int(hexChecksum,base=16)

	#bytes conversion handler
	def getBytes(self,content):
		self.logger.info("hex element array values : {}".format(content))
		_bytes=bytes(content)
		self.logger.info("bytes conversion : {}".format(_bytes))
		return _bytes


	def getChgSts(self):
		#setup serial connection
		self.setSerialDevice


while 1:
	ChgSts=esmart()
	ChgSts.ctlEsmart(ChgSts.config.ChgSts)
	BatParam=esmart()
	BatParam.ctlEsmart(BatParam.config.BatParam)
	time.sleep(1)
