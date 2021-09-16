from rest_framework import serializers
from .models import Quiz, QuizQuestion, QuizAnswer
from QuestionGenerator.models import GeneratedQuestionBank

class QuizAnswerSerializer(serializers.ModelSerializer):
    class Meta:
      model = QuizAnswer
      fields = ('id', "to_question", "is_correct", "answer_text")

class QuizQuestionSerializer(serializers.ModelSerializer):
    answers = QuizAnswerSerializer(many=True)
    class Meta:
      model = QuizQuestion
      fields = ('id', "on_quiz", "question_text", "answer_type", "order_by", 'answers')

class QuizSerializer(serializers.ModelSerializer):
  questions = QuizQuestionSerializer(many=True)
  class Meta:
    model = Quiz
    fields = ('id', 'title', "questions")


class GeneratedQuestionBankSerializer(serializers.ModelSerializer):
  class Meta:
    model = GeneratedQuestionBank
    fields = ('id',"generated_date", "generated_time", "source_type", "source_id", "question", "answer", "user_proof")
