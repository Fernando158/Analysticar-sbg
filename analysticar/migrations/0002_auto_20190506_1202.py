# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-05-06 16:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysticar', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='client_id',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='client_secret',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]