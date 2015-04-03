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

    _ArtForm_closed = pyqtSignal(['PyQt_PyObject'], name = "ArtFormFermeture")
    
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

            self.cmboListModels = QComboBox()
            
            btnAdd.setMaximumSize(100, 30)
            btnMod.setMaximumSize(100, 30)
            btnSup.setMaximumSize(100, 30)
            btnRef.setMaximumSize(100, 30)
            btnGen.setMaximumSize(100, 30)
            btnImp.setMaximumSize(100, 30)

            mainLayout = QGridLayout()
            mainLayout.addWidget(self.cmboListModels, 0, 1, 1, 4)
            mainLayout.addWidget(self.tableWidget, 1, 1, 1, 4)
            mainLayout.addWidget(btnAdd, 2, 1)
            mainLayout.addWidget(btnMod, 2, 2)
            mainLayout.addWidget(btnSup, 2, 3)
            mainLayout.addWidget(btnGen, 3, 1)
            mainLayout.addWidget(btnImp, 3, 2)
            mainLayout.addWidget(btnRef, 3, 3)
                
            self.setLayout(mainLayout)
#             self.resize(500, 500)
            btnAdd.clicked.connect(self.AjouterModel)
            btnMod.clicked.connect(self.ModifierModel)
            btnSup.clicked.connect(self.SupprimerArticle)
            btnRef.clicked.connect(self.afficherModel)
            btnGen.clicked.connect(self.generer)
            btnImp.clicked.connect(self.imprimer)
            self._ArtForm_closed.connect(self.slot_FormArticle_closed)
            
            self.__listModels = self.__proxy.listerModels()
            self.initCmboListModels()
            self.afficherModel()

        except Exception as e:
            logger.exception(e)
            
    #############################################################################
    # Affiche tous les articles dans QTableWidget
    #############################################################################
    def afficherModel(self):
        try:
            i = 0
            self.__lstModel = self.__proxy.listerModel(self.cmboListModels.currentText())
            self.tableWidget.clear()
                
            self.tableWidget.setRowCount(len(self.__lstModel))
            header = list(self.__lstModel[0]['fields'].keys())
            self.tableWidget.setColumnCount(len(header)) 
            self.tableWidget.setHorizontalHeaderLabels(header)
                                        
            for model in self.__lstModel:
                for col in range(len(header)):
                    self.tableWidget.setItem(i, col, QTableWidgetItem(str(model['fields'][header[col]])))
                i = i + 1
        
        except Exception as e:
            logger.exception(e)
            
    #############################################################################
    # Afficher FormArticle
    #############################################################################
    def AfficherFormulaire(self, adictModel = None):
        try:
            self._ArtForm = DetailWindow(None, self._ArtForm_closed, adictModel)
            self._ArtForm.setWindowModality(QtCore.Qt.ApplicationModal)
            self._ArtForm.show()
            
        except Exception as e:
            logger.exception(e)


    #############################################################################
    # Ajouter un article
    #############################################################################
    def AjouterModel(self):
        try:
            self._mode = constantes.MODE_ADD
            
            #création d'un dico par défaut vide
            dictDefault = {}
            dictDefault['fields'] = self.__lstModel[0]['fields']
            
            for k in dictDefault['fields'].keys():
                dictDefault['fields'][k] = ""
            
            print ("dictdefault = ", dictDefault)
            self.AfficherFormulaire(dictDefault)

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
    def ModifierModel(self):
        try:
            self._mode = constantes.MODE_MOD
            if self.tableWidget.selectedItems():
                self.AfficherFormulaire(self.__lstModel[self.tableWidget.currentRow()])                

        except Exception as e:
            logger.exception(e)
            
    def slot_FormArticle_closed(self, adictModel):
        """
            SLOT Fermeture fenetre DetailWindow
            :param alibelle: libelle de l'objet
            :param aprix: prix de l'objet
            :param adate: date de l'objet
        """
        try:
            if self._mode == constantes.MODE_ADD:
                self.__proxy.ajouterModel(self.cmboListModels.currentText(), adictModel)
            elif self._mode == constantes.MODE_MOD:
                self.__proxy.modifierModel(self.cmboListModels.currentText(), adictModel)
            else:
                logger.error("Mode inconnu")
 
            self.afficherModel()
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

    def listerModels(self):
        try:
            return self.__proxy.listerModels()
        except Exception as e:
            logger.exception(e)
            
        
    def initCmboListModels(self):
        """
        initialise la combobox avec la liste des models
        """
        try:
            for model in self.__listModels:
                self.cmboListModels.addItem(model['fields']['name'])
            self.cmboListModels.setCurrentIndex(0)

        except Exception as e:
            logger.exception(e)

        