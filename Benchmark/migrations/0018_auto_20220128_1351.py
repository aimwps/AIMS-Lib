# Generated by Django 3.2.9 on 2022-01-28 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Benchmark', '0017_benchmarksessionquestion_question_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='benchmarksessionquestion',
            name='time_to_answer',
        ),
        migrations.AddField(
            model_name='question',
            name='time_to_answer',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='benchmarksessionquestion',
            name='question_status',
            field=models.CharField(choices=[('b_skipped', 'skipped'), ('d_abandoned', 'abandoned'), ('c_complete', 'complete'), ('a_pending', 'pending')], default='a_pending', max_length=100),
        ),
    ]