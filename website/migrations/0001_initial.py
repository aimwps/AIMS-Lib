# Generated by Django 3.2.7 on 2021-09-16 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ModuleNavData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nav_title', models.TextField()),
                ('nav_info', models.TextField()),
                ('nav_module', models.CharField(choices=[('pathways', 'pathways'), ('community', 'community'), ('aims', 'aims'), ('library', 'library')], max_length=100)),
                ('module_sub_page', models.CharField(max_length=255)),
            ],
        ),
    ]
