# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calorie_tracker', '0002_auto_20150529_1829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='date',
            field=models.DateField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='meal',
            name='text',
            field=models.CharField(default=b'', max_length=64),
        ),
        migrations.AlterField(
            model_name='meal',
            name='time',
            field=models.TimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='expected_calories',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
