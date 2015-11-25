# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HostInfo',
            fields=[
                ('hostname', models.CharField(max_length=64, serialize=False, verbose_name='\u4e3b\u673a\u540d', primary_key=True)),
                ('memory', models.CharField(max_length=1024, verbose_name='\u5185\u5b58')),
                ('disk', models.CharField(max_length=1024, verbose_name='\u78c1\u76d8')),
                ('cpu', models.CharField(max_length=1024, verbose_name='Cpu')),
                ('os', models.CharField(max_length=1024, verbose_name='OS')),
                ('ip', models.CharField(max_length=64, verbose_name='IP', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Monitoring_data',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_date', models.DateField(verbose_name='\u6536\u96c6\u65f6\u95f4')),
                ('type', models.CharField(max_length=16, verbose_name='\u6570\u636e\u7c7b\u578b', choices=[(b'cpu', b'cpu'), (b'diskio', b'diskio'), (b'memory', b'memory'), (b'network', b'network')])),
                ('data', models.CharField(default=b'', max_length=1024, verbose_name='\u6570\u636e')),
                ('hostname', models.ForeignKey(to='home_app.HostInfo')),
            ],
        ),
    ]
