#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 19 mars 2015

@author: stefano
'''

from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, \
    QTableWidgetItem, QLineEdit, QAbstractItemView, QComboBox
from PyQt5.QtGui import QTextDocument
from PyQt5.Qt import QTableWidget
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog

import string
from random import sample
import random
from _datetime import datetime, date
from _ast import Delete

from clientPyQt import constantes
from clientPyQt.detailwindow import DetailWindow
import logging

logger = logging.getLogger(__name__)

class ListWindow(QWidget):
    
    _mode = ''

    _ArtForm_closed = pyqtSignal(['QString', 'QString', 'QString'], name = "ArtFormFermeture")
    
    def __init__(self, parent=None, aproxy=None):
        super(ListWindow, self).__init__(parent)
        
        try:
            self.__proxy = aproxy

            
            self.tableWidget   = QTableWidget()
            self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection) 
            self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.tableWidget.setMinimumHeight(10)

            btnAdd = QPushButton('Ajouter')
            btnMod = QPushButton('Modifier')
            btnSup = QPushButton('Supprimer')
            btnRef = QPushButton('Raffraichir')
            btnGen = QPushButton('Generate')
            btnImp = QPushButton('Imprimer')
            
            btnAdd.setMaximumSize(100, 30)
            btnMod.setMaximumSize(100, 30)
            btnSup.setMaximumSize(100, 30)
            btnRef.setMaximumSize(100, 30)
            btnGen.setMaximumSize(100, 30)
            btnImp.setMaximumSize(100, 30)

            mainLayout = QGridLayout()
            mainLayout.addWidget(self.tableWidget, 1, 1, 1, 4)
            mainLayout.addWidget(btnAdd, 2, 1)
            mainLayout.addWidget(btnMod, 2, 2)
            mainLayout.addWidget(btnSup, 2, 3)
            mainLayout.addWidget(btnGen, 3, 1)
            mainLayout.addWidget(btnImp, 3, 2)
            mainLayout.addWidget(btnRef, 3, 3)
                
            self.setLayout(mainLayout)
#             self.resize(500, 500)
            btnAdd.clicked.connect(self.AjouterArticle)
            btnMod.clicked.connect(self.ModifierArticle)
            btnSup.clicked.connect(self.SupprimerArticle)
            btnRef.clicked.connect(self.afficherArticles)
            btnGen.clicked.connect(self.generer)
            btnImp.clicked.connect(self.imprimer)
            self._ArtForm_closed.connect(self.slot_FormArticle_closed)

        except Exception as e:
            logger.exception(e)
            
    #############################################################################
    # Affiche tous les articles dans QTableWidget
    #############################################################################
    def afficherArticles(self):
        try:
            i = 0
            lstArt = self.__proxy.listerArticles()
            self.tableWidget.clear()
                
            self.tableWidget.setRowCount(len(lstArt))
            self.tableWidget.setColumnCount(4)
            self.tableWidget.setHorizontalHeaderLabels(('Id;Libellé;Prix;Date').split(';'))

                                        
            for art in lstArt:
                self.tableWidget.setItem(i, 0, QTableWidgetItem(str(art[0])))
                self.tableWidget.setItem(i, 1, QTableWidgetItem(str(art[1])))
                self.tableWidget.setItem(i, 2, QTableWidgetItem(str(art[2])))
                self.tableWidget.setItem(i, 3, QTableWidgetItem(str(art[3])))
                i = i + 1
        
        except Exception as e:
            logger.exception(e)
            
    #############################################################################
    # Afficher FormArticle
    #############################################################################
    def AfficherFormulaire(self, aLibelle = '', aPrix = 0, aDate = date.today()):
        try:
            self._ArtForm = DetailWindow(None, self._ArtForm_closed, aLibelle, aPrix, aDate)
            self._ArtForm.setWindowModality(QtCore.Qt.ApplicationModal)
            self._ArtForm.show()
            
        except Exception as e:
            logger.exception(e)


    #############################################################################
    # Ajouter un article
    #############################################################################
    def AjouterArticle(self):
        try:
            self._mode = self.MODE_ADD
            self.AfficherFormulaire()

        except Exception as e:
            logger.exception(e)

    #############################################################################
    # Supprimer un article
    #############################################################################
    def SupprimerArticle(self):
        try:
            if self.tableWidget.selectedItems():
                self.__proxy.supprimerArticle(self.tableWidget.selectedItems()[0].text())
                self.afficherArticles()

        except Exception as e:
            logger.exception(e)
    
    #############################################################################
    # Modifier un article
    #############################################################################
    def ModifierArticle(self):
        try:
            self._mode = self.MODE_MOD
            if self.tableWidget.selectedItems():
                self.AfficherFormulaire(self.tableWidget.selectedItems()[1].text(), 
                                        float(self.tableWidget.selectedItems()[2].text()),
                                        datetime.strptime(self.tableWidget.selectedItems()[3].text(), '%Y-%M-%d').date())                

        except Exception as e:
            logger.exception(e)
            
    def slot_FormArticle_closed(self, alibelle, aprix, adate):
        """
            SLOT Fermeture fenetre DetailWindow
            :param alibelle: libelle de l'objet
            :param aprix: prix de l'objet
            :param adate: date de l'objet
        """
        try:
            if self._mode == self.MODE_ADD:
                self.__proxy.ajouterArticle(alibelle, aprix, adate)
            elif self._mode == self.MODE_MOD:
                self.__proxy.modifierArticle(int(self.tableWidget.selectedItems()[0].text()), alibelle, aprix, adate)
            else:
                logger.error("Mode inconnu")

            self.afficherArticles()
            self._mode = ''
            
        except Exception as e:
            logger.exception(e)

    def generer(self):
        """
            remplit la TableWidget de 1000 objets
        """
        try:
            pop = string.ascii_letters
            i = 1
            while i < 1000:
                i = i + 1
                libelle = ''.join(sample(pop, 12))
                prix = random.uniform(1, 100)
                self.__proxy.ajouterArticle(libelle, prix)
                if i%500 == 0:  # ???
                    logger.debug('generer')

        except Exception as e:
            logger.exception(e)
            
    def imprimer(self):
        """
            imprime un document de test
        """
        printer=QPrinter()
     
        doc=QTextDocument("Hello")
#         doc=QTextDocument()
#         doc.setHtml("<body> salut </body>")
        dialog = QPrintDialog(printer)
        dialog.setModal(True)
        dialog.setWindowTitle("Print Document" )
        # dialog.addEnabledOption(QAbstractPrintDialog.PrintSelection)
        if dialog.exec_() == True:
            doc.print(printer)
            