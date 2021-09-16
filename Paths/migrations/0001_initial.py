# Generated by Django 3.2.7 on 2021-09-16 08:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Benchmark', '0001_initial'),
        ('WrittenLecture', '0001_initial'),
        ('VideoLecture', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Pathway',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pathway_creator', to=settings.AUTH_USER_MODEL)),
                ('participants', models.ManyToManyField(blank=True, related_name='pathway_users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PathwayCompletitionRecords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_date', models.DateField(auto_now_add=True)),
                ('record_time', models.TimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='WrittenLectureCompletionRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_status', models.CharField(choices=[('first_completion', 'first_completion'), ('did_not_complete', 'did_not_complete'), ('recap_completion', 'recap_completion')], max_length=100)),
                ('pathway_to_complete', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Paths.pathwaycompletitionrecords')),
            ],
        ),
        migrations.CreateModel(
            name='VideoLectureCompletionRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_status', models.CharField(choices=[('first_completion', 'first_completion'), ('did_not_complete', 'did_not_complete'), ('recap_completion', 'recap_completion')], max_length=100)),
                ('pathway_to_complete', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Paths.pathwaycompletitionrecords')),
            ],
        ),
        migrations.CreateModel(
            name='QuizLectureCompletionRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_status', models.CharField(choices=[('first_completion', 'first_completion'), ('did_not_complete', 'did_not_complete'), ('recap_completion', 'recap_completion')], max_length=100)),
                ('pathway_to_complete', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Paths.pathwaycompletitionrecords')),
            ],
        ),
        migrations.CreateModel(
            name='PathwayContentSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_type', models.CharField(choices=[('video-lecture', 'Video Lecture'), ('written-lecture', 'Written Lecture'), ('quiz', 'Knowledge Incrementer')], max_length=255)),
                ('order_by', models.PositiveIntegerField()),
                ('must_complete_previous', models.BooleanField()),
                ('must_revise_continous', models.BooleanField(default=True)),
                ('pathway', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='full_pathway', to='Paths.pathway')),
                ('quiz', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Benchmark.quiz')),
                ('video_lecture', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='VideoLecture.videolecture')),
                ('written_lecture', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='WrittenLecture.writtenlecture')),
            ],
            options={
                'get_latest_by': 'order_by',
            },
        ),
        migrations.AddField(
            model_name='pathwaycompletitionrecords',
            name='pathway_content',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Paths.pathwaycontentsetting'),
        ),
        migrations.AddConstraint(
            model_name='pathwaycontentsetting',
            constraint=models.UniqueConstraint(fields=('pathway', 'order_by'), name='pathway_order_by'),
        ),
    ]
