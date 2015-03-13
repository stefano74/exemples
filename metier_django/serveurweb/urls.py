#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
    url(r'^',    include('serveurweb.core.urls')),
    url(r'^user/',    include('serveurweb.user.urls')),
)