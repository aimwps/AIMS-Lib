# Generated by Django 3.2.9 on 2021-12-14 11:03

import ckeditor.fields
import datetime
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
            name='MemberProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('power_quote', models.TextField(blank=True, max_length=255, null=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='path to images')),
                ('biography', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('personal_website', models.CharField(blank=True, max_length=255, null=True)),
                ('linked_in', models.CharField(blank=True, max_length=255, null=True)),
                ('day_reset_time', models.TimeField(default=datetime.time(5, 0))),
                ('week_reset_day', models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], default='Monday', max_length=100)),
                ('month_reset_day', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(31)])),
                ('year_reset_month', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)])),
                ('create_date', models.DateField(auto_now_add=True)),
                ('create_time', models.TimeField(auto_now_add=True)),
                ('modify_date', models.DateField(auto_now=True)),
                ('modify_time', models.TimeField(auto_now=True)),
                ('author', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
