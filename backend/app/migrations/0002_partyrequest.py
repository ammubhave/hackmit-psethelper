# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartyRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('request_datetime', models.DateTimeField()),
                ('approved', models.BooleanField(default=False)),
                ('party', models.ForeignKey(to='app.Party')),
                ('requestor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
