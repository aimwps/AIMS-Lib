# Generated by Django 3.2.5 on 2021-07-29 10:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Members', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='memberprofile',
            name='day_reset_time',
            field=models.TimeField(default=datetime.time(5, 0)),
        ),
    ]
