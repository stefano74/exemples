#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 16 mars 2015

@author: stefano
'''
from django.forms.models import ModelForm
from serveurweb.core.models import Articles, Familles

class form_article(ModelForm):
    class Meta:
        model = Articles
        fields = '__all__'

class form_famille(ModelForm):
    class Meta:
        model = Familles
        fields = '__all__'