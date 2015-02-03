#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import xmlrpc.client
from datetime import date
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QTableView, \
    QHeaderView, QTableWidgetItem, QLabel, QLineEdit, QAbstractItemView, QDateEdit
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.Qt import QTableWidget
from PyQt5.QtCore import pyqtSignal
from _random import Random
import string
from random import sample
import random
from xmlrpc.client import ProtocolError
import http
from _datetime import datetime


#################################################################################
#Description:
#   Formulaire d un article
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
class FormArticle(QWidget):
    
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

        except:
            print ('FormArticle.__init__ Erreur! : ', sys.exc_info()[0], sys.exc_info()[1])

    #############################################################################
    # Envoi un signal "Ajouter Un article" à MainWindow
    #############################################################################
    def AjouterArticle(self):
        try:
            self._signal_closed.emit(self.edtLib.text(), self.edtPri.text(), self.edtDat.text())
            self.close()

        except:
            print ('FormArticle.AjouterArticle Erreur! : ', sys.exc_info()[0], sys.exc_info()[1])
        
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
    
    MODE_ADD = 'add'
    MODE_MOD = 'mod'
    
    _mode = ''

    _ArtForm_closed = pyqtSignal(['QString', 'QString', 'QString'], name = "ArtFormFermeture")
    
    def __init__(self, parent=None, aConnection=None):
        super(MainWindow, self).__init__(parent)
        
        try:
            #connection serveur d'application
