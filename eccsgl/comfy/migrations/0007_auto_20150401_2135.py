# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('comfy', '0006_auto_20150401_0049'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 1, 21, 35, 7, 374202)),
        ),
        migrations.AlterField(
            model_name='user',
            name='hash',
            field=models.CharField(default='d16abab354ededeb441eb61c2ff2f915b7d0d2935489e9fb0694ae4ba268cc70', max_length=256),
        ),
    ]
