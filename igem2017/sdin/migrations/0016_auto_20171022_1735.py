# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-22 17:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sdin', '0015_auto_20171022_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyword',
            name='medalRelation',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='keyword',
            name='suggestedPart',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='keyword',
            name='suggestedProject',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='keyword',
            name='trackRelation',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='keyword',
            name='weightedRelated',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='keyword',
            name='yearRelation',
            field=models.CharField(max_length=1000),
        ),
    ]