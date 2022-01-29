from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
# Create your models here.
class Article(models.Model): # A body of text with extra elements e.g. Data Tables, recipes or images
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=500,blank=True,  null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateField(auto_now=False,auto_now_add=True)
    create_time = models.TimeField(auto_now=False,auto_now_add=True)
    modify_date = models.DateField(auto_now=True,auto_now_add=False)
    modify_time = models.TimeField(auto_now=True,auto_now_add=False)
    body = RichTextField(config_name="article_editor", )
    def __str__(self):
        return f"<WrittenLecture : {self.title}>"
    def get_absolute_url(self):
        return reverse('"articles-dash"')

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

class ArticleSession(models.Model):

    ARTICLE_STATUS = (
                        ("pending", "pending"),
                        ("recap", "recap"),
                        ("complete", "complete"),
                        ("incomplete", "incomplete"),
                    )
    for_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="article_sessions")
    on_article = models.ForeignKey(Article, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=ARTICLE_STATUS)
    create_date = models.DateField(auto_now=False,auto_now_add=True)
    create_time = models.TimeField(auto_now=False,auto_now_add=True)
    completion_time = models.PositiveIntegerField()
