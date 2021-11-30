from rest_framework import serializers
from .models import PathwayContent, Pathway



class PathwayContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PathwayContent
        fields = ("id","content_type", "article", "video", "benchmark", "order_position", "complete_previous", "revise_continuous")

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
