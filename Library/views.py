from django.shortcuts import render
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
from django.views.generic import View
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q


def LibraryView_ajax_search_library(request):
    search_phrase = request.GET.get("search_phrase")
    pathways = Pathway.objects.filter(Q(title__icontains=search_phrase)| Q(description__icontains=search_phrase))
    videos = VideoLecture.objects.filter(Q(title__icontains=search_phrase)| Q(description__icontains=search_phrase))
    articles = Article.objects.filter(Q(title__icontains=search_phrase)| Q(description__icontains=search_phrase))
    benchmarks = Benchmark.objects.filter(Q(title__icontains=search_phrase)| Q(description__icontains=search_phrase))
    organisations = Organisation.objects.filter(Q(title__icontains=search_phrase)| Q(description__icontains=search_phrase))
    aims = Aim.objects.filter(Q(motivation__icontains=search_phrase) | Q(title__icontains=search_phrase))
    data =  {
            "pathways": PathwaySerializer(pathways, many=True).data ,
            "videos": VideoSerializer(videos, many=True).data,
            "articles": ArticleSerializer(articles, many=True).data,
            "benchmarks": BenchmarkSerializer(benchmarks, many=True).data,
            "organisations": OrganisationSerializer(organisations, many=True).data,
            "aims": AimsLibrarySerializer(aims, many=True).data,
            }
    return JsonResponse(data, safe=False)

class LibraryView(View):
    template_name = "library_view.html"
    def get(self, request):
        context = {}
        return render(request, self.template_name, context)





# Create your views here.
