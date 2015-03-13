#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from serveurweb.user import views
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^connexion/$', (views.connexion), name='connexion'),
    url(r'^deconnexion/$', login_required(views.deconnexion), name='deconnexion'),
)