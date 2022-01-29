from django.db import models
from embed_video.fields import EmbedVideoField
from django.contrib.auth.models import User
from django.urls import reverse

class VideoLecture(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=500,blank=True,  null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateField(auto_now_add=True)
    create_time = models.TimeField(auto_now_add=True)
    modify_date = models.DateField(auto_now=True,auto_now_add=False)
    modify_time = models.TimeField(auto_now=True,auto_now_add=False)
    video_link = EmbedVideoField()
    transcript = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"<VideoLecture : {self.title}>"
    def get_absolute_url(self):
        return reverse('pathways')
