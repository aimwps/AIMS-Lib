# Generated by Django 3.2.7 on 2021-09-29 10:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Development', '0006_alter_steptracker_metric_int_only'),
    ]

    operations = [
        migrations.RenameField(
            model_name='steptracker',
            old_name='complete_endpoint',
            new_name='complete_allowed',
        ),
    ]
