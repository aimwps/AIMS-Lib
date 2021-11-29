from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date
from django.db.models import Q
from django.core.validators import MaxValueValidator, MinValueValidator
from embed_video.fields import EmbedVideoField
from rest_framework import serializers
from VideoLecture.models import VideoLecture
from WrittenLecture.models import Article
from Benchmark.models import Benchmark
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


CONTENT_TYPE = (('Article', "Article"),
                ('VideoLecture', "Video Lecture"),
                )


class Pathway(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pathway_creator')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    create_date = models.DateField(auto_now=False,auto_now_add=True)
    create_time = models.TimeField(auto_now=False,auto_now_add=True)
    modify_date = models.DateField(auto_now=True,auto_now_add=False)
    modify_time = models.TimeField(auto_now=True,auto_now_add=False)
    def __str__(self):
        return f"pathway_{self.id}"

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(Pathway, self).get_form_kwargs(
            *args, **kwargs)
        return kwargs


class PathwayContent(models.Model):
    on_pathway = models.ForeignKey(Pathway, on_delete=models.CASCADE, related_name='full_pathway')
    content_type =  models.CharField(max_length=100, choices=CONTENT_TYPE)
    article = models.ForeignKey(Article, blank=True, null=True, on_delete=models.CASCADE)
    video = models.ForeignKey(VideoLecture, blank=True, null=True, on_delete=models.CASCADE)
    benchmark = models.ForeignKey(Benchmark, blank=True, null=True, on_delete=models.CASCADE)
    order_position = models.PositiveIntegerField(default=9999)
    create_date = models.DateField(auto_now=False,auto_now_add=True)
    create_time = models.TimeField(auto_now=False,auto_now_add=True)
    modify_date = models.DateField(auto_now=True,auto_now_add=False)
    modify_time = models.TimeField(auto_now=True,auto_now_add=False)
    complete_previous = models.BooleanField()
    revise_continuous = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['on_pathway', 'order_position'],
                name='pathway_order_by'
            )
        ]
        get_latest_by ='order_by'

    def get_next_order_by(self):
        max_rated_entry = self.objects.latest()
        return int(max_rated_entry.details) + 1

class PathwayCompletitionRecord(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_record")
    create_date = models.DateField(auto_now_add=True)
    create_time = models.TimeField(auto_now_add=True)
    pathway_content = models.ForeignKey(PathwayContent, on_delete=models.CASCADE)



class PathwayParticipant(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)#, related_name='pathway_participant')
    on_pathway = models.ForeignKey(Pathway, on_delete=models.CASCADE, related_name="participants")
    create_date = models.DateField(auto_now=False,auto_now_add=True)
    create_time = models.TimeField(auto_now=False,auto_now_add=True)


# class VideoLectureCompletionRecord(models.Model):
#     RECORD_STATUS = (('first_completion', 'first_completion'),
#                     ('did_not_complete', 'did_not_complete'),
#                     ('recap_completion', 'recap_completion'))
#     record_status = models.CharField(max_length=100, choices=RECORD_STATUS)
#     pathway_to_complete = models.ForeignKey(PathwayCompletitionRecords, on_delete=models.CASCADE)
#
# class BenchmarkLectureCompletionRecord(models.Model):
#     RECORD_STATUS = (('first_completion', 'first_completion'),
#                     ('did_not_complete', 'did_not_complete'),
#                     ('recap_completion', 'recap_completion'))
#     record_status = models.CharField(max_length=100, choices=RECORD_STATUS)
#     pathway_to_complete = models.ForeignKey(PathwayCompletitionRecords, on_delete=models.CASCADE)
#
# class WrittenLectureCompletionRecord(models.Model):
#     RECORD_STATUS = (('first_completion', 'first_completion'),
#                     ('did_not_complete', 'did_not_complete'),
#                     ('recap_completion', 'recap_completion'))
#     record_status = models.CharField(max_length=100, choices=RECORD_STATUS)
#     pathway_to_complete = models.ForeignKey(PathwayCompletitionRecords, on_delete=models.CASCADE)
