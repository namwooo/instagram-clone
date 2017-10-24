# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-24 07:41
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0002_auto_20171023_0659'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('F', 'Facebook'), ('D', 'Django')], default='D', max_length=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='following_users',
            field=models.ManyToManyField(through='member.Relation', to=settings.AUTH_USER_MODEL),
        ),
    ]
