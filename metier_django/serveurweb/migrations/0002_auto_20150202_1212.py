# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.apps.registry import apps

def ajoutFammilleDefaut(apps, shema_editor):
    familles = apps.get_model("serveurweb", "Familles")
    f = familles(libelle = 'par défaut')
    f.save()

class Migration(migrations.Migration):

    dependencies = [
        ('serveurweb', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(ajoutFammilleDefaut),
    ]
