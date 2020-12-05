#!/usr/bin/python3

class Config:
	def __init__(self, **kwds):
		self.__dict__.update(kwds)
		self.dev="/dev/ttyUSB0"
		self.chgMode=["IDLE", "CC", "CV", "FLOAT", "STARTING"]
		self.batType=["User-defined", "Flooded", "Sealed", "Gel"]
		self.batSys=["Auto","1*12V","2*12V","3*12V","4*12V"]
		self.loadSwitchStatus=["Shutdown", "Open"]
		self.enableTimeTwo=["Closing time 2 settings","Opening period 2 settings"]
		self.tempParam=["Centigrade","Fahrenheit"]

		#Fixed time-light control mode:
		self.periodOne={
			5100:"Light control delay mode. (Start Voltage, Closed Voltage)",
			5101:"Light control opens the load and closes 1 hours later.",
			5102:"Light control opens the load and closes 2 hours later.",
			5103:"Light control opens the load and closes 3 hours later.",
			5104:"Light control opens the load and closes 4 hours later.",
			5105:"Light control opens the load and closes 5 hours later.",
			5106:"Light control opens the load and closes 6 hours later.",
			5107:"Light control opens the load and closes 7 hours later.",
			5108:"Light control opens the load and closes 8 hours later.",
			5109:"Light control opens the load and closes 9 hours later.",
			5110:"Light control opens the load and closes 10 hours later.",
			5111:"Light control opens the load and closes 11 hours later.",
			5112:"Light control opens the load and closes 12 hours later.",
			5113:"Light control opens the load and closes 13 hours later.",
			5114:"Light control opens the load and closes 14 hours later.",
			5115:"Light control opens the load and closes 15 hours later.",
			5116:"Turn-on Time1: Turn-off Time1: (Dual Timer Mode)",
			5117:"Normally open state. (Manual switching mode)",
			5118:"Normally close state. (Manual switching mode)",
			}

		self.periodTwo={
			5200:"Light control delay mode. (Start Voltage, Closed Voltage)",
			5201:"Light control opens the load and closes 1 hours later.",
			5202:"Light control opens the load and closes 2 hours later.",
			5203:"Light control opens the load and closes 3 hours later.",
			5204:"Light control opens the load and closes 4 hours later.",
			5205:"Light control opens the load and closes 5 hours later.",
			5206:"Light control opens the load and closes 6 hours later.",
			5207:"Light control opens the load and closes 7 hours later.",
			5208:"Light control opens the load and closes 8 hours later.",
			5209:"Light control opens the load and closes 9 hours later.",
			5210:"Light control opens the load and closes 10 hours later.",
			5211:"Light control opens the load and closes 11 hours later.",
			5212:"Light control opens the load and closes 12 hours later.",
			5213:"Light control opens the load and closes 13 hours later.",
			5214:"Light control opens the load and closes 14 hours later.",
			5215:"Light control opens the load and closes 15 hours later.",
			}

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

		self.device = {
			'typeAll':0x00,
			'type':0x01,
			'addrAll':0x00,
			'addr':0x01
		}

		self.command =  {
			'CMD_ACK':0x00,
			'CMD_GET':0x01,
			'CMD_SET':0x02,
			'CMD_SET_NO_RESP':0x03,
			'CMD_NACK':0x04,
			'CMD_EXEC':0x05,
			'CMD_ERR':0x7F
		}

		#length of dataitem may differ
		#30=0x1e,
		#20=0x14,
		#50=0x32,
		#6=0x06,
		#14=0x0e,
		#8=0x08,
		#12=0x0c,
		#10=0x0a

		self.commandItem = {
			'db_ChgSts':{'dataItem':0x00,'length':0x20},
			'db_BatParam':{'dataItem':0x01,'length':0x16},
			'db_Log':{'dataItem':0x02,'length':0x32},
			'db_parameters':{'dataItem':0x03,'length':0x1a},
			'db_LoadParam':{'dataItem':0x04,'length':0x24},
			'db_ChgDebug':{'dataItem':0x05,'length':0x1e},
			'db_remoteControl':{'dataItem':0x06,'length':0x14},
			'db_ProParam':{'dataItem':0x07,'length':0x0e},
			'db_Information':{'dataItem':0x08,'length':0x28},
			'db_TempParam':{'dataItem':0x09,'length':0x0c},
			'db_EngSave':{'dataItem':0x10,'length':0x0a},

		}

		self.getTempParam=[
			0xaa,
			self.device['type'],
			self.device['addr'],
			self.command['CMD_GET'],
			self.commandItem['db_TempParam']['dataItem'],
			0x03,
			0x00,
			0x00,
			self.commandItem['db_TempParam']['length']
		]

		self.getChgSts=[
			0xaa,
			self.device['type'],
			self.device['addr'],
			self.command['CMD_GET'],
			self.commandItem['db_ChgSts']['dataItem'],
			0x03,
			0x00,
			0x00,
			self.commandItem['db_ChgSts']['length']
		]

		self.getBatParam=[
			0xaa,
			self.device['type'],
			self.device['addr'],
			self.command['CMD_GET'],
			self.commandItem['db_BatParam']['dataItem'],
			0x03,
			0x00,
			0x00,
			self.commandItem['db_BatParam']['length']
		]

		self.getLog=[
			0xaa,
			self.device['type'],
			self.device['addr'],
			self.command['CMD_GET'],
			self.commandItem['db_Log']['dataItem'],
			0x03,
			0x00,
			0x00,
			self.commandItem['db_Log']['length']
		]

		self.getParameters=[
			0xaa,
			self.device['type'],
			self.device['addr'],
			self.command['CMD_GET'],
			self.commandItem['db_parameters']['dataItem'],
			0x03,
			0x00,
			0x00,
			self.commandItem['db_parameters']['length']
		]

		self.getLoadParam=[
			0xaa,
			self.device['type'],
			self.device['addr'],
			self.command['CMD_GET'],
			self.commandItem['db_LoadParam']['dataItem'],
			0x03,
			0x00,
			0x00,
			self.commandItem['db_LoadParam']['length']
		]

		self.getChgDebug=[
			0xaa,
			self.device['type'],
			self.device['addr'],
			self.command['CMD_GET'],
			self.commandItem['db_ChgDebug']['dataItem'],
			0x03,
			0x00,
			0x00,
			self.commandItem['db_ChgDebug']['length']
		]

		self.getRemoteControl=[
			0xaa,
			self.device['type'],
			self.device['addr'],
			self.command['CMD_GET'],
			self.commandItem['db_remoteControl']['dataItem'],
			0x03,
			0x00,
			0x00,
			self.commandItem['db_remoteControl']['length']
		]

		self.getProParam=[
			0xaa,
			self.device['type'],
			self.device['addr'],
			self.command['CMD_GET'],
			self.commandItem['db_ProParam']['dataItem'],
			0x03,
			0x00,
			0x00,
			self.commandItem['db_ProParam']['length']
		]

		self.getInformation=[
			0xaa,
			self.device['type'],
			self.device['addr'],
			self.command['CMD_GET'],
			self.commandItem['db_Information']['dataItem'],
			0x03,
			0x00,
			0x00,
			self.commandItem['db_Information']['length']
		]

		self.getTempParam=[
			0xaa,
			self.device['type'],
			self.device['addr'],
			self.command['CMD_GET'],
			self.commandItem['db_TempParam']['dataItem'],
			0x03,
			0x00,
			0x00,
			self.commandItem['db_TempParam']['length']
		]

		self.getEngSave=[
			0xaa,
			self.device['type'],
			self.device['addr'],
			self.command['CMD_GET'],
			self.commandItem['db_EngSave']['dataItem'],
			0x03,
			0x00,
			0x00,
			self.commandItem['db_EngSave']['length']
		]
