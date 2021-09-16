# Generated by Django 3.2.7 on 2021-09-16 08:07

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Aim',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('why', models.TextField(blank=True, null=True)),
                ('user_status', models.CharField(choices=[('deleted', 'deleted'), ('active', 'active'), ('inactive', 'inactive'), ('completed', 'completed')], default='active', max_length=100)),
                ('in_order', models.PositiveIntegerField(default=9999)),
            ],
        ),
        migrations.CreateModel(
            name='Lever',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('in_order', models.PositiveIntegerField()),
                ('user_status', models.CharField(choices=[('deleted', 'deleted'), ('active', 'active'), ('inactive', 'inactive'), ('completed', 'completed')], default='active', max_length=100)),
                ('on_aim', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Development.aim')),
            ],
        ),
        migrations.CreateModel(
            name='TrackerBoolean',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metric_description', models.TextField(max_length=500)),
                ('frequency', models.CharField(choices=[('daily', 'daily'), ('weekly', 'weekly'), ('monthly', 'monthly'), ('yearly', 'yearly')], max_length=100)),
                ('frequency_quantity', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('complete_criteria', models.CharField(choices=[('consecutive', 'consecutive'), ('total', 'total')], max_length=100)),
                ('complete_value', models.PositiveIntegerField()),
                ('has_prompt', models.BooleanField(default=True)),
                ('has_timeout', models.BooleanField(default=True)),
                ('has_public_logs', models.BooleanField(default=False)),
                ('allows_multi_period_logs', models.BooleanField(default=True)),
                ('user_status', models.CharField(choices=[('deleted', 'deleted'), ('active', 'active'), ('inactive', 'inactive'), ('completed', 'completed')], default='active', max_length=100)),
                ('lever', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tracker_boolean', to='Development.lever')),
            ],
        ),
        migrations.CreateModel(
            name='TrackerMinAim',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metric_type', models.CharField(max_length=100)),
                ('metric_min', models.PositiveIntegerField()),
                ('metric_aim', models.PositiveIntegerField()),
                ('metric_description', models.TextField(blank=True, null=True)),
                ('frequency', models.CharField(choices=[('daily', 'daily'), ('weekly', 'weekly'), ('monthly', 'monthly'), ('yearly', 'yearly')], max_length=100)),
                ('frequency_quantity', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('complete_criteria', models.CharField(choices=[('consecutive', 'consecutive'), ('total', 'total')], max_length=100)),
                ('complete_value', models.PositiveIntegerField()),
                ('has_prompt', models.BooleanField(default=True)),
                ('has_timeout', models.BooleanField(default=True)),
                ('has_public_logs', models.BooleanField(default=False)),
                ('allows_multi_period_logs', models.BooleanField(default=True)),
                ('user_status', models.CharField(choices=[('deleted', 'deleted'), ('active', 'active'), ('inactive', 'inactive'), ('completed', 'completed')], default='active', max_length=100)),
                ('lever', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tracker_min_aim', to='Development.lever')),
            ],
        ),
        migrations.CreateModel(
            name='TrackerMinAimRecords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lever_performed', models.BooleanField(default=False)),
                ('record_date', models.DateField(auto_now_add=True)),
                ('record_time', models.TimeField(auto_now_add=True)),
                ('metric_quantity', models.IntegerField(blank=True, null=True)),
                ('tracker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Development.trackerminaim')),
            ],
        ),
        migrations.CreateModel(
            name='TrackerBooleanRecords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lever_performed', models.BooleanField()),
                ('record_date', models.DateField(auto_now_add=True)),
                ('record_time', models.TimeField(auto_now_add=True)),
                ('metric_quantity', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default='Yes')),
                ('tracker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Development.trackerboolean')),
            ],
        ),
        migrations.CreateModel(
            name='SkillArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_area_name', models.CharField(max_length=255)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('forum_rules', models.TextField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DevelopmentCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('global_standard', models.BooleanField(default=False)),
                ('parent_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='Development.developmentcategory')),
            ],
        ),
        migrations.AddField(
            model_name='aim',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Development.developmentcategory'),
        ),
        migrations.AddField(
            model_name='aim',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='lever',
            constraint=models.UniqueConstraint(fields=('on_aim', 'in_order'), name='unique_order_of_levers'),
        ),
        migrations.AddConstraint(
            model_name='aim',
            constraint=models.UniqueConstraint(fields=('user', 'in_order'), name='unique_aims_orderby'),
        ),
    ]
