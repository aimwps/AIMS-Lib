from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date
from django.db.models import Q
from django.core.validators import MaxValueValidator, MinValueValidator
from ckeditor.fields import RichTextField
from embed_video.fields import EmbedVideoField
from rest_framework import serializers

# class QuizModelManager(models.Manager):
#     def get_by_natural_key(self, title):
#         return self.get(title=title)
# class QuestionModelManager(models.Manager):
#     def get_by_natural_key(self, on_quiz, question_text, answer_type, order_by, answer_text,question_answers):
#         return self.get(on_quiz=on_quiz, question_text=question_text, answer_type=answer_type, order_by=order_by, question_answers=question_answers)
# class AnswerModelManager(models.Manager):
#     def get_by_natural_key(self, to_question, is_correct, answer_text):
#         return self.get(to_question=to_question,is_correct=is_correct, answer_text=answer_text)


class Pathway(models.Model): #### (GROUP)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pathway_creator')
    title = models.CharField(max_length=255)
    participants = models.ManyToManyField(User, blank=True, related_name="pathway_users")
    description = models.TextField(blank=True)
    # organisations = models.ManyToManyField(User, blank=True, related_name="pathway_users")
    # public_records = models.BooleanField()
    # is_cloneable = models.BooleanField()
    def get_absolute_url(self):
        return reverse('skill-paths')
    def __str__(self):
        return f"pathway_{self.id}"

class Quiz(models.Model): # A collection of questions
    # objects = QuizModelManager()
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    publish_date = models.DateField(auto_now_add=True)
    publish_time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"quiz_{self.id}"
    def get_absolute_url(self):
        return reverse('user-benchmarks')
    # def natural_key(self):
    #     return (self.title,)
class GeneratedQuestionBank(models.Model):
    SOURCE_TYPE = (("transcript","transcript"),
                            ("literature","literature"),
                            ("document", "document"))
    PROOF_OPTIONS = (("perfect", "perfect"),
                    ("editable", "editable"),
                    ("incorrect","incorrect"),
                    ("unknown", "unknown"))

    generated_date = models.DateField(auto_now_add=True)
    generated_time = models.TimeField(auto_now_add=True)
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    source_type = models.CharField(max_length=255, choices=SOURCE_TYPE)
    source_id = models.PositiveIntegerField()
    question = models.TextField()
    answer = models.TextField()
    user_proof = models.CharField(max_length=255, choices=PROOF_OPTIONS, default="unknown")

class QuizQuestion(models.Model):

    ANSWER_TYPES = (("multiple-choice", "Multiple choice"),
                    ("multiple-correct-choice","Multiple correct choices"),
                    ("text-entry-exact", "Text entry (Exact)"),
                    ("text-entry-nearest", "Text entry (Close enough)"))

    on_quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    question_text = models.TextField()
    answer_type = models.CharField(max_length=255, choices=ANSWER_TYPES, default="text-entry-exact")
    order_by = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['on_quiz', 'order_by'],
                name='question_order_by'
            )
        ]
    def __str__(self):
        return f"QuizQuestion_{self.id}"

class QuizAnswer(models.Model):
    # objects = AnswerModelManager()
    to_question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name="answers")
    is_correct = models.BooleanField()
    answer_text = models.TextField()
    # def natural_key(self):
    #     return (self.to_question, self.is_correct, self.answer_text)
    def __str__(self):
        return f"<QuizAnswer>"

class VideoLecture(models.Model): #### (PERSON)
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    publish_date = models.DateField(auto_now_add=True)
    publish_time = models.TimeField(auto_now_add=True)
    video_link = EmbedVideoField()
    transcript = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"<VideoLecture : {self.title}>"
    def get_absolute_url(self):
        return reverse('skill-paths')

class WrittenLecture(models.Model): # A body of text with extra elements e.g. Data Tables, recipes or images
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    publish_date = models.DateField(auto_now_add=True)
    publish_time = models.TimeField(auto_now_add=True)
    body = RichTextField(config_name="article_editor", )
    def __str__(self):
        return f"<WrittenLecture : {self.title}>"
    def get_absolute_url(self):
        return reverse('skill-paths')

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
    must_revise_continous = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['pathway', 'order_by'],
                name='pathway_order_by'
            )
        ]
        get_latest_by ='order_by'
    def get_next_order_by(self):
        max_rated_entry = self.objects.latest()
        return int(max_rated_entry.details) + 1

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

class WrittenLectureCompletionRecord(models.Model):
    RECORD_STATUS = (('first_completion', 'first_completion'),
                    ('did_not_complete', 'did_not_complete'),
                    ('recap_completion', 'recap_completion'))
    record_status = models.CharField(max_length=100, choices=RECORD_STATUS)
    pathway_to_complete = models.ForeignKey(PathwayCompletitionRecords, on_delete=models.CASCADE)

class QuizLectureCompletionRecord(models.Model):
    RECORD_STATUS = (('first_completion', 'first_completion'),
                    ('did_not_complete', 'did_not_complete'),
                    ('recap_completion', 'recap_completion'))
    record_status = models.CharField(max_length=100, choices=RECORD_STATUS)
    pathway_to_complete = models.ForeignKey(PathwayCompletitionRecords, on_delete=models.CASCADE)
