# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-20 13:31
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hrop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(db_index=True, verbose_name='Time hroping')),
                ('period', models.PositiveIntegerField(default=0)),
                ('response_time', models.PositiveIntegerField(default=0)),
                ('intensity', models.PositiveIntegerField(default=0)),
                ('track_name', models.CharField(blank=True, default=None, max_length=150)),
                ('volume_track', models.PositiveIntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hrop', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User hrop',
            },
        ),
    ]
