# Generated by Django 3.2.7 on 2021-09-29 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Development', '0003_auto_20210929_0850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='steptracker',
            name='record_start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
