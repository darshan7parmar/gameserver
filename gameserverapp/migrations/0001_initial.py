# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-04 06:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_status', models.CharField(max_length=20)),
                ('turn_seq', models.CharField(max_length=20)),
                ('words_done', models.CharField(max_length=20)),
                ('scores', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nick', models.CharField(max_length=20)),
                ('player_id', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='admin_player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='admin_player', to='gameserverapp.Player'),
        ),
        migrations.AddField(
            model_name='game',
            name='current_player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='current_player', to='gameserverapp.Player'),
        ),
        migrations.AddField(
            model_name='game',
            name='players',
            field=models.ManyToManyField(to='gameserverapp.Player'),
        ),
    ]
