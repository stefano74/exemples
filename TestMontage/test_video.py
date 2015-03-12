#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import time

import KbHit

class TestVideo:
	"""
	classe de Test Video 
	"""
	def __init__(self):
		"""
		Constructeur
		"""
		#Saisie au vol de caractere
		KbHit.initkb()
		self.kbhit=None
	
	def __del__(self):
		print "destructeur TestVideo"
		KbHit.set_normal_term()
		
	def testRouge(self):
		"""
		Remplit l'écran en rouge
		"""	
		while 1:
 			sys.stdout.write("\033[0;31;41m 0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB \033[0m")
#			os.system(echo -e '\033[0;31;41m 0xDBOxDBOxDBOxDBOxDBOxDBOxDBOxDBOxDBOxDB \033[0m')
	
			#Arret du programme par saisie clavier
			if KbHit.kbhit():
				self.kbhit = KbHit.getch()
	      	#print 'Arret programme demande '
				break
			
#			time.sleep(1)

	def testVert(self):
		"""
		Remplit l'écran en vert
		"""	
		while 1:
			sys.stdout.write("\033[0;32;42m 0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB \033[0m")
			#Arret du programme par saisie clavier
			if KbHit.kbhit():
				self.kbhit = KbHit.getch()
	      	#print 'Arret programme demande '
				break
			
#			time.sleep(1)

	def testBleu(self):
		"""
		Remplit l'écran en rouge
		"""	
		while 1:
			sys.stdout.write("\033[0;34;44m 0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB \033[0m")

			#Arret du programme par saisie clavier
			if KbHit.kbhit():
				self.kbhit = KbHit.getch()
	      	#print 'Arret programme demande '
				break
			
#			time.sleep(1)

	def run(self):
		"""
		Teste les 3 couleurs
		"""
		self.testRouge()
		self.testVert()
		self.testBleu()
	
	############################################################################
if __name__ == "__main__":

	video = TestVideo()
	video.run()

