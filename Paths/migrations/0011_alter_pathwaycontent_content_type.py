# Generated by Django 3.2.9 on 2022-02-22 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Paths', '0010_alter_pathwaypurchase_spent_on_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pathwaycontent',
            name='content_type',
            field=models.CharField(choices=[('Article', 'Article'), ('Video', 'Video'), ('Benchmark', 'Benchmark')], max_length=100),
        ),
    ]
