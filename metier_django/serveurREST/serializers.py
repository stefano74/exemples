#!/usr/bin/python
# -*- coding: utf-8 -

from rest_framework import serializers
from serveurweb.models import Articles


class ArticlesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Articles
        fields = ('id', 'libelle', 'prix', 'date')
