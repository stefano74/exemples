#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 19 mars 2015

@author: stefano
'''
from PyQt5 import QtCore
from PyQt5.QtWidgets import *

from clientPyQt import constantes
from clientPyQt.proxy import *


import logging
from _ast import Delete
from functools import partial
from clientPyQt.listwindow import ListWindow

logger = logging.getLogger(__name__)

class MainWindow(QWidget):
    """
        classe de l'écran principale
    """
    def __init__(self, parent=None):
        """
            Constructeur de la classe MainWindow
        """
        super(MainWindow, self).__init__(parent)
        
        try:
            self.__proxy = None
            self.__listwindow = None
            btnCon = QPushButton('Connecter')
            btnDec = QPushButton('Deconnecter')
            btnQui = QPushButton('Quitter')
            self.edtUrl = QLineEdit(constantes.PROXY_URL)
            self.edtUsr = QLineEdit(constantes.PROXY_USER)
            self.edtPwd = QLineEdit(constantes.PROXY_PWD)
            
            btnCon.setMaximumSize(100, 30)
            btnDec.setMaximumSize(100, 30)
            btnQui.setMaximumSize(100, 30)

            self.cmbProxy = QComboBox()
            self.cmbProxy.setMaximumSize(200, 30)
            self.cmbProxy.addItem(constantes.PROXY_XMLRPC)
            self.cmbProxy.addItem(constantes.PROXY_REST)
            self.cmbProxy.addItem(constantes.PROXY_WEB)
            self.cmbProxy.setCurrentText(constantes.PROXY_WEB)

            mainLayout = QVBoxLayout()
            proxyLayout = QHBoxLayout()
            usrLayout = QFormLayout()
            btnLayout = QGridLayout()
            headLayout = QVBoxLayout()
            self.listLayout = QVBoxLayout()
            proxyLayout.addWidget(self.cmbProxy)
            proxyLayout.addWidget(self.edtUrl)
            usrLayout.addRow("User", self.edtUsr)
            usrLayout.addRow("Password", self.edtPwd)
            btnLayout.addWidget(btnQui, 0, 0)
            btnLayout.addWidget(btnCon,0, 5)
            btnLayout.addWidget(btnDec, 0, 6)
            btnLayout.setAlignment(QtCore.Qt.AlignRight)
            headLayout.addLayout(proxyLayout)
            headLayout.addLayout(usrLayout)
            headLayout.addLayout(btnLayout)
            headLayout.setAlignment(QtCore.Qt.AlignTop)
            mainLayout.addLayout(headLayout, )
            mainLayout.addLayout(self.listLayout)
            
            self.setLayout(mainLayout)
            self.setWindowTitle(__name__)
            self.resize(500, 500)
            btnCon.clicked.connect(self.connecter)
            btnDec.clicked.connect(self.deconnecter)
            btnQui.clicked.connect(self.fermerAppli)
#             self.cmbProxy.currentIndexChanged.connect(partial(
#                                                               self.changerProxy,
#                                                               self.cmbProxy.currentText(),
#                                                               self.edtUrl.text()
#                                                               ))            

        except Exception as e:
            logger.exception(e)
            
    def changerProxy(self, aproxy, aconnection):
        """
            change le proxy
            :param aproxy: nom du proxy suivant constantes
            :type aproxy: string 
            :param aconnection: url de connection au serveur
            :type aproxy: string 
        """
        
        try:
            if self.__proxy:
                if type(self.__proxy) == ProxyWeb:
                    self.__proxy.deconnecter()
                Delete(self.__proxy)
            
            if aproxy == constantes.PROXY_XMLRPC:
                self.__proxy = ProxyXMLRPC(aconnection)
            elif aproxy == constantes.PROXY_REST:
                self.__proxy = ProxyREST(aconnection)
            elif aproxy == constantes.PROXY_WEB:
                self.__proxy = ProxyWeb(aconnection)
            else:
                self.__proxy = None
                raise Exception("Erreur changement proxy")
            
        except Exception as e:
            logger.exception(e)
    

    def afficherList(self, aproxy):
        """
            crée la fenetre ListWindow et l'affiche dans listLayout
        """
        self.__listwindow = ListWindow(self, aproxy)
        self.listLayout.addWidget(self.__listwindow)

    def supprimerList(self):
        """
            retire la fenetre ListWindow de listLayout et la supprime
        """
        if self.__listwindow:
            self.listLayout.removeWidget(self.__listwindow)
            self.__listwindow.close()
            del self.__listwindow
            self.__listwindow = None
        
    def connecter(self):
        """
            connecte au serveur
            implémenté uniquement pour ProxyWeb
        """
        try:
            self.changerProxy(self.cmbProxy.currentText(), self.edtUrl.text())
            
            if not self.__proxy.connecter(constantes.PROXY_USER, constantes.PROXY_PWD):
                raise Exception("Erreur connection Proxy")
            
            self.afficherList(self.__proxy)
            
        except Exception as e:
            logger.exception(e)
        
    def deconnecter(self):
        """
            deconnecte du serveur
            implémenté uniquement pour ProxyWeb
        """
        try:
            self.supprimerList()

            if self.__proxy:
                if not self.__proxy.deconnecter():
                    raise Exception("Erreur deconnection Proxy")
            
                del self.__proxy # verifier si del remet à None 
                self.__proxy = None
                
        except Exception as e:
            logger.exception(e)
            
    def fermerAppli(self):
        try:
            if self.__proxy:
                self.__proxy.deconnecter()
            self.close()
                
        except Exception as e:
            logger.exception(e)

