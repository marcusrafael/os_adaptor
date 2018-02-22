# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adaptor', '0003_auto_20160107_1253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operator',
            name='apf',
            field=models.ForeignKey(to='adaptor.Apf', null=True),
        ),
        migrations.AlterField(
            model_name='operator',
            name='tenant',
            field=models.ForeignKey(to='adaptor.Tenant', null=True),
        ),
    ]
