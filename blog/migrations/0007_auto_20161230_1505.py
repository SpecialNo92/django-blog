# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-30 14:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20161229_2340'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'get_latest_by': 'date_added', 'ordering': ['-date_added', 'title'], 'permissions': (('user_add_his', 'User can add his posts'), ('user_edit_his', 'User can edit his posts'), ('user_remove_his', 'User can remove his posts'))},
        ),
    ]
