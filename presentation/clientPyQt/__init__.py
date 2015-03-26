#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import gettext

# internationalisation
pathname = os.path.dirname(sys.argv[0])
localedir = os.path.abspath(pathname) + "/locale"

lang_en = gettext.translation('messages', localedir=localedir, languages=['en_GB'])
lang_fr = gettext.translation('messages', localedir=localedir, languages=['fr_FR'])
lang_fr.install() # choix de la langue

# prend le fichier messages.mo correspondant le répertoire locale/${LANGUAGE}/LC_MESSAGES/
# utilise directement la variable systeme LANGUAGE d'ubuntu 
# pas besoin de définir lang_en, lang_fr
# gettext.install("messages", localedir)
