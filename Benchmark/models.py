from django.db import models
from QuestionGenerator.models import GeneratedQuestionBank
from django.contrib.auth.models import User
from Paths.models import PathwayCompletitionRecords

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    publish_date = models.DateField(auto_now_add=True)
    publish_time = models.TimeField(auto_now_add=True)
    def __str__(self):
        return f"quiz_{self.id}"
    def get_absolute_url(self):
        return reverse('user-benchmarks')

class QuizQuestion(models.Model):

    ANSWER_TYPES = (("multiple-choice", "Multiple choice"),
                    ("multiple-correct-choice","Multiple correct choices"),
                    ("text-entry-exact", "Text entry (Exact)"),
                    ("text-entry-nearest", "Text entry (Close enough)"))

    on_quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    generated_from = models.ForeignKey(GeneratedQuestionBank, on_delete=models.SET_NULL, blank=True, null=True)
    has_been_modified = models.BooleanField(blank=True, null=True)
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

    to_question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name="answers")
    generated_from = models.ForeignKey(GeneratedQuestionBank, on_delete=models.SET_NULL, blank=True, null=True)
    is_correct = models.BooleanField()
    answer_text = models.TextField()

    def __str__(self):
        return f"<QuizAnswer>"


class QuizLectureCompletionRecord(models.Model):
    RECORD_STATUS = (('first_completion', 'first_completion'),
                    ('did_not_complete', 'did_not_complete'),
                    ('recap_completion', 'recap_completion'))
    record_status = models.CharField(max_length=100, choices=RECORD_STATUS)
    pathway_to_complete = models.ForeignKey(PathwayCompletitionRecords, on_delete=models.CASCADE)
