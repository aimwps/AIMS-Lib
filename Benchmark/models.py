from django.db import models
from QuestionGenerator.models import GeneratedQuestionBank
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Q

class Benchmark(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateField(auto_now_add=True)
    create_time = models.TimeField(auto_now_add=True)
    def __str__(self):
        return f"Benchmark_{self.id}"
    def get_success_url(self):
        return reverse('edit-benchmark', kwargs={'benchmark_id' : self.object.pk})

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(Quiz, self).get_form_kwargs(
            *args, **kwargs)
        return kwargs


class Question(models.Model):

    ANSWER_TYPES = (("multiple-choice", "Multiple choice"),
                    ("multiple-correct-choice","Multiple correct choices"),
                    ("text-entry-exact", "Text entry (Exact)"),
                    ("text-entry-nearest", "Text entry (Close enough)"))

    on_quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    generator_source = models.ForeignKey(GeneratedQuestionBank, on_delete=models.SET_NULL, blank=True, null=True)
    source_was_modified  = models.BooleanField(blank=True, null=True)
    question_text = models.TextField()
    answer_type = models.CharField(max_length=255, choices=ANSWER_TYPES, default="text-entry-exact")
    order_position = models.PositiveIntegerField()
    create_date = models.DateField(auto_now_add=True)
    create_time = models.TimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['on_quiz', 'order_position'],
                name='question_order_position'
            )
        ]
    def __str__(self):
        return f"Question_{self.id}"

class Answer(models.Model):
    on_question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name="answers")
    generator_source = models.ForeignKey(GeneratedQuestionBank, on_delete=models.SET_NULL, blank=True, null=True)
    source_was_modified = models.BooleanField(blank=True, null=True)
    answer_text = models.TextField()
    is_correct = models.BooleanField()
    is_default = models.BooleanField(unique=true)
    order_position = models.PositiveIntegerField()
    create_date = models.DateField(auto_now_add=True)
    create_time = models.TimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['to_question', 'order_position'],
                name='answer_order_position'
            ),
            models.UniqueConstraint(
                fields=['to_question'],
                conditon=Q(is_default=True),
                name='default_correct_answer'
            )
        ]

    def __str__(self):
        return f"Answer_{self.id}"
