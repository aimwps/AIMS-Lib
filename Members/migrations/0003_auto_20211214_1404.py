# Generated by Django 3.2.9 on 2021-12-14 14:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Members', '0002_alter_memberprofile_day_reset_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='memberprofile',
            name='day_reset_time',
        ),
        migrations.AddField(
            model_name='memberprofile',
            name='day_reset_hour',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(23)]),
        ),
    ]
