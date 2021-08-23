# Generated by Django 3.2.5 on 2021-08-23 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Development', '0002_trackerminaim_user_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='trackerboolean',
            name='user_status',
            field=models.CharField(choices=[('deleted', 'deleted'), ('active', 'active'), ('inactive', 'inactive'), ('completed', 'completed')], default='active', max_length=100),
        ),
    ]
