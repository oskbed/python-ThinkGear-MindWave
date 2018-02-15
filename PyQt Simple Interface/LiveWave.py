import time
import serial
import io
import os
import sys
from threading import Thread
from serial import SerialException

#This is Mind Wave Parser library for Windows. For managing live parsing I used threading module.
#It will be changed in newer version.
#Version 0.2

# Bytes codes

SYNC = b'\xaa'
EXCODE = b'\x55'
POOR_SIGNAL = b'\x02'
ATTENTION = b'\x04'
MEDITATION = b'\x05'
RAW_VALUE = b'\x80'

class LiveWave:
	""" Live Data Parser for Mind Wave Mobile """
	def __init__(self, port = None, baudRate=57600, byteSize = serial.EIGHTBITS, parity = serial.PARITY_NONE, stopBits = serial.STOPBITS_ONE , timeout=10):
		self.meditation = 0
		self.attention = 0
		self.rawValue = 0
		self.rawBuffer = []
		self.poor_signal = 0
		self.state = 0 # 0 - Instance Created / Device not Connected || 1 - Device Connected ||
		self.sendingData = False

		if port == None:
			platform = sys.platform
			if platform == "win32":
				port = "COM4"


		### Serial ##
		self.__serialPort = port
		self.__serialBaudRate = baudRate
		self.__serialByteSize = byteSize
		self.__serialParity = parity
		self.__serialStopBits = stopBits
		self.__serialTimeOut = timeout


		#Thread#
		self.__parserThread = None
		self.__threadRun = False
		self.__ser = None
		try:
			self.connect()
		except Exception as e:
			print (e)

	def connect(self):
		if self.__ser == None:
			try:
				self.__ser = serial.Serial(
					self.__serialPort, self.__serialBaudRate, self.__serialByteSize,
					self.__serialParity, self.__serialStopBits, self.__serialTimeOut)
			except serial.SerialException as e:
				print (e)
				return
		else:
			print ("MindWave already connected!")

		self.__ser.flushInput()
		if self.__ser.isOpen:
			print ("Successfully connected!")
		self.state = 1
	def __del__(self):
		self.__ser.__del__()
	def showstate(self):
		if self.state == 0:
			print ("Device not connected.")
		if self.state == 1:
			print ("Device is connected.")
		if self.sendingData:
			print ("Parser is running and sending data!")
	def start(self):
		if self.__ser.isOpen():
			try:
				self.__parserThread = Thread(target=self.parser, args=())
				self.__threadRun = True
				self.__parserThread.start()
			except Exception as e:
				print ("Error! ", e)
		else:
			 self.__ser.open()
			 self.start()
	def stop(self):
		if self.__threadRun == True:
			self.__threadRun = False
			self.__parserThread.join()
			self.__ser.close()
	def parser(self):
		self.sendingData = True
		while self.__threadRun:
			byte1 = self.__ser.read(1)
			byte2 = self.__ser.read(1)
			while (byte1 != (b'\xaa') or byte2 != (b'\xaa')) and self.__threadRun:
				byte1 = byte2
				byte2 = self.__ser.read(1)
			else:
				if self.__threadRun == False:
					break

				payload = []
				checksum = 0
				packet_length = self.__ser.read(1)
				payloadLength = (packet_length[0])
				for i in range(payloadLength):
					packet_code = self.__ser.read(1)
					tempPacket = packet_code[0]
					payload.append(packet_code)
					checksum += tempPacket
				checksum = ~checksum & 0xff #Checksum calculator
				check = self.__ser.read(1)
				if checksum == check[0]:
					i = 0
					while i < payloadLength:
						packet = payload[i]
						if packet == (b'\x80'): # raw value
							i += 1
							i += 1
							val0 = payload[i]
							i += 1
							val1 = payload[i]
							self.rawValue = val0[0] * 256 + val1[0]
							if self.rawValue > 32768:
								self.rawValue = self.rawValue - 65536
								self.rawBuffer.append(self.rawValue)
							else:
								self.rawBuffer.append(self.rawValue)
							#print ("Signal :", self.rawValue)
						elif packet == bytes(b'\x02'): # Poor signal
							i += 1
							a = payload[i]
							self.poor_signal = a[0]
						elif packet == (b'\x04'): # Attention (eSense)
							i += 1
							a = payload[i]
							if a[0]>0:
								self.attention = a[0]
						elif packet == (b'\x05'): # Meditation (eSense)
							i += 1
							a = payload[i]
							if a[0]>0:
								self.meditation = a[0]
						#Rest of the code packets are WIP#
						else:
							pass
						i += 1
