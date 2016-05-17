# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-17 00:56
from __future__ import unicode_literals

from django.db import migrations, models
import emoto_backend.models


class Migration(migrations.Migration):

    dependencies = [
        ('emoto_backend', '0008_auto_20160509_0512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emoto',
            name='image',
            field=models.ImageField(upload_to=emoto_backend.models.s3_emoto_upload),
        ),
    ]
