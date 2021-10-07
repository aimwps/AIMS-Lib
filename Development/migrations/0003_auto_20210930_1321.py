# Generated by Django 3.2.7 on 2021-09-30 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Development', '0002_auto_20210930_1314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='steptracker',
            name='metric_tracker_type',
            field=models.CharField(choices=[('maximize', 'Count Up'), ('minimize', 'Count Down'), ('boolean', 'Yes or No')], default='boolean', max_length=100),
        ),
        migrations.AlterField(
            model_name='steptracker',
            name='record_frequency',
            field=models.CharField(choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly'), ('yearly', 'Yearly'), ('custom', 'Specific days')], default='weekly', max_length=100),
        ),
    ]