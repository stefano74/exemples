#!/usr/bin/python
# -*- coding: utf-8 -*-

from test_video import TestVideo
from test_reseau import TestReseau

import const

class MenuTest:
	"""
	classe Affichage
	"""
	def __init__(self):
		"""
		Constructeur
		"""
		self.choix = ""
	
	def afficher(self):
		"""
		Affiche le menu des tests montage
		"""
		print "############################################"
		print "TESTS MONTAGE"
		print "############################################"

		print '0 : AUTO'
		print '1 : Video'
		print '2 : Reseau'

		self.choix = input("choix = ")
		
	def run(self):
		"""
		lance le test en fonction de choix
		"""

		if (self.choix == 0):
			video = TestVideo()
			reseau = TestReseau()
			print "run auto"

			vResultat, msg1 = video.run()
			vResultat, msg2 = reseau.run(const.MODE_AUTO)

			print msg1
			print msg2
			
		elif (self.choix == 1):
			print "run video"
			video = TestVideo()
			video.run()
			#del video # le destructeur est appele automatiquement a la sortie de la methode
		elif (self.choix == 2):
			print "run reseau"
			reseau = TestReseau()
			reseau.run(const.MODE_MANU)
			#del reseau # le destructeur est appele automatiquement a la sortie de la methode
		else:
			print "Choix inconnu !"
	
##############################################################################
if __name__ == "__main__":

	menu = MenuTest()
	while 1:
		menu.afficher()
		menu.run()

