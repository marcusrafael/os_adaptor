# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adaptor', '0004_auto_20160107_1253'),
    ]

    operations = [
        migrations.AddField(
            model_name='attribute',
            name='ontology',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='operator',
            name='ontology',
            field=models.BooleanField(default=False),
        ),
    ]
