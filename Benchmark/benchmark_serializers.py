from rest_framework import serializers
from .models import Benchmark, Question, Answer
from QuestionGenerator.models import GeneratedQuestionBank

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
      model = Answer
      fields = ('id', "on_question", "is_correct", "answer_text", "is_default")

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    class Meta:
      model = Question
      fields = ('id', "on_benchmark", "question_text", "answer_type", "order_position", 'answers')


class BenchmarkSerializer(serializers.ModelSerializer):
  questions = QuestionSerializer(many=True)
  class Meta:
    model = Benchmark
    fields = ('id', 'title','description', 'questions')



class GeneratedQuestionBankSerializer(serializers.ModelSerializer):
  class Meta:
    model = GeneratedQuestionBank
    fields = ('id',"create_date", "create_time", "source_type", "source_id", "question", "answer", "user_proof")
