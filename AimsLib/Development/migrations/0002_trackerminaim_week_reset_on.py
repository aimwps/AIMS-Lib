# Generated by Django 3.2.5 on 2021-07-29 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Development', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trackerminaim',
            name='week_reset_on',
            field=models.CharField(choices=[('start date day', 'The day of the week you start your tracker'), ('Members profile', 'The day set on your user profile')], default='start date day', max_length=100),
        ),
    ]
