# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adaptor', '0002_auto_20160105_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attribute',
            name='apf',
            field=models.ForeignKey(to='adaptor.Apf', null=True),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='tenant',
            field=models.ForeignKey(to='adaptor.Tenant', null=True),
        ),
    ]
