# Generated by Django 3.2.9 on 2022-01-19 16:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Benchmark', '0002_auto_20220119_1609'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='answer',
            name='default_correct_answer',
        ),
    ]
