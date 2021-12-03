from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
      model = Article
      fields = (  "title",
                  "author",
                  "create_date",
                  "create_time",
                  "modify_date",
                  "modify_time",
                  "body", )
