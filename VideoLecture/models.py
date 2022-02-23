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
        return reverse('user-videos')
    @property
    def library_type(self):
        return "VideoLecture"

    @property
    def library_description(self):
        if self.description:
            return self.description
        else:
            return "There is no set description for this video"
    @property
    def library_title(self):
        return self.title
class VideoLectureSession(models.Model):

    ARTICLE_STATUS = (
                        ("pending", "pending"),
                        ("recap", "recap"),
                        ("complete", "complete"),
                        ("incomplete", "incomplete"),
                    )
    for_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="video_sessions")
    on_video = models.ForeignKey(VideoLecture, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=ARTICLE_STATUS, default="pending")
    completion_time = models.PositiveIntegerField()
    create_date = models.DateField(auto_now=False,auto_now_add=True)
    create_time = models.TimeField(auto_now=False,auto_now_add=True)
