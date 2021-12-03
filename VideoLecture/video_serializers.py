from rest_framework import serializers
from .models import VideoLecture

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
      model = VideoLecture
      fields = (
                "title",
                "author",
                "create_date",
                "create_time",
                "modify_date",
                "modify_time",
                "video_link",
                "transcript",
                "notes",
                )
