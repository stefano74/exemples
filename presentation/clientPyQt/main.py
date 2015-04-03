#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication

import logging
from clientPyQt import log
from clientPyQt.mainwindow import MainWindow

# configuration log
log.configure()
logger = logging.getLogger(__name__)

"""
    Module principal
    Point d'entrée de l'application clientPyQt
"""
        
            
#################################################################################
# programme principal
#################################################################################
if __name__ == "__main__":
    
    logger.debug('clientPyQt Main')

    app = QApplication(sys.argv)
    
    vMainWindow = MainWindow(None)
    vMainWindow.show()
    
    sys.exit(app.exec_())
#################################################################################
