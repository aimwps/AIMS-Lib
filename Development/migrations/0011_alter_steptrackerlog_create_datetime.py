# Generated by Django 3.2.9 on 2021-12-09 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Development', '0010_auto_20211206_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='steptrackerlog',
            name='create_datetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
