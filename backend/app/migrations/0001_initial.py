# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('class_for', models.CharField(max_length=64)),
                ('short_description', models.TextField()),
                ('description', models.TextField()),
                ('location', models.TextField()),
                ('start_datetime', models.DateTimeField()),
                ('end_datetime', models.DateTimeField()),
                ('latitude', models.IntegerField(default=-1)),
                ('longitude', models.IntegerField(default=-1)),
                ('organizer', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
