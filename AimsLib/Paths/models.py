from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date
from django.db.models import Q
from django.core.validators import MaxValueValidator, MinValueValidator
from ckeditor.fields import RichTextField
from embed_video.fields import EmbedVideoField

class Pathway(models.Model): #### (GROUP)
    title = models.CharField(max_length=255)
    participants = models.ManyToManyField(User, blank=True)
    # def get_absolute_url(self):
    #     return reverse('skill-paths')
        #return reverse('home')

class Quiz(models.Model): # A collection of questions
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    publish_date = models.DateField(auto_now_add=True)
    publish_time = models.TimeField(auto_now_add=True)
    def __str__(self):
        return f"<Quiz : {self.title}>"
    # def get_absolute_url(self):
    #     return reverse('skill-paths')
        #return reverse('home')



class QuizQuestion(models.Model):
    ANSWER_TYPES = (("multiple-choice", "Multiple choice"),
                    ("multiple-correct-choice","Multiple correct choices"),
                    ("text-entry-exact", "Text entry (Exact)"),
                    ("text-entry-nearest", "Text entry (Close enough)"))

    on_quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.TextField()
    answer_type = models.CharField(max_length=255, choices=ANSWER_TYPES)
    order_by = models.PositiveIntegerField()
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['on_quiz', 'order_by'],
                name='question_order_by'
            )
        ]
    def __str__(self):
        return f"<QuizQuestion : {self.answer_type}>"
    # def get_absolute_url(self):
    #     return reverse('skill-paths')
        #return reverse('home')

class QuizAnswer(models.Model):
    to_question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    is_correct = models.BooleanField()
    answer_text = models.TextField()
    def __str__(self):
        return f"<QuizAnswer>"
    # def get_absolute_url(self):
    #     return reverse('skill-paths')
        #return reverse('home')




class VideoLecture(models.Model): #### (PERSON)
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    publish_date = models.DateField(auto_now_add=True)
    publish_time = models.TimeField(auto_now_add=True)
    video_link = EmbedVideoField()
    transcript = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"<VideoLecture : {self.title}>"
    # def get_absolute_url(self):
    #     return reverse('skill-paths')
        #return reverse('home')

class WrittenLecture(models.Model): # A body of text with extra elements e.g. Data Tables, recipes or images
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    publish_date = models.DateField(auto_now_add=True)
    publish_time = models.TimeField(auto_now_add=True)
    body = RichTextField(config_name="article_editor", )
    def __str__(self):
        return f"<WrittenLecture : {self.title}>"
    # def get_absolute_url(self):
    #     return reverse('skill-paths')
        #return reverse('home')

class PathwayContentSetting(models.Model):
    PATHWAY_CONTENT_TYPE = (("video-lecture","Video Lecture"),
                            ("written-lecture","Written Lecture"),
                            ("quiz","Knowledge Incrementer"),)
    pathway = models.ForeignKey(Pathway, on_delete=models.CASCADE, related_name='full_pathway')
    content_type = models.CharField(max_length=255, choices=PATHWAY_CONTENT_TYPE)
    video_lecture = models.ForeignKey(VideoLecture, on_delete=models.CASCADE, blank=True, null=True)
    written_lecture = models.ForeignKey(WrittenLecture, on_delete=models.CASCADE, blank=True, null=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, blank=True, null=True)
    order_by = models.PositiveIntegerField()
    must_complete_previous = models.BooleanField()
    is_refreshable = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['pathway', 'order_by'],
                name='pathway_order_by'
            )
        ]

class PathwayCompletitionRecords(models.Model):
    record_date = models.DateField(auto_now_add=True)
    record_time = models.TimeField(auto_now_add=True)
    pathway_content = models.ForeignKey(PathwayContentSetting, on_delete=models.CASCADE)

class VideoLectureCompletionRecord(models.Model):
    RECORD_STATUS = (('first_completion', 'first_completion'),
                    ('did_not_complete', 'did_not_complete'),
                    ('recap_completion', 'recap_completion'))
    record_status = models.CharField(max_length=100, choices=RECORD_STATUS)
    pathway_to_complete = models.ForeignKey(PathwayCompletitionRecords, on_delete=models.CASCADE)
