# Generated by Django 3.2.6 on 2021-09-13 10:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Paths', '0021_rename_genereated_from_quizquestion_generated_from'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quizanswer',
            old_name='genereated_from',
            new_name='generated_from',
        ),
    ]