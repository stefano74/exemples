#!/usr/bin/python
# -*- coding: utf-8 -*-


DEBUG = True
"""
Développement : DEBUG = True
Production : DEBUG = False
"""

MODE_ADD = 'add' 
""" MODE Ajout d'un objet"""
MODE_MOD = 'mod' 
""" MODE Modification d'un objet"""

PROXY_XMLRPC    = 'Proxy XML-RPC'
PROXY_REST      = 'Proxy REST'
PROXY_WEB       = 'Proxy WEB'

PROXY_USER      = 'guest'
""" Utilisateur """
PROXY_PWD       = 'guest'
""" Mot de passe """

PROXY_URL   = 'http://localhost:8000'
ADR_XMLRPC  = '/serveurXMLRPC/'
""" URL du serveur XML-RPC """
ADR_REST    = '/serveurREST/'
""" URL du serveur REST """
ADR_WEB     = '/serveurweb/'
""" URL du serveur web - serveur principale """
