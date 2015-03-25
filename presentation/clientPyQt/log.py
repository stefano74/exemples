#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
    Created on 18 mars 2015

    @author: stefano

    Module de configuration des logs

    :Example:

    logger = logging.getLogger(__name__)
    
    logger.debug('trace de debug')
'''

import logging
from clientPyQt import constantes

from logging.config import dictConfig


dict_log = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'log.RequireDebugTrue',
        },
    },    
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(levelname)s %(message)s',
        'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
        'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'null': {
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'development_logfile': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/tmp/clientPyQt_dev.log',
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount' : 7,
            'formatter': 'verbose'
        },
        'production_logfile': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/tmp/clientPyQt_prod.log',
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount' : 7,
            'formatter': 'simple'
        },
    },
    'loggers': {
                'py.warnings': {
                    'handlers': ['console', 'development_logfile',],
                },
                '': {
                     'handlers': ['console', 'production_logfile', 'development_logfile'],
                     'level': "DEBUG",
                },
    }
}

def configure():
    """
        Configure les log avec dict_log
    """
    dictConfig(dict_log)
    
class RequireDebugFalse(logging.Filter):
    """
        classe de filtre pour DEBUG = False
    """
    def filter(self, record):
        return not constantes.DEBUG
    
class RequireDebugTrue(logging.Filter):
    """
        classe de filtre pour DEBUG = True
    """
    def filter(self, record):
        return constantes.DEBUG