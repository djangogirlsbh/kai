# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-24 22:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(default=1, max_length=10),
            preserve_default=False,
        ),
    ]
