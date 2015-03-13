#!/usr/bin/python
# -*- coding: utf-8 -# Create your views here.

from serveurweb.core.models import Articles
from rest_framework import viewsets
from serveurREST.serializers import ArticlesSerializer


class ArticlesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Articles to be viewed or edited.
    """
    queryset = Articles.objects.all()
    serializer_class = ArticlesSerializer