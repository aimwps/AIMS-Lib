# Generated by Django 3.2.9 on 2022-01-28 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Benchmark', '0018_auto_20220128_1351'),
    ]

    operations = [
        migrations.AddField(
            model_name='benchmarksessionquestion',
            name='remaining_time_to_answer',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
