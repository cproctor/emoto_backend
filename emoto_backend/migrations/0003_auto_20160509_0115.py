# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-09 01:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emoto_backend', '0002_auto_20160509_0115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='username',
            field=models.TextField(max_length=100, unique=True),
        ),
    ]
