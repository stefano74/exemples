#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from _datetime import date

# Create your models here.

class Familles(models.Model):

    libelle = models.CharField(max_length = 20, unique = True) #unicité du libellé
 
    def __str__(self):
        return "<Famille(id='%d', libelle='%s')>" % (self.id, self.libelle)

    class Meta:
        db_table = 'familles'

class Articles(models.Model):
    #id      = models.AutoField(primary_key = True)
    libelle = models.CharField(max_length = 20, unique = True) #unicité du libellé
    famille = models.ForeignKey(Familles, default = 1)
    prix    = models.FloatField()
#     date    = models.DateField(default = '2015-01-23')
    date    = models.DateField(default = date.today)

#     def __str__(self):
#         return "<Article(id='%d', libelle='%s', famille = '%s', prix='%f', date='%s')>" % (self.id, self.libelle, self.famille, self.prix, self.date)

    class Meta:
        db_table = 'articles'
        