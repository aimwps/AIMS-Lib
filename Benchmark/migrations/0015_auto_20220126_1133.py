# Generated by Django 3.2.9 on 2022-01-26 11:33

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('Benchmark', '0014_alter_benchmarksessionquestion_question'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='question',
            managers=[
                ('total_correct_answers', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name='benchmarksessionquestion',
            name='benchmark_session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='session_questions', to='Benchmark.benchmarksession'),
        ),
        migrations.AlterField(
            model_name='benchmarksessionquestion',
            name='question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Benchmark.question'),
        ),
    ]
