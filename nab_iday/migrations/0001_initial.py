# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('description', models.CharField(unique=True, max_length=255)),
                ('state', models.CharField(choices=[('neutral', 'neutral'), ('plus', 'plus'), ('minus', 'minus')], default='neutral', max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
