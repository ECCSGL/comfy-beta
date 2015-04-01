# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comfy', '0003_auto_20150401_0037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='team_1',
            field=models.ForeignKey(to='comfy.Team', null=True, related_name='matches_as_team_1'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='match',
            name='team_2',
            field=models.ForeignKey(to='comfy.Team', null=True, related_name='matches_as_team_2'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='hash',
            field=models.CharField(default='81bd4c26104b76175364e5fad6921381115f37d4255d1a3ef7ec2049ae34fc4f', max_length=256),
            preserve_default=True,
        ),
    ]
