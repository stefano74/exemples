#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from serveurweb import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^articles/$', views.articles.as_view(), name='articles_list'),
    url(r'^articles/(?P<article_id>\d+)/$', views.detail_article, name='detail_article'),
    url(r'^familles/$', views.familles.as_view(), name='familles_list'),
    url(r'^familles/(?P<pk>\d+)/$', views.detail_familles.as_view(), name='familles_detail'),
)
