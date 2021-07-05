from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date
from Development.models import SkillArea
from ckeditor.fields import RichTextField


# Create your models here.
class MemberProfile(models.Model):
    user_profile = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    power_quote = models.TextField(max_length=255, null=True, blank=True)
    profile_picture =  models.ImageField(null=True, blank=True, upload_to="path to images") ### STILL NEED TO SET IMAGE PATHS
    biography = RichTextField(blank=True, null=True)
    personal_website = models.CharField(max_length=255, null=True, blank=True)
    linked_in = models.CharField(max_length=255, null=True, blank=True)
    #social_media = models.CharField(max_length=255, null=True, blank=True)
    # social_media = models.CharField(max_length=255, null=True, blank=True)
    # social_media = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.user_profile)
