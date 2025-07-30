# -*- coding: utf-8; mode: python; indent-tabs-mode: t; tab-width:4 -*-

from __future__ import print_function
import time

def connect(route,**args):
	return TSL2591(route,**args)

class TSL2591: 
	TSL2591_GAIN = 0x00  # 0x00=1x , 0x10 = medium 25x, 0x20 428x , 0x30 Max 9876x
	TSL2591_TIMING = 0x00  # 0x00=100 mS , 0x05 = 600mS

	TSL2591_ADDRESS = 0x29

	TSL2591_COMMAND_BIT = 0xA0
	# Register (0x00)
	TSL2591_ENABLE_REGISTER = 0x00
	TSL2591_ENABLE_POWERON = 0x01
	TSL2591_ENABLE_POWEROFF = 0x00
	TSL2591_ENABLE_AEN = 0x02
	TSL2591_ENABLE_AIEN = 0x10
	TSL2591_ENABLE_SAI = 0x40
	TSL2591_ENABLE_NPIEN = 0x80

	TSL2591_CONTROL_REGISTER = 0x01
	TSL2591_SRESET = 0x80
	# AGAIN
	TSL2591_LOW_AGAIN = 0X00  # Low gain (1x)
	TSL2591_MEDIUM_AGAIN = 0X10  # Medium gain (25x)
	TSL2591_HIGH_AGAIN = 0X20  # High gain (428x)
	TSL2591_MAX_AGAIN = 0x30  # Max gain (9876x)
	# ATIME
	TSL2591_ATIME_100MS = 0x00  # 100 millis #MAX COUNT 36863
	TSL2591_ATIME_200MS = 0x01  # 200 millis #MAX COUNT 65535
	TSL2591_ATIME_300MS = 0x02  # 300 millis #MAX COUNT 65535
	TSL2591_ATIME_400MS = 0x03  # 400 millis #MAX COUNT 65535
	TSL2591_ATIME_500MS = 0x04  # 500 millis #MAX COUNT 65535
	TSL2591_ATIME_600MS = 0x05  # 600 millis #MAX COUNT 65535

	TSL2591_AILTL_REGISTER = 0x04
	TSL2591_AILTH_REGISTER = 0x05
	TSL2591_AIHTL_REGISTER = 0x06
	TSL2591_AIHTH_REGISTER = 0x07
	TSL2591_NPAILTL_REGISTER = 0x08
	TSL2591_NPAILTH_REGISTER = 0x09
	TSL2591_NPAIHTL_REGISTER = 0x0A
	TSL2591_NPAIHTH_REGISTER = 0x0B
	TSL2591_PERSIST_REGISTER = 0x0C

	TSL2591_ID_REGISTER = 0x12

	TSL2591_STATUS_REGISTER = 0x13

	TSL2591_CHAN0_LOW = 0x14
	TSL2591_CHAN0_HIGH = 0x15
	TSL2591_CHAN1_LOW = 0x16
	TSL2591_CHAN1_HIGH = 0x14

	# LUX_DF = GA * 53   GA is the Glass Attenuation factor
	TSL2591_LUX_DF = 408.0
	TSL2591_LUX_COEFB = 1.64
	TSL2591_LUX_COEFC = 0.59
	TSL2591_LUX_COEFD = 0.86

	# LUX_DF              = 408.0
	TSL2591_MAX_COUNT_100MS = (36863)  # 0x8FFF
	TSL2591_MAX_COUNT = (65535)  # 0xFFFF

	PLOTNAMES = ['Full','IR','Visible']
	def __init__(self, I2C,**kwargs):
		self.I2C = I2C  
		self.TSL2591_ADDRESS = kwargs.get('address', self.TSL2591_ADDRESS)

		b = self.I2C.readBulk(self.TSL2591_ADDRESS, self.TSL2591_COMMAND_BIT | self.TSL2591_ID_REGISTER, 1)
		if b is None: return None
		b = b[0]
		if b != 0x50:
			print('TSL. wrong ID:', b)

		self.I2C.writeBulk(self.TSL2591_ADDRESS, [self.TSL2591_COMMAND_BIT | self.TSL2591_ENABLE_REGISTER,
			                                     self.TSL2591_ENABLE_AIEN | self.TSL2591_ENABLE_POWERON | self.TSL2591_ENABLE_AEN | self.TSL2591_ENABLE_NPIEN])
		self.I2C.writeBulk(self.TSL2591_ADDRESS, [self.TSL2591_COMMAND_BIT | self.TSL2591_PERSIST_REGISTER, 0x01])
		self.TSL2591_config(self.TSL2591_GAIN, self.TSL2591_TIMING)
		self.TSL2591_all()



	def initialize(self,v):
		pass
		
	def TSL2591_gain(self, gain):
		self.TSL2591_GAIN = gain << 4  # 0x00=1x , 0x10 = medium 25x, 0x20 428x , 0x30 Max 9876x
		self.TSL2591_config(self.TSL2591_GAIN, self.TSL2591_TIMING)

	def TSL2591_timing(self, timing):
		self.TSL2591_TIMING = timing
		self.TSL2591_config(self.TSL2591_GAIN, self.TSL2591_TIMING)

	def TSL2591_config(self, gain, timing):
		self.I2C.writeBulk(self.TSL2591_ADDRESS,
			              [self.TSL2591_COMMAND_BIT | self.TSL2591_CONTROL_REGISTER, gain | timing])

	def TSL2591_Read_CHAN0(self):
		b = self.I2C.readBulk(self.TSL2591_ADDRESS, self.TSL2591_COMMAND_BIT | self.TSL2591_CHAN0_LOW, 2)
		if b is None: return None
		if None not in b:
			return (b[1] << 8) | b[0]

	def TSL2591_Read_CHAN1(self):
		b = self.I2C.readBulk(self.TSL2591_ADDRESS, self.TSL2591_COMMAND_BIT | self.TSL2591_CHAN1_LOW, 2)
		if b is None: return None
		if None not in b:
			return (b[1] << 8) | b[0]

	def TSL2591_Read_FullSpectrum(self):
		"""Read the full spectrum (IR + visible) light and return its value"""
		data = (self.TSL2591_Read_CHAN1() << 16) | self.TSL2591_Read_CHAN0()
		return data

	def TSL2591_Read_Infrared(self):
		'''Read the infrared light and return its value as a 16-bit unsigned number'''
		data = self.TSL2591_Read_CHAN0()
		return data

	def TSL2591_all(self):
		b = self.I2C.readBulk(self.TSL2591_ADDRESS, self.TSL2591_COMMAND_BIT | self.TSL2591_CHAN0_LOW, 4)
		if b is None: return None
		if None not in b:
			channel_0 = (b[1] << 8) | b[0]
			channel_1 = (b[3] << 8) | b[2]

		# channel_0 = self.TSL2591_Read_CHAN0()
		# channel_1 = self.TSL2591_Read_CHAN1()
		# for i in range(0, self.TSL2591_TIMING+2):
		#	time.sleep(0.1)

		atime = 100.0 * self.TSL2591_TIMING + 100.0

		# Set the maximum sensor counts based on the integration time (atime) setting
		if self.TSL2591_TIMING == 0:
			max_counts = self.TSL2591_MAX_COUNT_100MS
		else:
			max_counts = self.TSL2591_MAX_COUNT

		'''
		if channel_0 >= max_counts or channel_1 >= max_counts:
			if(self.TSL2591_GAIN != self.TSL2591_LOW_AGAIN):
				self.TSL2591_GAIN = ((self.TSL2591_GAIN>>4)-1)<<4
				self.TSL2591_config(self.self.TSL2591_GAIN,self.TSL2591_TIMING)
				channel_0 = 0
				channel_1 = 0
				while(channel_0 <= 0 and channel_1 <=0):
					channel_0 = self.TSL2591_Read_CHAN0()
					channel_1 = self.TSL2591_Read_CHAN1()
					time.sleep(0.1)
			else :
				return 0
		'''

		if channel_0 >= max_counts or channel_1 >= max_counts:
			return [(channel_1 & 0xFFFFFFFF << 16) | channel_0, 0, 0]

		again = 1.0
		if self.TSL2591_GAIN == self.TSL2591_MEDIUM_AGAIN:
			again = 25.0
		elif self.TSL2591_GAIN == self.TSL2591_HIGH_AGAIN:
			again = 428.0
		elif self.TSL2591_GAIN == self.TSL2591_MAX_AGAIN:
			again = 9876.0

		cpl = (atime * again) / self.TSL2591_LUX_DF

		lux1 = (channel_0 - (self.TSL2591_LUX_COEFB * channel_1)) / cpl

		lux2 = ((self.TSL2591_LUX_COEFC * channel_0) - (self.TSL2591_LUX_COEFD * channel_1)) / cpl

		return [(channel_1 & 0xFFFFFFFF << 16) | channel_0, lux1, lux2]

