# Generated by Django 3.2.9 on 2022-02-22 13:00

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Paths', '0011_alter_pathwaycontent_content_type'),
        ('Development', '0002_auto_20220213_1336'),
        ('WrittenLecture', '0007_alter_article_description'),
        ('Organisations', '0010_alter_organisation_description'),
        ('VideoLecture', '0005_alter_videolecture_description'),
        ('Benchmark', '0023_alter_question_time_to_answer'),
        ('Library', '0005_librarypermission'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookmark',
            name='for_user',
        ),
        migrations.AddField(
            model_name='librarypermission',
            name='aim',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='permissions', to='Development.aim'),
        ),
        migrations.AddField(
            model_name='librarypermission',
            name='article',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='permissions', to='WrittenLecture.article'),
        ),
        migrations.AddField(
            model_name='librarypermission',
            name='behaviour',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='permissions', to='Development.behaviour'),
        ),
        migrations.AddField(
            model_name='librarypermission',
            name='benchmark',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='permissions', to='Benchmark.benchmark'),
        ),
        migrations.AddField(
            model_name='librarypermission',
            name='content_type',
            field=models.CharField(choices=[('Article', 'Article'), ('VideoLecture', 'Video'), ('Benchmark', 'Benchmark'), ('Pathway', 'Pathway'), ('Organisation', 'Organisation'), ('Aim', 'Aim'), ('Behaviour', 'Behaviour'), ('StepTracker', 'StepTracker')], default='Article', max_length=100),
        ),
        migrations.AddField(
            model_name='librarypermission',
            name='create_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='librarypermission',
            name='create_time',
            field=models.TimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='librarypermission',
            name='organisation',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='permissions', to='Organisations.organisation'),
        ),
        migrations.AddField(
            model_name='librarypermission',
            name='pathway',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='permissions', to='Paths.pathway'),
        ),
        migrations.AddField(
            model_name='librarypermission',
            name='steptracker',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='permissions', to='Development.steptracker'),
        ),
        migrations.AddField(
            model_name='librarypermission',
            name='video',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='permissions', to='VideoLecture.videolecture'),
        ),
    ]
