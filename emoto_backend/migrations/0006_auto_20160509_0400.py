# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-09 04:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('emoto_backend', '0005_auto_20160509_0226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='emoto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='emoto_backend.Emoto'),
        ),
    ]
