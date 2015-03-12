#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

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
		KbHit.set_normal_term()
		
	def testRouge(self):
		"""
		Remplit l'écran en rouge
		"""	
		vResultat = False
		while 1:
			sys.stdout.write("\033[0;31;41m 0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB \033[0m")
#			os.system(echo -e '\033[0;31;41m 0xDBOxDBOxDBOxDBOxDBOxDBOxDBOxDBOxDBOxDB \033[0m')
	
			#Arret du programme par saisie clavier
			if KbHit.kbhit():
				self.kbhit = KbHit.getch()
				if (self.kbhit == 'o') or (self.kbhit == 'O'):
					vResultat = True
				#print 'Arret programme demande '
				break
			
#			time.sleep(1)
		return vResultat

	def testVert(self):
		"""
		Remplit l'écran en vert
		"""
		vResultat = False	
		while 1:
			sys.stdout.write("\033[0;32;42m 0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB \033[0m")
			#Arret du programme par saisie clavier
			if KbHit.kbhit():
				self.kbhit = KbHit.getch()
				if (self.kbhit == 'o') or (self.kbhit == 'O'):
					vResultat = True
				#print 'Arret programme demande '
				break
			
#			time.sleep(1)
		return vResultat

	def testBleu(self):
		"""
		Remplit l'écran en rouge
		"""	
		vResultat = False	
		while 1:
			sys.stdout.write("\033[0;34;44m 0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB0xDB \033[0m")

			#Arret du programme par saisie clavier
			if KbHit.kbhit():
				self.kbhit = KbHit.getch()
				if (self.kbhit == 'o') or (self.kbhit == 'O'):
					vResultat = True
				#print 'Arret programme demande '
				break
			
#			time.sleep(1)
		return vResultat

	def run(self):
		"""
		Teste les 3 couleurs
		"""
		vResultat = self.testRouge() and \
					self.testVert() and \
					self.testBleu()
		
		if vResultat:
			msg = "\033[0;37;42m Test Video OK \033[0m"
		else:
			msg = "\033[0;37;41m Test Video NOK \033[0m"

		return vResultat, msg
	
	############################################################################
if __name__ == "__main__":

	video = TestVideo()
	video.run()

