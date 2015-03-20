#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 19 mars 2015

@author: stefano
'''
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, \
    QLabel, QLineEdit, QDateEdit
from PyQt5.QtCore import pyqtSignal
    

import logging
from _datetime import date

logger = logging.getLogger(__name__)

class DetailWindow(QWidget):
    """
        classe detail d'un modèle
        lié à la fenêtre list window
    """
    
    _signal_closed = pyqtSignal()

    def __init__(self, parent=None, aSignal = None, aLibelle = '', aPrix = 0, aDate = date.today):
        """
            Constructeur class DetailWindow
        """
        super(DetailWindow, self).__init__(parent)
        
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
