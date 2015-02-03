#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from serveurweb.models import Articles

# Create your views here.

def index(request):
    list_articles = Articles.objects.all()
    context = {'list_articles' : list_articles, 'page_titre' : 'Liste des articles'}
    
    return render(request, 'serveurweb/index.html', context)