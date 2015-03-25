#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from datetime import date
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, \
    QTableWidgetItem, QLabel, QLineEdit, QAbstractItemView, QDateEdit, QComboBox
from PyQt5.QtGui import QTextDocument
from PyQt5.Qt import QTableWidget
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
import string
from random import sample
import random
from _datetime import datetime
from _ast import Delete

from clientPyQt import constantes
import logging
from clientPyQt import log
from clientPyQt.proxy import ProxyXMLRPC, ProxyREST, ProxyWeb

"""
    Ce module est le point d'entrée du programme
"""

log.configure()
logger = logging.getLogger(__name__)

class FormArticle(QWidget):
    """
        fenêtre d'édition d'un article
        utilisé pour ajouter/modifier un article
    """
    
    _signal_closed = pyqtSignal()

    def __init__(self, parent=None, aSignal = None, aLibelle = '', aPrix = 0, aDate = date.today):
        super(FormArticle, self).__init__(parent)
        
        try:
            self._libelle = aLibelle
            self._prix = aPrix
            self._date = aDate
            
            self.lblLib = QLabel('libellé')
            self.lblpri = QLabel('prix')
            self.lbldat = QLabel('date')
            self.edtLib = QLineEdit()
            self.edtPri = QLineEdit()
            self.edtDat = QDateEdit()
            self.edtDat.setDisplayFormat('yyyy-MM-dd')
            self.edtLib.setText(aLibelle)
            self.edtPri.setText(str(aPrix))
            self.edtDat.setDate(aDate)
            
            self.btnOk = QPushButton('OK')
            self.btnCancel = QPushButton('Annuler')  
            self.btnOk.setMaximumSize(100, 30)  
            self.btnCancel.setMaximumSize(100, 30)

            self._signal_closed = aSignal
            self.btnOk.clicked.connect(self.AjouterArticle)  
            self.btnCancel.clicked.connect(self.Annuler)  
            
            self.mainLayout = QGridLayout()
            self.mainLayout.addWidget(self.lblLib, 0, 0)
            self.mainLayout.addWidget(self.edtLib, 0, 1)
            self.mainLayout.addWidget(self.lblpri, 1, 0)
            self.mainLayout.addWidget(self.edtPri, 1, 1)
            self.mainLayout.addWidget(self.lbldat, 2, 0)
            self.mainLayout.addWidget(self.edtDat, 2, 1)
            self.mainLayout.addWidget(self.btnOk, 3, 0)
            self.mainLayout.addWidget(self.btnCancel, 3, 1)
                        
            self.setLayout(self.mainLayout)
            self.setWindowTitle('Article')

        except Exception as e:
            logger.exception(e)

    #############################################################################
    # Envoi un signal "Ajouter Un article" à MainWindow
    #############################################################################
    def AjouterArticle(self):
        try:
            self._signal_closed.emit(self.edtLib.text(), self.edtPri.text(), self.edtDat.text())
            self.close()

        except Exception as e:
            logger.exception(e)
        
    #############################################################################
    # Fermeture ArtForm sans envoi de signal
    #############################################################################
    def Annuler(self):
            self.close()

        
