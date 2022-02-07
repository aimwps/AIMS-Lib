from django.db import models
from QuestionGenerator.models import GeneratedQuestionBank
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Q

class Benchmark(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    max_num_questions = models.PositiveIntegerField(default=20)
    randomize_questions = models.BooleanField(default=True, choices=((True, 'Yes'), (False, 'No')))
    default_answer_seconds = models.PositiveIntegerField(default=180)
    override_time_with_default = models.BooleanField(default=True, choices=((True, 'Yes'), (False, 'No')))
    create_date = models.DateField(auto_now_add=True)
    create_time = models.TimeField(auto_now_add=True)
    percent_to_pass = models.PositiveIntegerField(default=70)
    def __str__(self):
        return f"Benchmark_{self.title}"
    def get_success_url(self):
        return reverse('edit-benchmark', kwargs={'benchmark_id' : self.object.pk})

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(Benchmark, self).get_form_kwargs(*args, **kwargs)
        return kwargs

    @property
    def total_session_questions(self):
        return min(self.max_num_questions, self.questions.count())
    @property
    def approx_session_length(self):
        if self.override_time_with_default:
            return min(self.max_num_questions, self.questions.count()) * self.default_answer_seconds //60
        else:
            if self.questions.count() == 0:
                return 0
            else:
                times_to_answer = self.questions.values_list('time_to_answer', flat=True)
                average_time_to_answer = sum(list(times_to_answer)) / times_to_answer.count()

                return ( min(self.max_num_questions, self.questions.count()) * average_time_to_answer) // 60

class Question(models.Model):

    ANSWER_TYPES = (("multiple-choice", "Multiple choice"),
                    ("multiple-correct-choice","Multiple correct choices"),
                    ("text-entry-exact", "Text entry (Exact)"),
                    ("text-entry-nearest", "Text entry (Close enough)"))

    on_benchmark = models.ForeignKey(Benchmark, on_delete=models.CASCADE, related_name="questions")
    generator_source = models.ForeignKey(GeneratedQuestionBank, on_delete=models.SET_NULL, blank=True, null=True, related_name="question_source")
    source_was_modified  = models.BooleanField(blank=True, null=True)
    question_text = models.TextField()
    answer_type = models.CharField(max_length=255, choices=ANSWER_TYPES, default="text-entry-exact")
    order_position = models.PositiveIntegerField()
    create_date = models.DateField(auto_now_add=True)
    create_time = models.TimeField(auto_now_add=True)
    time_to_answer = models.PositiveIntegerField(default=30)



    class Meta:
        ordering = ["order_position"]
        constraints = [
            models.UniqueConstraint(
                fields=['on_benchmark', 'order_position'],
                name='question_order_position'
            )
        ]
    def __str__(self):
        return f"Question_{self.id}"
    @property
    def num_correct_answers(self):
        return self.answers.filter(is_correct=True).count()

    @property
    def total_session_questions(self):
        return min(self.on_benchmark.questions.count(), self.on_benchmark.max_num_questions)

    @property
    def session_default_time(self):
        if self.on_benchmark.override_time_with_default:
            return self.on_benchmark.default_answer_seconds
        else:
            return self.time_to_answer


class Answer(models.Model):
    on_question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    generator_source = models.ForeignKey(GeneratedQuestionBank, on_delete=models.SET_NULL, blank=True, null=True, related_name="answer_source")
    source_was_modified = models.BooleanField(blank=True, null=True)
    answer_text = models.TextField()
    is_correct = models.BooleanField(default=True,choices=((True, 'Yes'), (False, 'No')))
    is_default = models.BooleanField(default=False,choices=((True, 'Yes'), (False, 'No')))
    order_position = models.PositiveIntegerField()
    create_date = models.DateField(auto_now_add=True)
    create_time = models.TimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['on_question', 'order_position'],
                name='answer_order_position'
            ),
            models.UniqueConstraint(
                fields=['on_question'],
                condition=Q(is_default=True),
                name='default_correct_answer'
            )
        ]

    def __str__(self):
        return f"Answer_{self.id}"

class BenchmarkSession(models.Model):
    COMPLETION_TYPES = (("testing", "testing"),
                        ("submission", "submission"))
    for_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="benchmark_sessions")
    on_benchmark = models.ForeignKey(Benchmark, on_delete=models.SET_NULL, null=True)
    completion_type = models.CharField(max_length=255, choices=COMPLETION_TYPES, default="testing")
    completed = models.BooleanField(default=False)
    # result = models.PositiveIntegerField(blank=True, null=True)
    create_date = models.DateField(auto_now_add=True)
    create_time = models.TimeField(auto_now_add=True)
    completion_date = models.DateField(blank=True, null=True)
    completion_time = models.TimeField(blank=True, null=True)
    class Meta:
        ordering = ["-create_date", "-create_time"]
    @property
    def session_result(self):
        total_questions = BenchmarkSessionQuestion.objects.filter( Q(benchmark_session=self) ).count()
        print(total_questions)
        total_correct_questions = BenchmarkSessionQuestion.objects.filter(Q(benchmark_session=self),
        Q(answered_correctly=True)).count()
        if total_correct_questions > 0:
            return round( (total_correct_questions / float(total_questions)) * 100, 2)
        else:
            return 0

    @property
    def status(self):
        if self.session_result > self.on_benchmark.percent_to_pass:
            return "complete"
        else:
            return "recap"





class BenchmarkSessionQuestion(models.Model):
    QUESTION_STATUS = (("b_skipped", "skipped"),
                        ("d_abandoned", "abandoned"),
                        ("c_complete", "complete"),
                        ("a_pending", "pending"))
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
    benchmark_session = models.ForeignKey(BenchmarkSession, on_delete=models.CASCADE, related_name="session_questions")
    question_status = models.CharField(max_length=100, choices=QUESTION_STATUS, default="a_pending")
    answered_correctly = models.BooleanField(blank=True, null=True)
    remaining_time_to_answer = models.PositiveIntegerField(blank=True, null=True)
    given_answer = models.TextField(blank=True, null=True)
    create_date = models.DateField(auto_now_add=True)
    create_time = models.TimeField(auto_now_add=True)
