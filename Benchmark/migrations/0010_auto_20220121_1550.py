# Generated by Django 3.2.9 on 2022-01-21 15:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Benchmark', '0009_benchmarksession_benchmarksessionquestion'),
    ]

    operations = [
        migrations.AddField(
            model_name='benchmarksession',
            name='completion_type',
            field=models.CharField(choices=[('testing', 'testing'), ('submission', 'submission')], default='testing', max_length=255),
        ),
        migrations.AddField(
            model_name='benchmarksession',
            name='for_user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='benchmark_sessions', to='auth.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='benchmarksessionquestion',
            name='given_answer',
            field=models.TextField(blank=True, null=True),
        ),
    ]
