# Generated by Django 3.0.4 on 2020-04-04 15:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workout', '0006_auto_20200404_2105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofiledb',
            name='d_o_b',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, null=True),
        ),
    ]
