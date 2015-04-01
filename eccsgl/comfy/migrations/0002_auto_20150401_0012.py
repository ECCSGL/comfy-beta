# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comfy', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='hash',
            field=models.CharField(max_length=256, default='bfb845567a836c7e19a83010f9742d1cdef1bc3ae7f805b2e3c1cf65e3aafd0f'),
            preserve_default=True,
        ),
    ]
