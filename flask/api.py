#!/usr/bin/python3

from settings import Config
import struct, time, serial, socket, requests
import logging

from Rpi import RpiPin

class esmart:
	def __init__(self):
		#logging.basicConfig(filename='esmart3.log', level=logging.INFO)
		#self.logger = logging.getLogger('esmart3')
		#self.logger.setLevel(logging.DEBUG)
		#self.logger.info('Started')
		self.config=Config()
		self.ser = serial.Serial(self.config.dev,9600,timeout=0.1)
		self.ser.port=self.config.dev
		self.varBatCap=0
#	def __del__(self):
#		self.ser.close()


	def ctlEsmart(self,content):
		MESSAGE=self.readContent(content)
		#self.logger.info("MESSAGE : {}".format(MESSAGE))
		self.ser.write(MESSAGE)
		data=self.ser.read(100)
		arrData=[]
		#read each decimal value in recieve message
		for c in data:
			arrData.append(c)
		#self.logger.info("recieved data : {}".format(data))
		#self.logger.info("value of recieved data : {}".format(arrData))

		if (arrData[4] == 0):
			return (self.getChgStsJson(arrData))
		elif (arrData[4] == 1):
			return (self.getBatParamJson(arrData))
		elif (arrData[4] == 2):
			return (self.getLogJson(arrData))
		elif (arrData[4] == 3):
			return (self.getParametersJson(arrData))
		elif (arrData[4] == 4):
			return (self.getLoadParamJson(arrData))
		elif (arrData[4] == 5):
			return (self.getChgDebugJson(arrData))
		elif (arrData[4] == 6):
			return (self.getRemoteControlJson(arrData))
		elif (arrData[4] == 7):
			return (self.getProParamJson(arrData))
		elif (arrData[4] == 8):
			return (self.getInformationJson(arrData))
		elif (arrData[4] == 9):
			return (self.getTempParamJson(arrData))
		elif ((arrData[4] == 10) and (arrData[6] == 1)):
			return (self.getMonthPowerJson(arrData))
