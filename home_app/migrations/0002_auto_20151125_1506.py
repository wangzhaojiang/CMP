# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hostinfo',
            name='update_time',
            field=models.DateTimeField(verbose_name='\u4e0a\u4e00\u6b21\u66f4\u65b0\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='monitoring_data',
            name='data_date',
            field=models.DateTimeField(verbose_name='\u6536\u96c6\u65f6\u95f4'),
        ),
    ]
