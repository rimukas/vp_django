# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-01 19:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vart', '0007_auto_20161001_1911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sutartis',
            name='pastaba',
            field=models.CharField(max_length=200, null=True, verbose_name='Pastaba'),
        ),
    ]