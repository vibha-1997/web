# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-26 12:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0010_auto_20180716_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='selection',
            name='product_cat',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='selection',
            name='user_cat',
            field=models.IntegerField(),
        ),
    ]