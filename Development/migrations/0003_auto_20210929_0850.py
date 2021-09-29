# Generated by Django 3.2.7 on 2021-09-29 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Development', '0002_auto_20210929_0833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='steptracker',
            name='complete_criteria',
            field=models.CharField(blank=True, choices=[('consecutive', 'consecutive'), ('total', 'total')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='steptracker',
            name='complete_value',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='steptracker',
            name='metric_max',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='steptracker',
            name='metric_min',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='steptracker',
            name='metric_tracker_type',
            field=models.CharField(blank=True, choices=[('maximize', 'Count Up'), ('minimize', 'Count Down'), ('boolean', 'Yes or No')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='steptracker',
            name='metric_unit',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='steptracker',
            name='minimum_show_allowed',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='steptracker',
            name='record_frequency',
            field=models.CharField(blank=True, choices=[('daily', 'daily'), ('weekly', 'weekly'), ('monthly', 'monthly'), ('yearly', 'yearly'), ('custom', 'custom')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='steptracker',
            name='record_multiple_per_frequency',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='steptracker',
            name='record_start_date',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
