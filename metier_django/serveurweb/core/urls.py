#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from serveurweb.core import views
from django.contrib.auth.decorators import login_required


urlpatterns = patterns('',
    url(r'^$', login_required(views.index), name='index'),
    url(r'^articles/$', login_required(views.articles.as_view()), name='articles_list'), # version CBV
    url(r'^articles/add/$', login_required(views.AjoutArticle.as_view()), name='AjoutArticle'), # version CBV
    url(r'^articles/(?P<pk>\d+)/$', login_required(views.ModifArticle.as_view()), name='ModifArticle'),
    url(r'^articles/(?P<pk>\d+)/del/$', login_required(views.SuppressionArticle.as_view()), name='SuppressionArticle'),
    url(r'^familles/$', views.familles.as_view(), name='familles_list'),
    url(r'^familles/add/$', views.ajouter_famille.as_view(), name='ajouter_famille'),
    url(r'^familles/(?P<pk>\d+)/$', views.modifier_famille.as_view(), name='modifier_famille'),
    url(r'^familles/(?P<pk>\d+)/del/$', views.supprimer_famille.as_view(), name='supprimer_famille'),
)