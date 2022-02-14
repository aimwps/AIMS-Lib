from rest_framework import serializers
from .models import VideoLecture

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
      model = VideoLecture
      fields = ("id",
                "description",
                "title",
                "author",
                "create_date",
                "create_time",
                "modify_date",
                "modify_time",
                "video_link",
                "transcript",
                "notes",
                "library_type",
                "library_description",
                "library_title"
                )
