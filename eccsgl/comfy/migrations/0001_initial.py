# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team', models.IntegerField(default=0)),
                ('amount', models.FloatField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('odds_1', models.IntegerField(default=0)),
                ('odds_2', models.IntegerField(default=0)),
                ('time', models.CharField(max_length=100)),
                ('state', models.IntegerField(choices=[(1, 'Open'), (2, 'Live'), (3, 'Finished')])),
                ('winner', models.IntegerField(choices=[(1, 'Team 1'), (2, 'Team 2'), (3, 'Closed/Returned')])),
                ('processed', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash', models.CharField(max_length=256, default='a0134d7ef58a5d7ff5cbc1d392f573a19078b23d85b53f4e20c411b5e39d722c')),
                ('created', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='match',
            name='team_1',
            field=models.ForeignKey(to='comfy.Team', related_name='matches_as_team_1'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='match',
            name='team_2',
            field=models.ForeignKey(to='comfy.Team', related_name='matches_as_team_2'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bet',
            name='match',
            field=models.ForeignKey(to='comfy.Match'),
            preserve_default=True,
        ),
    ]
