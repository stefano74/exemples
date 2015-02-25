#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from serveurweb import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^articles/$', views.articles.as_view(), name='articles_list'), # version CBV
#     url(r'^articles/$', views.list_articles, name='articles_list'), # version FBV
    url(r'^articles/(?P<article_id>\d+)/$', views.detail_article, name='detail_article'),
    url(r'^articles/(?P<article_id>\d+)/del/$', views.supprimer_article, name='supprimer_article'),
    url(r'^articles/add/$', views.ajouter_article, name='ajouter_article'),
    url(r'^familles/$', views.familles.as_view(), name='familles_list'),
    url(r'^familles/(?P<pk>\d+)/$', views.modifier_famille.as_view(), name='detail_famille'),
    url(r'^familles/(?P<pk>\d+)/edit/$', views.modifier_famille.as_view(), name='modifier_famille'),
    url(r'^familles/(?P<pk>\d+)/del/$', views.supprimer_famille.as_view(), name='supprimer_famille'),
    url(r'^familles/add/$', views.ajouter_famille.as_view(), name='ajouter_famille'),
)