#            self._proxy = xmlrpc.client.ServerProxy('http://localhost:8888')
            self._proxy = xmlrpc.client.ServerProxy(aConnection, verbose=True)
            
            #demande la conf d'affichage
            if self._proxy.afficherMainWindow():
                
                self._tableWidget   = QTableWidget()
                self._tableWidget.setSelectionMode(QAbstractItemView.SingleSelection) 
                self._tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
                self._tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

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
                
                btnAdd.setMaximumSize(100, 30)
                btnMod.setMaximumSize(100, 30)
                btnSup.setMaximumSize(100, 30)
                btnRef.setMaximumSize(100, 30)
                btnGen.setMaximumSize(100, 30)
                btnCom.setMaximumSize(100, 30)
                btnRol.setMaximumSize(100, 30)
                btnQui.setMaximumSize(100, 30)

                mainLayout = QGridLayout()
                mainLayout.addWidget(self._tableWidget, 0, 0, 1, 4)
                mainLayout.addWidget(btnAdd, 1, 1)
                mainLayout.addWidget(btnMod, 1, 2)
                mainLayout.addWidget(btnSup, 1, 3)
                mainLayout.addWidget(btnCom, 2, 1)
                mainLayout.addWidget(btnGen, 2, 2)
                mainLayout.addWidget(btnRef, 2, 3)
                mainLayout.addWidget(btnRol, 3, 1)
                mainLayout.addWidget(btnQui, 3, 3)
                    
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
                self._ArtForm_closed.connect(self.slot_FormArticle_closed)

    
        except ProtocolError as err:
            print ('MainWindow.__init__ Erreur! : ', sys.exc_info()[0], sys.exc_info()[1])
            print ("A protocol error occurred")
            print ("URL: %s" % err.url)
            print ("HTTP/HTTPS headers: %s" % err.headers)
            print ("Error code: %d" % err.errcode)
            print ("Error message: %s" % err.errmsg)
    #############################################################################
    # Affiche tous les articles dans QTableWidget
    #############################################################################
    def afficherArticles(self):
        try:
            i = 0
            lstArt = self._proxy.listerArticles()
            self._tableWidget.clear()
                
            self._tableWidget.setRowCount(len(lstArt))
            self._tableWidget.setColumnCount(4)
            self._tableWidget.setHorizontalHeaderLabels(('Id;Libellé;Prix;Date').split(';'))

                                        
            for art in lstArt:
                self._tableWidget.setItem(i, 0, QTableWidgetItem(str(art[0])))
                self._tableWidget.setItem(i, 1, QTableWidgetItem(str(art[1])))
                self._tableWidget.setItem(i, 2, QTableWidgetItem(str(art[2])))
                self._tableWidget.setItem(i, 3, QTableWidgetItem(str(art[3])))
                i = i + 1
        
        except:
            print ('MainWindow.afficherArticles Erreur! : ', sys.exc_info()[0], sys.exc_info()[1])
            
    #############################################################################
    # Afficher FormArticle
    #############################################################################
    def AfficherFormulaire(self, aLibelle = '', aPrix = 0, aDate = date.today()):
        try:
            self._ArtForm = FormArticle(None, self._ArtForm_closed, aLibelle, aPrix, aDate)
            self._ArtForm.setWindowModality(QtCore.Qt.ApplicationModal)
            self._ArtForm.show()
            
        except:
            print ('MainWindow.AfficherUnArticle Erreur! : ', sys.exc_info()[0], sys.exc_info()[1])


    #############################################################################
    # Ajouter un article
    #############################################################################
    def AjouterArticle(self):
        try:
            self._mode = self.MODE_ADD
            self.AfficherFormulaire()

        except:
            print ('MainWindow.ajouterArticle Erreur! : ', sys.exc_info()[0], sys.exc_info()[1])

    #############################################################################
    # Supprimer un article
    #############################################################################
    def SupprimerArticle(self):
        try:
            if self._tableWidget.selectedItems():
                self._proxy.supprimerArticle(self._tableWidget.selectedItems()[1].text())
                self.afficherArticles()
        except:
            print ('MainWindow.SupprimerArticle Erreur! : ', sys.exc_info()[0], sys.exc_info()[1])
    
    #############################################################################
    # Modifier un article
    #############################################################################
    def ModifierArticle(self):
        try:
            self._mode = self.MODE_MOD
            if self._tableWidget.selectedItems():
                self.AfficherFormulaire(self._tableWidget.selectedItems()[1].text(), 
                                        float(self._tableWidget.selectedItems()[2].text()),
                                        datetime.strptime(self._tableWidget.selectedItems()[3].text(), '%Y-%M-%d').date())                
        except:
            print ('MainWindow.ModifierArticle Erreur! : ', sys.exc_info()[0], sys.exc_info()[1])
            
    #############################################################################
    # Slot fermeture FormArticle
    #############################################################################
    def slot_FormArticle_closed(self, alibelle, aprix, adate):
        try:
            if self._mode == self.MODE_ADD:
                self._proxy.ajouterArticle(alibelle, aprix, adate)
            elif self._mode == self.MODE_MOD:
                self._proxy.modifierArticle(int(self._tableWidget.selectedItems()[0].text()), alibelle, aprix, adate)
            else:
                print('MainWindow.slot_FormArticle_closed : mode inconnu')

            self.afficherArticles()
            self._mode = ''
            
        except:
            print ('MainWindow.slot_FormArticle_closed Erreur! : ', sys.exc_info()[0], sys.exc_info()[1])

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
                self._proxy.ajouterArticle(libelle, prix)
                if i%500 == 0:
                    print('RemplirArticles')
        except:
            print ('MainWindow.RemplirArticles Erreur! : ', sys.exc_info()[0], sys.exc_info()[1])
            
    #############################################################################
    # COMMIT
    #############################################################################
    def CommitSession(self):
        try:
            self._proxy.commitSession()
        except:
            print ('MainWindow.CommitSession Erreur! : ', sys.exc_info()[0], sys.exc_info()[1])
            
    #############################################################################
    # ROLLBACK
    #############################################################################
    def RollbackSession(self):
        try:
            self._proxy.rollbackSession()
        except:
            print ('MainWindow.RollbackSession Erreur! : ', sys.exc_info()[0], sys.exc_info()[1])

    #############################################################################
    # Ferme fenêtre principale
    #############################################################################
    def fermerAppli(self):
        try:
            self.close()
        except:
            print ('MainWindow.RollbackSession Erreur! : ', sys.exc_info()[0], sys.exc_info()[1])


#################################################################################
# programme principal
#################################################################################
if __name__ == "__main__":
    
    print('clientPyQt Main')

    vConnection = sys.argv[1]

    app = QApplication(sys.argv)
    
    vMainWindow = MainWindow(None, vConnection)
    vMainWindow.show()
    
    sys.exit(app.exec_())
#################################################################################
