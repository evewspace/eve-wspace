# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Map', '0004_auto_20151229_1537'),
    ]

    operations = [
        migrations.AddField(
            model_name='wsystem',
            name='static3',
            field=models.ForeignKey(related_name='tertiary_statics', blank=True, to='Map.WormholeType', null=True),
        ),
    ]
