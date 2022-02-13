from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
      model = Article

      fields = ("id",
                "title",
                "description",
                "author",
                "create_date",
                "create_time",
                "modify_date",
                "modify_time",
                "body",
                "library_type",
                "library_description", )
