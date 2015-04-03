#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 19 mars 2015

@author: stefano
'''
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, \
    QLabel, QLineEdit, QDateEdit, QFormLayout, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore    

import logging
from _datetime import date

logger = logging.getLogger(__name__)

class DetailWindow(QWidget):
    """
        classe detail d'un modèle
        lié à la fenêtre list window
    """
    
    _signal_closed = pyqtSignal()

    def __init__(self, parent=None, aSignal = None, adictModel = None):
        """
            Constructeur class DetailWindow
        """
        super(DetailWindow, self).__init__(parent)
        
        try:
            self.__dictModel = adictModel
            
            self.btnOk = QPushButton('OK')
            self.btnCancel = QPushButton('Annuler')  
            self.btnOk.setMaximumSize(100, 30)  
            self.btnCancel.setMaximumSize(100, 30)

            self._signal_closed = aSignal
            self.btnOk.clicked.connect(self.AjouterArticle)  
            self.btnCancel.clicked.connect(self.Annuler)  
            
            btnLayout = QHBoxLayout()
            btnLayout.addWidget(self.btnOk)
            btnLayout.addWidget(self.btnCancel)
            btnLayout.setAlignment(QtCore.Qt.AlignRight)

            self.formLayout = QFormLayout()
            for cle, valeur in adictModel['fields'].items():
                lineEdit = QLineEdit(str(valeur))
#                 lineEdit.setObjectName(cle)
                self.formLayout.addRow(cle, lineEdit)
            self.mainLayout = QVBoxLayout()
            self.mainLayout.addLayout(self.formLayout)
            self.mainLayout.addLayout(btnLayout)
            
                        
            self.setLayout(self.mainLayout)
            self.setWindowTitle('Detail')

        except Exception as e:
            logger.exception(e)

    #############################################################################
    # Envoi un signal "Ajouter Un article" à MainWindow
    #############################################################################
    def AjouterArticle(self):
        try:
            # mise à jour du dico avec le formulaire
            for i in range(self.formLayout.count()):
                if (i % 2) == 0:
                    label = self.formLayout.itemAt(i).widget()
                    lineedit = self.formLayout.itemAt(i+1).widget()
                    self.__dictModel['fields'][label.text()] = lineedit.text()
            
            self._signal_closed.emit(self.__dictModel)
            self.close()

        except Exception as e:
            logger.exception(e)
        
    #############################################################################
    # Fermeture ArtForm sans envoi de signal
    #############################################################################
    def Annuler(self):
            self.close()
