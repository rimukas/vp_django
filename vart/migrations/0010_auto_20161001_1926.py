# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-01 19:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vart', '0009_auto_20161001_1923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sutartis',
            name='pastaba',
            field=models.CharField(blank=True, max_length=200, verbose_name='Pastaba'),
        ),
    ]