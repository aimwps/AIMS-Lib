from django.db import models
from django.contrib.auth.models import User



class Post(models.Model):
    title = models.CharField(max_length=255)
    skill_area = models.CharField(max_length=255, default="None set")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()


    def __str__(self):
        return self.title + ' | ' + str(self.author) #This changes the displayed object name into relevant text information
