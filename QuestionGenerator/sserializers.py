from rest_framework import serializers
from .models import GeneratedQuestionBank


class GeneratedQuestionBankSerializer(serializers.ModelSerializer):
  class Meta:
    model = GeneratedQuestionBank
    fields = ('id',"generated_date", "generated_time", "source_type", "source_id", "question", "answer", "user_proof")
