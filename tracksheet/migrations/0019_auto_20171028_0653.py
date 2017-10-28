# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-28 06:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracksheet', '0018_auto_20171028_0644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='employee', serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
