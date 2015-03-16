# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('libelle', models.CharField(max_length=20, unique=True)),
                ('prix', models.FloatField()),
                ('date', models.DateField(default=datetime.date.today)),
            ],
            options={
                'db_table': 'articles',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Familles',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('libelle', models.CharField(max_length=20, unique=True)),
            ],
            options={
                'db_table': 'familles',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='articles',
            name='famille',
            field=models.ForeignKey(default=1, to='core.Familles'),
            preserve_default=True,
        ),
    ]
