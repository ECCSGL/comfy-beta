# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comfy', '0005_auto_20150401_0040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='state',
            field=models.IntegerField(default=1, choices=[(1, 'Open'), (2, 'Live'), (3, 'Finished'), (4, 'Processed')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='hash',
            field=models.CharField(max_length=256, default='a6b71307ac7cd11e57fbbb2f4e3dc35cc221aaa26c7bbadc11f2bee8d34db7f0'),
            preserve_default=True,
        ),
    ]
