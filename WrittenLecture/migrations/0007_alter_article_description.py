# Generated by Django 3.2.9 on 2022-02-13 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WrittenLecture', '0006_alter_article_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='description',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]