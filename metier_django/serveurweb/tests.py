#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.test import TestCase
from serveurweb.models import Familles, Articles
from _datetime import date

# Create your tests here.

class Test_Familles(TestCase):
    """
    classe de test pour le model Familles
    """    
    def test_defaultfamille(self):
        """
        teste la présence d'une famille par défaut avec identifiant 1
        """
        
        famille_defaut= Familles.objects.get(pk=1)
        self.assertEqual(famille_defaut.libelle, "par défaut")
        
    def test_create_famille(self):
        """
        teste la sauvegarde d'une famille
        """
        
        famille = Familles(libelle="test")
        famille.save()
        famille = Familles.objects.get(libelle="test")
        self.assertEqual(famille.libelle, "test")
        
class Test_Articles(TestCase):
    """
    classe de test pour le model Articles
    """    
    
    def test_create__article(self):
        """
        teste la sauvegarde d'un article
        """
        article = Articles(libelle="test", prix=2, date=date.today())
        article.save()
        article = Articles.objects.get(libelle="test")
        self.assertEqual(article.prix, 2)
        self.assertEqual(article.date, date.today())
        self.assertEqual(article.famille.id, 1) # prend la famille par défaut lors de la création
        self.assertEqual(article.famille.libelle, "par défaut") # prend la famille par défaut lors de la création
