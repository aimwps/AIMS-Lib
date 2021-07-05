from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date
from Development.models import SkillArea
from ckeditor.fields import RichTextField



class Post(models.Model):
    title = models.CharField(max_length=255)
    assigned_skill_area = models.ForeignKey(SkillArea, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    #body = models.TextField()
    body = RichTextField(blank=True, null=True)
    publish_date = models.DateField(auto_now_add=True)
    publish_time = models.TimeField(auto_now_add=True)
    topic_snippet = models.TextField(max_length=500, default="A short snippet on your topic")
    #modify_date = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.title + ' | ' + str(self.author) #This changes the displayed object name into relevant text information

    def get_absolute_url(self):
        return reverse('forum-home')
        #return reverse('home')


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    on_post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    body = models.TextField()
    publish_date = models.DateField(auto_now_add=True)
    publish_time = models.TimeField(auto_now_add=True)
    #modify_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return "<Comment by " + str(self.author)+" to "+str(self.on_post.author) + " on " + str(self.on_post) + ">" #This changes the displayed object name into relevant text information

    def get_absolute_url(self):
        return reverse('forum-home')
        #return reverse('home')


class Reply(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    on_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    #body = models.TextField()
    body = RichTextField(blank=True, null=True)
    publish_date = models.DateField(auto_now_add=True)
    publish_time = models.TimeField(auto_now_add=True)
    #modify_date = models.DateField(auto_now_add=True)


    def __str__(self):
        return "<Reply by " + str(self.author)+">"#This changes the displayed object name into relevant text information

    def get_absolute_url(self):
        return reverse('forum-home')
        #return reverse('home')
