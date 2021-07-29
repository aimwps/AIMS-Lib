# Generated by Django 3.2.5 on 2021-07-29 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Members', '0002_memberprofile_day_reset_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='memberprofile',
            name='week_reset_day',
            field=models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], default='Monday', max_length=100),
        ),
    ]
