# Generated by Django 3.2.5 on 2021-08-17 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Paths', '0007_alter_pathwaycontentsetting_content_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videolecture',
            name='video_link',
            field=models.URLField(max_length=1000),
        ),
    ]
