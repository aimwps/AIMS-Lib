# Generated by Django 3.2.9 on 2022-02-13 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Organisations', '0009_alter_organisation_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]