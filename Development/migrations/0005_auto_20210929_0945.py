# Generated by Django 3.2.7 on 2021-09-29 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Development', '0004_alter_steptracker_record_start_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='steptracker',
            name='metric_number_display_type',
        ),
        migrations.AddField(
            model_name='steptracker',
            name='complete_endpoint',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='steptracker',
            name='metric_int_only',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='steptracker',
            name='complete_criteria',
            field=models.CharField(choices=[('consecutive', 'consecutive'), ('total', 'total')], default='consecutive', max_length=100),
        ),
        migrations.AlterField(
            model_name='steptracker',
            name='complete_value',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='steptracker',
            name='create_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='steptracker',
            name='create_time',
            field=models.TimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='steptracker',
            name='metric_max',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='steptracker',
            name='metric_min',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='steptracker',
            name='metric_tracker_type',
            field=models.CharField(choices=[('maximize', 'Count Up'), ('minimize', 'Count Down'), ('boolean', 'Yes or No')], max_length=100),
        ),
        migrations.AlterField(
            model_name='steptracker',
            name='metric_unit',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='steptracker',
            name='minimum_show_allowed',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='steptracker',
            name='record_frequency',
            field=models.CharField(choices=[('daily', 'daily'), ('weekly', 'weekly'), ('monthly', 'monthly'), ('yearly', 'yearly'), ('custom', 'custom')], max_length=100),
        ),
        migrations.AlterField(
            model_name='steptracker',
            name='record_multiple_per_frequency',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='steptracker',
            name='record_start_date',
            field=models.DateField(),
        ),
    ]
