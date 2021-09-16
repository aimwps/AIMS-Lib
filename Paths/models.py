from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date
from django.db.models import Q
from django.core.validators import MaxValueValidator, MinValueValidator
from embed_video.fields import EmbedVideoField
from rest_framework import serializers
from VideoLecture.models import VideoLecture
from WrittenLecture.models import WrittenLecture
from Benchmark.models import Quiz

class Pathway(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pathway_creator')
    title = models.CharField(max_length=255)
    participants = models.ManyToManyField(User, blank=True, related_name="pathway_users")
    description = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse('skill-paths')
    def __str__(self):
        return f"pathway_{self.id}"



class PathwayContentSetting(models.Model):
    PATHWAY_CONTENT_TYPE = (("video-lecture","Video Lecture"),
                            ("written-lecture","Written Lecture"),
                            ("quiz","Knowledge Incrementer"),)
    pathway = models.ForeignKey(Pathway, on_delete=models.CASCADE, related_name='full_pathway')
    content_type = models.CharField(max_length=255, choices=PATHWAY_CONTENT_TYPE)
    video_lecture = models.ForeignKey(VideoLecture, on_delete=models.CASCADE, blank=True, null=True)
    written_lecture = models.ForeignKey(WrittenLecture, on_delete=models.CASCADE, blank=True, null=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, blank=True, null=True)
    order_by = models.PositiveIntegerField()
    must_complete_previous = models.BooleanField()
    must_revise_continous = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['pathway', 'order_by'],
                name='pathway_order_by'
            )
        ]
        get_latest_by ='order_by'
    def get_next_order_by(self):
        max_rated_entry = self.objects.latest()
        return int(max_rated_entry.details) + 1

class PathwayCompletitionRecords(models.Model):
    record_date = models.DateField(auto_now_add=True)
    record_time = models.TimeField(auto_now_add=True)
    pathway_content = models.ForeignKey(PathwayContentSetting, on_delete=models.CASCADE)

class VideoLectureCompletionRecord(models.Model):
    RECORD_STATUS = (('first_completion', 'first_completion'),
                    ('did_not_complete', 'did_not_complete'),
                    ('recap_completion', 'recap_completion'))
    record_status = models.CharField(max_length=100, choices=RECORD_STATUS)
    pathway_to_complete = models.ForeignKey(PathwayCompletitionRecords, on_delete=models.CASCADE)

class QuizLectureCompletionRecord(models.Model):
    RECORD_STATUS = (('first_completion', 'first_completion'),
                    ('did_not_complete', 'did_not_complete'),
                    ('recap_completion', 'recap_completion'))
    record_status = models.CharField(max_length=100, choices=RECORD_STATUS)
    pathway_to_complete = models.ForeignKey(PathwayCompletitionRecords, on_delete=models.CASCADE)

class WrittenLectureCompletionRecord(models.Model):
    RECORD_STATUS = (('first_completion', 'first_completion'),
                    ('did_not_complete', 'did_not_complete'),
                    ('recap_completion', 'recap_completion'))
    record_status = models.CharField(max_length=100, choices=RECORD_STATUS)
    pathway_to_complete = models.ForeignKey(PathwayCompletitionRecords, on_delete=models.CASCADE)
