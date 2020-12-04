#!/usr/bin/python3

class Config:
	def __init__(self, **kwds):
		self.__dict__.update(kwds)
		self.dev="/dev/ttyUSB0"

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
		#26=0x1a,
		#6=0x06,
		#14=0x0e,
		#8=0x08,
		#12=0x0c,
		#10=0x0a

		self.commandItem = {
			'db_ChgSts':{'dataItem':0x00,'length':0x1e},
			'db_BatParam':{'dataItem':0x01,'length':0x14},
			'db_Log':{'dataItem':0x02,'length':0x1e},
			'db_parameters':{'dataItem':0x03,'length':0x1a},
			'db_LoadParam':{'dataItem':0x04,'length':0x1a},
			'db_ChgDebug':{'dataItem':0x05,'length':0x1e},
			'db_remoteControl':{'dataItem':0x06,'length':0x06},
			'db_ProParam':{'dataItem':0x07,'length':0x0e},
			'db_Information':{'dataItem':0x08,'length':0x08},
			'db_TempParam':{'dataItem':0x09,'length':0x0c},
			'db_EngSave':{'dataItem':0x10,'length':0x0a},

		}

		self.ChgSts=[
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

		self.BatParam=[
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
