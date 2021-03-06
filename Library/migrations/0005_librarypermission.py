# Generated by Django 3.2.9 on 2022-02-22 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Library', '0004_auto_20220216_1242'),
    ]

    operations = [
        migrations.CreateModel(
            name='LibraryPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('can_be_previewed', models.BooleanField(default=False)),
                ('can_be_viewed', models.BooleanField(default=False)),
                ('can_be_bookmarked', models.BooleanField(default=False)),
                ('can_be_added_to_external_content', models.BooleanField(default=False)),
                ('author_pathways_hidden', models.BooleanField(default=False)),
                ('author_development_hidden', models.BooleanField(default=True)),
            ],
        ),
    ]
