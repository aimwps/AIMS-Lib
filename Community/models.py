from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from datetime import datetime, date
from Development.models import ContentCategory #,SkillArea
from ckeditor.fields import RichTextField


class Topic(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(ContentCategory, null=True,on_delete=models.SET_NULL)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = RichTextField(config_name="article_editor", )
    create_date = models.DateField(auto_now_add=True)
    create_time = models.TimeField(auto_now_add=True)
    snippet = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"Topic_{self.id}"

    def get_absolute_url(self):
        return reverse('forum-home')
        #return reverse('home')

class Reply(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    on_post = models.ForeignKey(Topic, related_name="replies", on_delete=models.CASCADE)
    body = RichTextField(config_name="article_editor", blank=True, null=True)
    create_date = models.DateField(auto_now_add=True)
    create_time = models.TimeField(auto_now_add=True)
    modify_date = models.DateField(auto_now=True,auto_now_add=False)
    modify_time = models.TimeField(auto_now=True,auto_now_add=False)


    def __str__(self):
        return f"Reply_{self.id}"#This changes the displayed object name into relevant text information

    def get_absolute_url(self):
        return reverse('forum-home')
        #return reverse('home')