#		elif (arrData[4] == 10):
#			return (self.getEngSaveJson(arrData))


	#Charger stats json document 
	def getChgStsJson(self,arrData):
		self.varBatCap=self.getValue(arrData[30:32])
		ChargerStatus= {
			"ChgMode" : self.config.chgMode[self.getValue(arrData[8:10])],
			"InnerTemp" : "{}C".format(self.getValue(arrData[28:30])),
			"CO2" : "{}kg".format((self.getValue(arrData[32:34]) + self.getValue(arrData[34:36]))/10),
			"PV" : "{}V".format(self.getValue(arrData[10:12])/10),
			"OutVolt" : "{}V".format(self.getValue(arrData[16:18])/10),
			"Fault" : "{}".format(self.getFault(arrData[36:38])),
			"SystemReminder" : "{}".format(self.getValue(arrData[38:40])),
#			"Other" : "{}".format(self.getValue(arrData[40:42])),
			#"Battery" : {
			"BatVolt":"{}V".format(self.getValue(arrData[12:14])/10),
			"ChgCurr":"{}A".format(self.getValue(arrData[14:16])/10),
			"ChgPwr":"{}W".format(self.getValue(arrData[22:24])),
			"BatTemp":"{}C".format(self.getValue(arrData[26:28])),
			"BatCap":"{}%".format(self.varBatCap),
		 	#	},
			#"Load" : {
			"LoadVolt":"{}V".format(self.getValue(arrData[18:20])/10),
			"LoadCurr":"{}A".format(self.getValue(arrData[20:22])/10),
			"LoadPower":"{}W".format(self.getValue(arrData[24:26])),
			#	}
		}

		return ChargerStatus

	def setAutoPower(self):
		#make threhold to switch off pc
		if ( self.varBatCap <= 50 ):
			print("automatically switch off pcpower <= 50%")
			RpiPin().setPinState({"pcpower":0})
			#RpiPin().setPinState({"acpower":1})
		elif ( self.varBatCap >= 60 ):
			pinData=RpiPin().getPinStatus()
			if (pinData.get('pcpower') == 0):
				print("automatically switch on pcpower >= 65%")
				RpiPin().setPinState({"pcpower":1})
				#RpiPin().setPinState({"acpower":1})


	def getBatParamJson(self,arrData):
		page={
			"Flag":"{}".format(self.getValue(arrData[8:10])),
			"Battery Type":"{}".format(self.config.batType[self.getValue(arrData[10:12])]),
			"Battery system":"{}".format(self.config.batSys[self.getValue(arrData[12:14])]),
			"Bulk voltage":"{}V".format(self.getValue(arrData[14:16])*0.1),
			"Float voltage":"{}V".format(self.getValue(arrData[16:18])*0.1),
			"Charge current limit":"{}A".format(self.getValue(arrData[18:20])*0.1),
			"DisCharge (Load) current limit":"{}A".format(self.getValue(arrData[20:22])*0.1),
			"Activation charge voltage":"{}V".format(self.getValue(arrData[22:24])*0.1),
			"Activation charge time":"{}min".format(self.getValue(arrData[24:26])),
			"Load utilization":"{}%".format(self.getValue(arrData[26:28])),
		}
		return page

	def getLogJson(self,arrData):
		page={
            "Flag":"{}".format(self.getValue(arrData[8:10])),
			"RunTime":"{}min".format(self.getValue(arrData[10:14])),
			"StartCnt":"{}".format(self.getValue(arrData[14:16])),
			"LastFaultInfo":"{}".format(self.getValue(arrData[16:18])),
			"FaultCnt":"{}".format(self.getValue(arrData[18:20])),
			"PVTodayEng":"{} wh".format(self.getValue(arrData[20:22]) + self.getValue(arrData[22:24])),
			"TodayEngDate":"{}".format(self.getValue(arrData[24:26]) + self.getValue(arrData[26:28])),
			"PVMonthEng":"{} kwh".format(self.getValue(arrData[28:30]) + self.getValue(arrData[30:32])/1000),
			"MonthEngDate":"{}".format(self.getValue(arrData[32:34]) + self.getValue(arrData[34:36])),
			"PVTotalEng":"{} kwh".format(self.getValue(arrData[36:38]) + self.getValue(arrData[38:40])/1000),
			"LoadTodayEng":"{} wh".format(self.getValue(arrData[40:42]) + self.getValue(arrData[42:44])),
			"LoadMonthEng":"{} kwh".format(self.getValue(arrData[44:46]) + self.getValue(arrData[46:48])/1000),
			"LoadTotalEng":"{} kwh".format(self.getValue(arrData[48:50]) + self.getValue(arrData[50:52])/1000),
			"BacklightTime":"{}S".format(self.getValue(arrData[52:54])),
			"SwitchEnable":"{}".format(self.getValue(arrData[54:56])),
		}
		return page

	#internal use only
	def getParametersJson(self,arrData):
		page={
			"Flag":"{}".format(self.getValue(arrData[8:10])),
			"PvVoltRatio":"{}".format(self.getValue(arrData[10:12])),
			"PvVoltOffset":"{}".format(self.getValue(arrData[12:14])),
			"BatVoltRatio":"{}".format(self.getValue(arrData[14:16])),
			"BatVoltOffset":"{}".format(self.getValue(arrData[16:18])),
			"ChgCurrRatio":"{}".format(self.getValue(arrData[18:20])),
			"ChgCurrOffset":"{}".format(self.getValue(arrData[20:22])),
			"LoadCurrRatio":"{}".format(self.getValue(arrData[22:24])),
			"LoadCurrOffset":"{}".format(self.getValue(arrData[24:26])),
			"LoadVoltRatio":"{}".format(self.getValue(arrData[26:28])),
			"LoadVoltOffset":"{}".format(self.getValue(arrData[28:30])),
			"OutVoltRatio":"{}".format(self.getValue(arrData[30:32])),
			"OutVoltOffset":"{}".format(self.getValue(arrData[32:34])),

		}
		return page

	def getLoadParamJson(self,arrData):
		page={
			"Flag":"{}".format(self.getValue(arrData[8:10])),
			"Load Module 1":"{}".format(self.config.periodOne[self.getValue(arrData[10:12])]),
			"Load Module 2":"{}".format(self.config.periodTwo[self.getValue(arrData[12:14])]),
			"Turn on the loads PV voltage":"{}V".format(self.getValue(arrData[14:16])*0.1),
			"Turn off the loads PV voltage":"{}V".format(self.getValue(arrData[16:18])*0.1),
			"Open the light-control load time delay":"{}min".format(self.getValue(arrData[18:20])),
			"Close the light-control load time delay":"{}min".format(self.getValue(arrData[20:22])),
			"Open the load time in the evening":"{}".format(self.getValue(arrData[22:24]) + self.getValue(arrData[24:26])),
			"Close the load in the evening":"{}".format(self.getValue(arrData[26:28]) + self.getValue(arrData[28:30])),
			"Open the load in the morning":"{}".format(self.getValue(arrData[30:32]) + self.getValue(arrData[32:34])),
			"Close the load in the morning":"{}".format(self.getValue(arrData[34:36]) + self.getValue(arrData[36:38])),
			"Load switch status":"{}".format(self.config.loadSwitchStatus[self.getValue(arrData[38:40])]),
			"Enable Time 2":"{}".format(self.config.enableTimeTwo[self.getValue(arrData[40:42])]),
		}
		return page

	def getChgDebugJson(self,arrData):
		page={}
		return page

	def getRemoteControlJson(self,arrData):
		page={
			"MagicNum":"{}".format(self.getValue(arrData[8:10])),
			"eRemoteCommand":"{}".format(self.getValue(arrData[10:12])),
			"uwData":"{}".format(self.getValue(arrData[12:14]) + self.getValue(arrData[14:16]) + self.getValue(arrData[16:18])),

		}
		return page

	def getProParamJson(self,arrData):
		page={
			"Flag":"{}".format(self.getValue(arrData[8:10])),
			"Load overvoltage protection":"{}V".format(self.getValue(arrData[10:12])*0.1),
			"Load low protection":"{}V".format(self.getValue(arrData[12:14])*0.1),
			"Load protection of battery":"{}V".format(self.getValue(arrData[14:16])*0.1),
			"Battery overvoltage recovery point":"{}V".format(self.getValue(arrData[16:18])*0.1),
			"Battery low voltage protection":"{}V".format(self.getValue(arrData[18:20])*0.1),

		}
		return page

	def getInformationJson(self,arrData):
		page={
			"Flag":"{}".format(self.getValue(arrData[8:10])),
			"Serial number":"{}".format(self.getValue(arrData[10:26])),
			"Version number":"{}".format(self.getValue(arrData[26:30])),
			"Model":"{}".format(self.getValue(arrData[30:46])),
		}
		return page

	def getTempParamJson(self,arrData):
		page={
			"Flag":"{}".format(self.getValue(arrData[8:10])),
			"TempSel":"{}".format(self.config.tempParam[self.getValue(arrData[16:18])]),

		}
		return page

	def getEngSaveJson(self,arrData):
		page={
			"Flag":"{}".format(self.getValue(arrData[8:10])),
			"Power":"{}".format(self.getValue(arrData[10:12])),

		}
		return page

	def getMonthPowerJson(self,arrData):

		#kw calculation (4 bytes = 2 bytes + 2 bytes = kw)
		page={}
		inPoint=8
		for month in self.config.month:
			outPoint=inPoint+2
			b_inPoint=outPoint
			b_outPoint=outPoint+2
			page[month]=self.getValue(arrData[inPoint:outPoint]) + self.getValue(arrData[b_inPoint:b_outPoint])
			inPoint=b_outPoint
			#outPoint=inPoint+2
			#page[month]=int.from_bytes(arrData[inPoint:outPoint],byteorder='little',signed=False)
			#inPoint=outPoint
		return page

	#find fault
	def getFault(self,arrData):
		#get Decimal value
		wFault=self.getValue(arrData)
		#convert binary from 'ob100000'
		binary=bin(wFault)[2:]
		print (binary)
		print (len(binary))
		#array begin with 0
		return self.config.fault[len(binary)-1]

	#convert decimal
	def getValue(self,element):
		return int.from_bytes(element,byteorder='little')

	def readContent(self,content):
		#return content with checksum value
		content=self.addChecksum(content)
		#byte conversion
		byteArray=self.getBytes(content)
		#return content
		#self.logger.info("write bit message : {}".format(byteArray))
		return byteArray

	#bytes conversion
	def addChecksum(self,content):
		byteArray=self.getBytes(content)
		checksum=self.getChecksum(byteArray)
		#self.logger.info("checksum value : {}".format(checksum))
		#append content array
		content.append(checksum)
		#self.logger.info("new content array with checksum value : {}".format(content))
		return content

	#calculate checksum equation
	def getChecksum(self,bytesArray):
		ubChecksum=(0-(sum(bytearray(bytesArray))))&0xFF
		#print(ubChecksum)
		hexChecksum=hex(ubChecksum)
		#self.logger.info("sum of hex elements : {} --> {}".format(ubChecksum,hexChecksum))
		return int(hexChecksum,base=16)

	#bytes conversion handler
	def getBytes(self,content):
		#self.logger.info("hex element array values : {}".format(content))
		_bytes=bytes(content)
		#self.logger.info("bytes conversion : {}".format(_bytes))
		return _bytes


	def getChgSts(self):
		#setup serial connection
		self.setSerialDevice

'''
	def defMain():
		while 1:
			ChgSts=esmart()
			ChgSts.ctlEsmart(ChgSts.config.ChgSts)
			BatParam=esmart()
			BatParam.ctlEsmart(BatParam.config.BatParam)
			time.sleep(1)
'''
