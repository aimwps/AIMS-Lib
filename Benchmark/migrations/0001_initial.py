# Generated by Django 3.2.9 on 2021-12-14 11:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('QuestionGenerator', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Benchmark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('create_date', models.DateField(auto_now_add=True)),
                ('create_time', models.TimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_was_modified', models.BooleanField(blank=True, null=True)),
                ('question_text', models.TextField()),
                ('answer_type', models.CharField(choices=[('multiple-choice', 'Multiple choice'), ('multiple-correct-choice', 'Multiple correct choices'), ('text-entry-exact', 'Text entry (Exact)'), ('text-entry-nearest', 'Text entry (Close enough)')], default='text-entry-exact', max_length=255)),
                ('order_position', models.PositiveIntegerField()),
                ('create_date', models.DateField(auto_now_add=True)),
                ('create_time', models.TimeField(auto_now_add=True)),
                ('generator_source', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='question_source', to='QuestionGenerator.generatedquestionbank')),
                ('on_benchmark', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='Benchmark.benchmark')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_was_modified', models.BooleanField(blank=True, null=True)),
                ('answer_text', models.TextField()),
                ('is_correct', models.BooleanField()),
                ('is_default', models.BooleanField(unique=True)),
                ('order_position', models.PositiveIntegerField()),
                ('create_date', models.DateField(auto_now_add=True)),
                ('create_time', models.TimeField(auto_now_add=True)),
                ('generator_source', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='answer_source', to='QuestionGenerator.generatedquestionbank')),
                ('on_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='Benchmark.question')),
            ],
        ),
        migrations.AddConstraint(
            model_name='question',
            constraint=models.UniqueConstraint(fields=('on_benchmark', 'order_position'), name='question_order_position'),
        ),
        migrations.AddConstraint(
            model_name='answer',
            constraint=models.UniqueConstraint(fields=('on_question', 'order_position'), name='answer_order_position'),
        ),
        migrations.AddConstraint(
            model_name='answer',
            constraint=models.UniqueConstraint(condition=models.Q(('is_default', True)), fields=('on_question',), name='default_correct_answer'),
        ),
    ]
