#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 13 mars 2015

@author: stefano
'''
from django import forms

class ConnexionForm(forms.Form):
    """
    classe form pour la connexion des utilisateurs
    """
    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)

