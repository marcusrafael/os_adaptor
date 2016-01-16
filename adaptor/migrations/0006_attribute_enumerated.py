# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adaptor', '0005_auto_20160107_1328'),
    ]

    operations = [
        migrations.AddField(
            model_name='attribute',
            name='enumerated',
            field=models.BooleanField(default=False),
        ),
    ]
