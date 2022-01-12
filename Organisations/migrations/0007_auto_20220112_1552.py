# Generated by Django 3.2.9 on 2022-01-12 15:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Organisations', '0006_alter_organisationmembers_organisation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisationmembers',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='organisationmembers',
            name='organisation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='org_memberss', to='Organisations.organisation'),
        ),
    ]
