#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from serveurweb import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^articles/$', views.articles.as_view(), name='articles_list'), # version CBV
    url(r'^articles/add/$', views.AjoutArticle.as_view(), name='AjoutArticle'), # version CBV
    url(r'^articles/(?P<pk>\d+)/$', views.ModifArticle.as_view(), name='ModifArticle'),
    url(r'^articles/(?P<pk>\d+)/del/$', views.SuppressionArticle.as_view(), name='SuppressionArticle'),
    url(r'^familles/$', views.familles.as_view(), name='familles_list'),
    url(r'^familles/add/$', views.ajouter_famille.as_view(), name='ajouter_famille'),
    url(r'^familles/(?P<pk>\d+)/$', views.modifier_famille.as_view(), name='modifier_famille'),
    url(r'^familles/(?P<pk>\d+)/del/$', views.supprimer_famille.as_view(), name='supprimer_famille'),
)