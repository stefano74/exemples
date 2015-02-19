#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from rest_framework import routers
from serveurREST import views

router = routers.DefaultRouter()
router.register(r'articles', views.ArticlesViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    
]