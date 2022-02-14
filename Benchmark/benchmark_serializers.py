from rest_framework import serializers
from .models import Benchmark, Question, Answer, BenchmarkSession, BenchmarkSessionQuestion
from QuestionGenerator.models import GeneratedQuestionBank


class AnswerSafeSerializer(serializers.ModelSerializer):
    class Meta:
      model = Answer
      fields = ('id', "answer_text",)


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
      model = Answer
      fields = ('id', "on_question", "is_correct", "answer_text", "is_default")

class QuestionSafeSerializer(serializers.ModelSerializer):
    answers = AnswerSafeSerializer(many=True)
    class Meta:
      model = Question
      fields = ('id', "on_benchmark", "question_text", "answer_type", "order_position", 'answers', 'num_correct_answers', "total_session_questions","time_to_answer", "session_default_time")

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    class Meta:
      model = Question
      fields = ('id', "on_benchmark", "question_text", "answer_type", "order_position", 'answers', "time_to_answer")


class BenchmarkSerializer(serializers.ModelSerializer):
  questions = QuestionSerializer(many=True)
  class Meta:
    model = Benchmark
    fields = (
        'id',
        'title',
        'description',
        'questions',
        "max_num_questions",
        "randomize_questions",
        "default_answer_seconds",
        "override_time_with_default",
        "library_type",
        "library_description",
        "library_title",
        )


class GeneratedQuestionBankSerializer(serializers.ModelSerializer):
  class Meta:
    model = GeneratedQuestionBank
    fields = ('id',"create_date", "create_time", "source_type", "source_id", "question", "answer", "user_proof")


class BenchmarkSessionQuestionSerializer(serializers.ModelSerializer):
    question = QuestionSafeSerializer()
    class Meta:
        model = BenchmarkSessionQuestion
        fields = (
            "id",
            "question",
            "answered_correctly",
            "given_answer",
            "remaining_time_to_answer",

        )

class BenchmarkSessionSerializer(serializers.ModelSerializer):
    session_questions = BenchmarkSessionQuestionSerializer(many=True)
    class Meta:
        model = BenchmarkSession
        fields = (
                "id",
                "for_user",
                "on_benchmark",
                "session_questions",
                "completion_type",
                "completed",
                "create_date",
                "create_time",
                "completion_date",
                "completion_time",
                "session_result",
                )
