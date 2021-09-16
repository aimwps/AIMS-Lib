from django.db import models
from embed_video.fields import EmbedVideoField
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class VideoLecture(models.Model): #### (PERSON)
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    publish_date = models.DateField(auto_now_add=True)
    publish_time = models.TimeField(auto_now_add=True)
    video_link = EmbedVideoField()
    transcript = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"<VideoLecture : {self.title}>"
    def get_absolute_url(self):
        return reverse('skill-paths')
