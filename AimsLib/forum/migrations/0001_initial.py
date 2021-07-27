# Generated by Django 3.2.5 on 2021-07-22 13:59

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
        ('Development', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('body', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('publish_date', models.DateField(auto_now_add=True)),
                ('publish_time', models.TimeField(auto_now_add=True)),
                ('topic_snippet', models.TextField(default='A short snippet on your topic', max_length=500)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('dev_area', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Development.developmentcategory')),
            ],
        ),
        migrations.CreateModel(
            name='VoteUpDown',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('is_up_vote', models.BooleanField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('votee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('publish_date', models.DateField(auto_now_add=True)),
                ('publish_time', models.TimeField(auto_now_add=True)),
                ('modify_date', models.DateField(auto_now=True)),
                ('modify_time', models.TimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('on_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='forum.post')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('body', models.TextField(max_length=500)),
                ('publish_date', models.DateField(auto_now_add=True)),
                ('publish_time', models.TimeField(auto_now_add=True)),
                ('modify_date', models.DateField(auto_now=True)),
                ('modify_time', models.TimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
        ),
    ]
