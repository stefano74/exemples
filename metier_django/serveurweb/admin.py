#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin
from serveurweb.models import Articles, Familles


class ArticlesAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Famille', {'fields': ['famille']}),
        (None,      {'fields': ['libelle']}),
        (None,      {'fields': ['prix']}),
        (None,      {'fields': ['date']}),
    ]

    list_display = ('famille', 'libelle', 'prix', 'date')
    
    list_filter = ['libelle']
    
# Register your models here.

admin.site.register(Articles, ArticlesAdmin)
#admin.site.register(Articles)
admin.site.register(Familles)