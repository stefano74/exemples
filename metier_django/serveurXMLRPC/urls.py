#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'django_xmlrpc.views.handle_xmlrpc', name='xmlrpc'),
# url(r'^$', 'serveurXMLRPC.views.rpc_handler', name='rpc_handler'),
)
