# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Apf',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('apf', models.ForeignKey(to='adaptor.Apf')),
            ],
        ),
        migrations.CreateModel(
            name='AttributeMapping',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('apf_attribute', models.ForeignKey(related_name='apf_attribute', to='adaptor.Attribute')),
                ('local_attribute', models.ForeignKey(related_name='local_attribute', to='adaptor.Attribute')),
            ],
        ),
        migrations.CreateModel(
            name='Hierarchy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Operator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('apf', models.ForeignKey(to='adaptor.Apf')),
            ],
        ),
        migrations.CreateModel(
            name='OperatorMapping',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('apf_operator', models.ForeignKey(related_name='apf_operator', to='adaptor.Attribute')),
                ('local_operator', models.ForeignKey(related_name='local_operator', to='adaptor.Attribute')),
            ],
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Value',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('attribute', models.ForeignKey(to='adaptor.Attribute')),
            ],
        ),
        migrations.CreateModel(
            name='ValueMapping',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('apf_value', models.ForeignKey(related_name='apf_value', to='adaptor.Attribute')),
                ('local_value', models.ForeignKey(related_name='local_value', to='adaptor.Attribute')),
            ],
        ),
        migrations.AddField(
            model_name='operator',
            name='tenant',
            field=models.ForeignKey(to='adaptor.Tenant'),
        ),
        migrations.AddField(
            model_name='hierarchy',
            name='child',
            field=models.ForeignKey(related_name='child', to='adaptor.Value'),
        ),
        migrations.AddField(
            model_name='hierarchy',
            name='parent',
            field=models.ForeignKey(related_name='parent', to='adaptor.Value'),
        ),
        migrations.AddField(
            model_name='attribute',
            name='tenant',
            field=models.ForeignKey(to='adaptor.Tenant'),
        ),
    ]
