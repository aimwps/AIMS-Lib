from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date
from django.db.models import Q
from django.core.validators import MaxValueValidator, MinValueValidator
from ckeditor.fields import RichTextField

class Quiz(models.Model): # A collection of questions
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = RichTextField(config_name="article_editor", )
    publish_date = models.DateField(auto_now_add=True)
    publish_time = models.TimeField(auto_now_add=True)
    def __str__(self):
        return f"<Quiz : {self.title}>"


class QuizQuestion(models.Model):
    ANSWER_TYPES = (("multiple-choice", "Multiple choice"),
                    ("multiple-correct-choice","Multiple correct choices"),
                    ("text-entry-exact", "Text entry (Exact)"),
                    ("text-entry-nearest", "Text entry (Close enough)"))

    on_quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.TextField()
    answer_type = models.CharField(max_length=255, choices=ANSWER_TYPES)
    def __str__(self):
        return f"<QuizQuestion : {self.answer_type}>"

class QuizAnswer(models.Model):
    to_question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    is_correct = models.BooleanField()
    answer_text = models.TextField()
    def __str__(self):
        return f"<QuizAnswer>"

class VideoLecture(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    publish_date = models.DateField(auto_now_add=True)
    publish_time = models.TimeField(auto_now_add=True)
    video_link = models.URLField(max_length=255)
    def __str__(self):
        return f"<VideoLecture : {self.title}>"

class WrittenLecture(models.Model): # A body of text with extra elements e.g. Data Tables, recipes or images
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    publish_date = models.DateField(auto_now_add=True)
    publish_time = models.TimeField(auto_now_add=True)
    body = RichTextField(config_name="article_editor", )
    def __str__(self):
        return f"<WrittenLecture : {self.title}>"
