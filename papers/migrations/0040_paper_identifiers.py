# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-11 12:28
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('papers', '0039_populate_oai_sources'),
    ]

    operations = [
        migrations.AddField(
            model_name='paper',
            name='identifiers',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=512), blank=True, null=True, size=None),
        ),
    ]