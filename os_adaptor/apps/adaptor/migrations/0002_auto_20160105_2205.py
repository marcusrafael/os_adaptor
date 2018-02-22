# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adaptor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='apf',
            name='description',
            field=models.CharField(default='default description', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='attribute',
            name='description',
            field=models.CharField(default='default description', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='operator',
            name='description',
            field=models.CharField(default='default description', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tenant',
            name='description',
            field=models.CharField(default='default description', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='value',
            name='description',
            field=models.CharField(default='default description', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='operatormapping',
            name='apf_operator',
            field=models.ForeignKey(related_name='apf_operator', to='adaptor.Operator'),
        ),
        migrations.AlterField(
            model_name='operatormapping',
            name='local_operator',
            field=models.ForeignKey(related_name='local_operator', to='adaptor.Operator'),
        ),
        migrations.AlterField(
            model_name='valuemapping',
            name='apf_value',
            field=models.ForeignKey(related_name='apf_value', to='adaptor.Value'),
        ),
        migrations.AlterField(
            model_name='valuemapping',
            name='local_value',
            field=models.ForeignKey(related_name='local_value', to='adaptor.Value'),
        ),
    ]
