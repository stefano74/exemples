# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=20)),
                ('prix', models.FloatField()),
                ('date', models.DateField(default='2015-01-23')),
            ],
            options={
                'db_table': 'articles',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Familles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'familles',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='articles',
            name='famille',
            field=models.ForeignKey(to='serveurweb.Familles', default=1),
            preserve_default=True,
        ),
    ]
