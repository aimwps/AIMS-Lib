# Generated by Django 3.2.5 on 2021-08-17 12:32

from django.db import migrations
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Paths', '0008_alter_videolecture_video_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videolecture',
            name='video_link',
            field=embed_video.fields.EmbedVideoField(),
        ),
    ]
