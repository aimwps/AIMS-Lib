# Generated by Django 3.2.7 on 2021-11-29 14:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Benchmark', '0001_initial'),
        ('Paths', '0003_delete_pathwayprogressiontracker'),
    ]

    operations = [
        migrations.AddField(
            model_name='pathwaycontent',
            name='benchmark',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Benchmark.benchmark'),
        ),
    ]
