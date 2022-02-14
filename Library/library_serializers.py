from rest_framework import serializers
from .models import Bookmark
from Paths.models import Pathway
from Paths.pathway_serializers import PathwaySerializer
from VideoLecture.models import VideoLecture
from VideoLecture.video_serializers import VideoSerializer
from WrittenLecture.models import Article
from WrittenLecture.article_serializers import ArticleSerializer
from Benchmark.models import Benchmark
from Benchmark.benchmark_serializers import BenchmarkSerializer
from Development.models import Aim
from Development.development_serializers import AimLibrarySerializer
from Organisations.models import Organisation
from Organisations.organisation_serializers import OrganisationSerializer


class BookmarkSerializer(serializers.ModelSerializer):
    article = ArticleSerializer()
    video = VideoSerializer()
    benchmark = BenchmarkSerializer()
    pathway = PathwaySerializer()
    organisation = OrganisationSerializer()
    aim = AimLibrarySerializer()
    class Meta:
        model = Bookmark
        fields = (  "content_type",
                    "article",
                    "video",
                    "benchmark",
                    "pathway",
                    "organisation",
                    "aim",
                    )
