# Generated by Django 3.2.6 on 2021-09-10 10:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Paths', '0018_auto_20210910_1024'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizanswer',
            name='genereated_from',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Paths.generatedquestionbank'),
        ),
    ]
