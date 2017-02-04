# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-02 08:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0006_auto_20170201_1218'),
    ]

    operations = [
        migrations.AddField(
            model_name='coach',
            name='points',
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='teamreport',
            name='points',
            field=models.PositiveSmallIntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='coach',
            name='league',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coachs', to='tournament.League'),
        ),
    ]
