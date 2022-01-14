# Generated by Django 3.2.9 on 2022-01-12 15:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Organisations', '0004_remove_organisation_members'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisationmembers',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_members', to=settings.AUTH_USER_MODEL),
        ),
    ]