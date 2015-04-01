# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comfy', '0004_auto_20150401_0039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='winner',
            field=models.IntegerField(default=0, choices=[(0, 'Pending'), (1, 'Team 1'), (2, 'Team 2'), (3, 'Closed/Returned')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='hash',
            field=models.CharField(default='888bc9c519363375d0b74c411eb22c74684e87b0bcf2ea6227599da916854dd9', max_length=256),
            preserve_default=True,
        ),
    ]
