# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comfy', '0002_auto_20150401_0012'),
    ]

    operations = [
        migrations.AddField(
            model_name='bet',
            name='output',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bet',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, 'Pending'), (1, 'Won'), (2, 'Lost'), (3, 'Closed')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='match',
            name='state',
            field=models.IntegerField(default=0, choices=[(1, 'Open'), (2, 'Live'), (3, 'Finished'), (4, 'Processed')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='match',
            name='winner',
            field=models.IntegerField(choices=[(0, 'Pending'), (1, 'Team 1'), (2, 'Team 2'), (3, 'Closed/Returned')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='hash',
            field=models.CharField(max_length=256, default='ac472162b79b992d5ada9e90b470f0f0a04d8303a20967609bc54f932f4b7fe3'),
            preserve_default=True,
        ),
    ]
