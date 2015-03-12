#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import time

import KbHit
import const

class TestReseau:
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
	
	def __del__(self):
		KbHit.set_normal_term()

	def run(self, mode=const.MODE_MANU):
		"""
		Teste ping
		"""
		vResultat = False
		
		if (mode == const.MODE_MANU):
			msg = "Mode Manuel"
			vResultat = True # non testé pour un test manuel
			while 1:    
				response=os.system("ping -c 1 " + const.ADR_IP)
				if response == 0:
					print "\033[0;37;42m Test Reseau OK \033[0m"
				else:
					print "\033[0;37;41m Test Reseau NOK \033[0m"

				#Arret du programme par saisie clavier
				if KbHit.kbhit():
					self.kbhit = KbHit.getch()
					#print 'Arret programme demande '
					break

				time.sleep(1)
		
		elif (mode == const.MODE_AUTO):
			cptOK = 0
			for i in range(10):
				response=os.system("ping -c 1 " + const.ADR_IP)
				if response == 0:
					cptOK = cptOK + 1
			
			if (cptOK > 8):
				vResultat = True
				msg = "\033[0;37;42m Test Reseau OK \033[0m"
			else:
				msg = "\033[0;37;41m Test Reseau NOK \033[0m"
		
		else:
			msg = "run : mode inconnu !"
			pass
		
				
		return vResultat, msg
	
	
	############################################################################
if __name__ == "__main__":

	reseau = TestReseau()
	reseau.run()

