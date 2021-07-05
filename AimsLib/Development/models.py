from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date



class SkillArea(models.Model):
    skill_area_name = models.CharField(max_length=255)
    created_date = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    forum_rules = models.TextField(default="The forum rules for this skill area are..")



    def __str__(self):
        return self.skill_area_name #This changes the displayed object name into relevant text information


# class trainingArticle(models.Model):
#     article_title = models.CharField(max_length=255)
#
