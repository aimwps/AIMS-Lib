from rest_framework import serializers
from .models import PathwayContent, Pathway
from WrittenLecture.article_serializers import ArticleSerializer
from VideoLecture.video_serializers import VideoSerializer
from Benchmark.benchmark_serializers import BenchmarkSerializer


class PathwayContentSerializer(serializers.ModelSerializer):
    article = ArticleSerializer()
    video = VideoSerializer()
    benchmark = BenchmarkSerializer()
    class Meta:
        model = PathwayContent
        fields = ("id","content_type", "article", "video", "benchmark", "order_position", "complete_to_move_on", "complete_anytime_overide", "revise_frequency")

    def get_queryset(self):
        queryset = PathwayContent.objects.all().order_by('order_position')
        return queryset

class PathwaySerializer(serializers.ModelSerializer):
    full_pathway = PathwayContentSerializer(many=True)
    class Meta:
        model = Pathway
        fields = (
            "id",
            "title",
            "description",
            "create_date",
            "create_time",
            "modify_date",
            "modify_time",
            "full_pathway",
                )