#################################################################################
#Description:
#   Fenetre principale liste des articles
#
#Entree:
#
#Sortie:
#
#Date:
#   05/12/2014
#
#Appels:
#
#
#Modifications:
#
#################################################################################
class MainWindow(QWidget):
    """
        fenêtre principale
        permet de lister les articles
        CRUD Articles
    """
    
    _mode = ''

    _ArtForm_closed = pyqtSignal(['QString', 'QString', 'QString'], name = "ArtFormFermeture")
    
    def __init__(self, parent=None, aConnection=None):
        super(MainWindow, self).__init__(parent)
        
        try:
            self.__adr_serveur = aConnection

            #connection serveur d'application
            self.__proxy = ProxyWeb(self.__adr_serveur)
            if not self.__proxy.connecter(constantes.PROXY_USER, constantes.PROXY_PWD):
                raise Exception("Erreur connection proxy")
                        
            #demande la conf d'affichage
            if self.__proxy.afficherMainWindow():
                
                self.tableWidget   = QTableWidget()
                self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection) 
                self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
                self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

                #alimentation de QTableView
                self.afficherArticles()
                    
                btnAdd = QPushButton('Ajouter')
                btnMod = QPushButton('Modifier')
                btnSup = QPushButton('Supprimer')
                btnRef = QPushButton('Raffraichir')
                btnGen = QPushButton('Generate')
                btnCom = QPushButton('Commit')
                btnRol = QPushButton('RollBack')
                btnQui = QPushButton('Quitter')
                btnImp = QPushButton('Imprimer')
                
                btnAdd.setMaximumSize(100, 30)
                btnMod.setMaximumSize(100, 30)
                btnSup.setMaximumSize(100, 30)
                btnRef.setMaximumSize(100, 30)
                btnGen.setMaximumSize(100, 30)
                btnCom.setMaximumSize(100, 30)
                btnRol.setMaximumSize(100, 30)
                btnQui.setMaximumSize(100, 30)
                btnImp.setMaximumSize(100, 30)

                self.cmbProxy = QComboBox()
                self.cmbProxy.setMaximumSize(200, 30)
                self.cmbProxy.addItem(constantes.PROXY_XMLRPC)
                self.cmbProxy.addItem(constantes.PROXY_REST)
                self.cmbProxy.addItem(constantes.PROXY_WEB)
                self.cmbProxy.setCurrentText(constantes.PROXY_WEB)

                mainLayout = QGridLayout()
                mainLayout.addWidget(self.cmbProxy, 0, 1)
                
                mainLayout.addWidget(self.tableWidget, 1, 1, 1, 4)
                mainLayout.addWidget(btnAdd, 2, 1)
                mainLayout.addWidget(btnMod, 2, 2)
                mainLayout.addWidget(btnSup, 2, 3)
                mainLayout.addWidget(btnCom, 3, 1)
                mainLayout.addWidget(btnGen, 3, 2)
                mainLayout.addWidget(btnRef, 3, 3)
                mainLayout.addWidget(btnRol, 4, 1)
                mainLayout.addWidget(btnImp, 4, 2)
                mainLayout.addWidget(btnQui, 4, 3)
                    
                self.setLayout(mainLayout)
                self.setWindowTitle('Articles - ' + aConnection)
                self.resize(500, 500)
                btnAdd.clicked.connect(self.AjouterArticle)
                btnMod.clicked.connect(self.ModifierArticle)
                btnSup.clicked.connect(self.SupprimerArticle)
                btnRef.clicked.connect(self.afficherArticles)
                btnGen.clicked.connect(self.RemplirArticles)
                btnCom.clicked.connect(self.CommitSession)
                btnRol.clicked.connect(self.RollbackSession)
                btnQui.clicked.connect(self.fermerAppli)
                btnImp.clicked.connect(self.imprimer)
                self.cmbProxy.currentIndexChanged.connect(self.changerProxy)
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
            self._ArtForm = FormArticle(None, self._ArtForm_closed, aLibelle, aPrix, aDate)
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
            
    #############################################################################
    # Slot fermeture FormArticle
    #############################################################################
    def slot_FormArticle_closed(self, alibelle, aprix, adate):
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

    #############################################################################
    # remplit table article
    #############################################################################
    def RemplirArticles(self):
        try:
            pop = string.ascii_letters
            i = 1
            while i < 1000:
                i = i + 1
                libelle = ''.join(sample(pop, 12))
                prix = random.uniform(1, 100)
                self.__proxy.ajouterArticle(libelle, prix)
                if i%500 == 0:
                    logger.debug('RemplirArticles')

        except Exception as e:
            logger.exception(e)
            
    #############################################################################
    # COMMIT
    #############################################################################
    def CommitSession(self):
        try:
            self.__proxy.commitSession()

        except Exception as e:
            logger.exception(e)
            
    #############################################################################
    # ROLLBACK
    #############################################################################
    def RollbackSession(self):
        try:
            self.__proxy.rollbackSession()

        except Exception as e:
            logger.exception(e)

    #############################################################################
    # Ferme fenêtre principale
    #############################################################################
    def fermerAppli(self):
        try:
            if type(self.__proxy) == ProxyWeb:
                self.__proxy.deconnecter()
            self.close()
        except Exception as e:
            logger.exception(e)

    #############################################################################
    # Imprimer
    #############################################################################
    def imprimer(self):
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
            
    
    ###########################################################################
    # slot combo Proxy modifié
    #############################################################################
    def changerProxy(self):
        
        try:
            if self.__proxy:
                if type(self.__proxy) == ProxyWeb:
                    self.__proxy.deconnecter()
                Delete(self.__proxy)
            
            if self.cmbProxy.currentText() == constantes.PROXY_XMLRPC:
                self.__proxy = ProxyXMLRPC(self.__adr_serveur)
            elif self.cmbProxy.currentText() == constantes.PROXY_REST:
                self.__proxy = ProxyREST(self.__adr_serveur)
            elif self.cmbProxy.currentText() == constantes.PROXY_WEB:
                self.__proxy = ProxyWeb(self.__adr_serveur)
                if not self.__proxy.connecter(constantes.PROXY_USER, constantes.PROXY_PWD):
                    raise Exception("Erreur connection proxy")
            else:
                self.cmbProxy.currentIndexChanged.disconnect()
                self.cmbProxy.setCurrentText(constantes.PROXY_XMLRPC)
                self.__proxy = ProxyXMLRPC(self.__adr_serveur)
                self.cmbProxy.currentIndexChanged.connect(self.changerProxy)

                raise Exception("Le proxy n'est pas défini")
            
            self.afficherArticles()

        except Exception as e:
            logger.exception(e)
            
                    
#################################################################################
# programme principal
#################################################################################
if __name__ == "__main__":
    
    logger.debug('clientPyQt Main')

    vConnection = sys.argv[1]

    app = QApplication(sys.argv)
    
    vMainWindow = MainWindow(None, vConnection)
    vMainWindow.show()
    
    sys.exit(app.exec_())
#################################################################################
