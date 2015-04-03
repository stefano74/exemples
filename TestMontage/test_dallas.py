#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import time

import KbHit
import const
import serial

class TestDallas:
	"""
	classe de Test Reseau
	"""
	def __init__(self):
		"""
		Constructeur
		"""
		#Saisie au vol de caractere
		KbHit.initkb()
		self.kbhit=None
		
		self.__serial = serial.Serial() 
		self.__serial.baudrate = 9600
		self.__serial.port = 1
		self.__serial.timeout = 0
		
		print "SERIAL = ", self.__serial
	
	def __del__(self):
		KbHit.set_normal_term()
		
	def Crc8(self, data=''):
		"""
			calcule le CRC8
			:param data: données pour calculer le CRC8
			:return: crc
			:rtype: integer
		"""
		crc=0x00
		#Pour chaque caractère, calcul du crc8
		for Car in data:
			crc=const.TABLE_CRC8[crc^ord(Car)]
		#Retour Crc8
		return chr(crc)	
	
	def lireISD(self):
		"""
		lit le numéro ISD sur la carte DALLAS
		"""		
		PREFIXE_LECTURE_NUMERO=('L')
		COMMANDE_DONNEES_NULLES=chr(0x00)+chr(0x00)+chr(0x00)+chr(0x00)+chr(0x00)+chr(0x00)+chr(0x00)+chr(0x00)
		COMMANDE_LECTURE_NUMERO=PREFIXE_LECTURE_NUMERO+COMMANDE_DONNEES_NULLES+chr(0x25)
		
		try: 

			self.__serial.open()

		except Exception, e:
			print "error open serial port: " + str(e)
			exit()

		if self.__serial.isOpen():
			try:

				self.__serial.flushInput() #flush input buffer, discarding all its contents
				self.__serial.flushOutput()#flush output buffer, aborting current output 
				#and discard all that is in buffer

				#write data

				self.__serial.write(COMMANDE_LECTURE_NUMERO)
				print("write data: Lecture ISD")

				time.sleep(0.5)  #give the serial port sometime to receive the data

				numOfLines = 0

				while True:
					response = self.__serial.readline()
					print("read data: ", response)
					numOfLines = numOfLines + 1
					if (numOfLines >= 5):
# 					if not response or response[-1:] != '\n':
						break

				self.__serial.close()

			except Exception, e1:
				print "error communicating...: " + str(e1)

		else:
			print "cannot open serial port "


	def run(self, mode=const.MODE_MANU):
		"""
		Teste lecture / écriture ISD
		"""
		vResultat = False
		
		self.lireISD()
		
		if (mode == const.MODE_MANU):
			msg = "Mode Manuel"
			vResultat = True # non testé pour un test manuel
		
		elif (mode == const.MODE_AUTO):
			pass		
		else:
			msg = "run : mode inconnu !"
			pass
		
				
		return vResultat, msg
	
	
	############################################################################
if __name__ == "__main__":

	dallas = TestDallas()
	dallas.run()

