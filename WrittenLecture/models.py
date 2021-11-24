from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
# Create your models here.
class Article(models.Model): # A body of text with extra elements e.g. Data Tables, recipes or images
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateField(auto_now=False,auto_now_add=True)
    create_time = models.TimeField(auto_now=False,auto_now_add=True)
    modify_date = models.DateField(auto_now=True,auto_now_add=False)
    modify_time = models.TimeField(auto_now=True,auto_now_add=False)
    body = RichTextField(config_name="article_editor", )
    def __str__(self):
        return f"<WrittenLecture : {self.title}>"
    def get_absolute_url(self):
        return reverse('pathways')

class ArticleImage(models.Model): # A body of text with extra elements e.g. Data Tables, recipes or images
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateField(auto_now=False,auto_now_add=True)
    create_time = models.TimeField(auto_now=False,auto_now_add=True)
    modify_date = models.DateField(auto_now=True,auto_now_add=False)
    modify_time = models.TimeField(auto_now=True,auto_now_add=False)
    body = RichTextField(config_name="article_editor", )
    def __str__(self):
        return f"<WrittenLecture : {self.title}>"
    def get_absolute_url(self):
        return reverse('skill-paths')

class ArticleText(models.Model): # A body of text with extra elements e.g. Data Tables, recipes or images
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateField(auto_now=False,auto_now_add=True)
    create_time = models.TimeField(auto_now=False,auto_now_add=True)
    modify_date = models.DateField(auto_now=True,auto_now_add=False)
    modify_time = models.TimeField(auto_now=True,auto_now_add=False)
    body = RichTextField(config_name="article_editor", )
    def __str__(self):
        return f"<WrittenLecture : {self.title}>"
    def get_absolute_url(self):
        return reverse('pathways')
