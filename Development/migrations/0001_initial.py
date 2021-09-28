# Generated by Django 3.2.7 on 2021-09-28 10:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('WebsiteTools', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aim',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('motivation', models.TextField(blank=True, null=True)),
                ('user_status', models.CharField(choices=[('deleted', 'deleted'), ('active', 'active'), ('inactive', 'inactive'), ('completed', 'completed')], default='active', max_length=100)),
                ('order_position', models.PositiveIntegerField(default=9999)),
                ('create_date', models.DateField(auto_now_add=True, null=True)),
                ('create_time', models.TimeField(auto_now_add=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='WebsiteTools.contentcategory')),
            ],
        ),
        migrations.CreateModel(
            name='Behaviour',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('user_status', models.CharField(choices=[('deleted', 'deleted'), ('active', 'active'), ('inactive', 'inactive'), ('completed', 'completed')], default='active', max_length=100)),
                ('order_position', models.PositiveIntegerField()),
                ('create_date', models.DateField(auto_now_add=True, null=True)),
                ('create_time', models.TimeField(auto_now_add=True, null=True)),
                ('on_aim', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Development.aim')),
            ],
        ),
        migrations.CreateModel(
            name='StepTracker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metric_tracker_type', models.CharField(choices=[('maximize', 'Count Up'), ('minimize', 'Count Down'), ('boolean', 'Yes or No')], max_length=100)),
                ('metric_action', models.TextField(blank=True, null=True)),
                ('metric_unit', models.CharField(max_length=100)),
                ('metric_number_display_type', models.CharField(choices=[('float', 'Upto 2 decimal places'), ('integer', 'Whole number only')], max_length=100)),
                ('metric_min', models.FloatField()),
                ('metric_max', models.FloatField()),
                ('minimum_show_allowed', models.BooleanField()),
                ('minimum_show_description', models.TextField(blank=True, null=True)),
                ('record_start_date', models.TimeField(auto_now_add=True, null=True)),
                ('record_frequency', models.CharField(choices=[('daily', 'daily'), ('weekly', 'weekly'), ('monthly', 'monthly'), ('yearly', 'yearly'), ('custom', 'custom')], max_length=100)),
                ('record_multiple_per_frequency', models.BooleanField()),
                ('complete_criteria', models.CharField(choices=[('consecutive', 'consecutive'), ('total', 'total')], max_length=100)),
                ('complete_value', models.PositiveIntegerField()),
                ('user_status', models.CharField(choices=[('deleted', 'deleted'), ('active', 'active'), ('inactive', 'inactive'), ('completed', 'completed')], default='active', max_length=100)),
                ('order_position', models.PositiveIntegerField()),
                ('create_date', models.DateField(auto_now_add=True, null=True)),
                ('create_time', models.TimeField(auto_now_add=True, null=True)),
                ('on_behaviour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trackers', to='Development.behaviour')),
            ],
        ),
        migrations.AddConstraint(
            model_name='steptracker',
            constraint=models.UniqueConstraint(fields=('on_behaviour', 'order_position'), name='unique_order_of_trackers'),
        ),
        migrations.AddConstraint(
            model_name='behaviour',
            constraint=models.UniqueConstraint(fields=('on_aim', 'order_position'), name='unique_order_of_behaviours'),
        ),
        migrations.AddConstraint(
            model_name='aim',
            constraint=models.UniqueConstraint(fields=('author', 'order_position'), name='unique_order_of_aims'),
        ),
    ]
