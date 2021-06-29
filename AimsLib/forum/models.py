from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date



class Post(models.Model):
    title = models.CharField(max_length=255)
    skill_area = models.CharField(max_length=255, default="None set")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_date = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.title + ' | ' + str(self.author) #This changes the displayed object name into relevant text information

    def get_absolute_url(self):
        return reverse('forum-topic-view', args=(str(self.id)))
        #return reverse('home')
