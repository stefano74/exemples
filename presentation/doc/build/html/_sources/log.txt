.. Client Test PyQt5 documentation master file, created by
   sphinx-quickstart on Wed Mar 25 15:21:47 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

***
Log
***

.. automodule:: log
   :members:

dictionnaire de configuration des logs *dict_log*::

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