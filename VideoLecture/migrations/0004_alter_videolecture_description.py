# Generated by Django 3.2.9 on 2022-02-13 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VideoLecture', '0003_videolecturesession'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videolecture',
            name='description',
            field=models.TextField(default='There is no description for this benchmark', max_length=500),
        ),
    ]