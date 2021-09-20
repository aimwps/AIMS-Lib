from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date
from ckeditor.fields import RichTextField
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class MemberProfile(models.Model):
    DAY_CHOICES = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
    DAY_CHOICES = ((d,d) for d in DAY_CHOICES)
    user_profile = models.OneToOneField(User, null=True, on_delete=models.CASCADE, related_name="profile")
    power_quote = models.TextField(max_length=255, null=True, blank=True)
    profile_picture =  models.ImageField(null=True, blank=True, upload_to="path to images") ### STILL NEED TO SET IMAGE PATHS
    biography = RichTextField(config_name="article_editor", blank=True, null=True)
    personal_website = models.CharField(max_length=255, null=True, blank=True)
    linked_in = models.CharField(max_length=255, null=True, blank=True)
    day_reset_time = models.TimeField(default=datetime.time(datetime(1800, 12, 25, 5, 0,0,0)))
    week_reset_day = models.CharField(max_length=100, choices=DAY_CHOICES, default="Monday")
    month_reset_day = models.PositiveIntegerField(default=1,validators=[MinValueValidator(1), MaxValueValidator(31)])
    year_reset_month = models.PositiveIntegerField(default=1,validators=[MinValueValidator(1), MaxValueValidator(12)])
    #social_media = models.CharField(max_length=255, null=True, blank=True)
    # social_media = models.CharField(max_length=255, null=True, blank=True)
    # social_media = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.user_profile)
