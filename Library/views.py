from django.shortcuts import render, get_object_or_404
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

def LibraryView_ajax_get_library_result(request):
    content_type, content_id = request.GET.get("result_phrase").split("_")
    print(content_type, content_id)
    data = {"success":"success"}
    content_type_converter = {
                            "Article": Article,
                            "Video": VideoLecture,
                            "Benchmark": Benchmark,
                            "Pathway": Pathway,
                            "Organisation": Organisation,
                            "Aim": Aim,
                            }
    result = get_object_or_404(content_type_converter[content_type], id=content_id)
    if isinstance(result, VideoLecture):
        data = VideoSerializer(result)
    elif isinstance(result, Article):
        data = ArticleSerializer(result)
    elif isinstance(result, Benchmark):
        data = BenchmarkSerializer(result)
    elif isinstance(result, Pathway):
        data = PathwaySerializer(result)
    elif isinstance(result, Organisation):
        data = OrganisationSerializer(result)
    elif isinstance(result, Aim):
        data = AimLibrarySerializer(result)
    else:
        print("DATA TYPE ERROR FOR SERIALIZATION")
    return JsonResponse(data.data, safe=False)
def LibraryView_ajax_search_library(request):
    search_phrase = request.GET.get("search_phrase")
    pathways = Pathway.objects.filter(Q(title__icontains=search_phrase)| Q(description__icontains=search_phrase)).distinct()
    videos = VideoLecture.objects.filter(Q(title__icontains=search_phrase)| Q(description__icontains=search_phrase)).distinct()
    articles = Article.objects.filter(Q(title__icontains=search_phrase)| Q(description__icontains=search_phrase)).distinct()
    benchmarks = Benchmark.objects.filter(Q(title__icontains=search_phrase)| Q(description__icontains=search_phrase)).distinct()
    organisations = Organisation.objects.filter(Q(title__icontains=search_phrase)| Q(description__icontains=search_phrase)).distinct()
    aims = Aim.objects.filter(Q(motivation__icontains=search_phrase) | Q(title__icontains=search_phrase)).distinct()
    data =  {
            "pathways": PathwaySerializer(pathways, many=True).data ,
            "videos": VideoSerializer(videos, many=True).data,
            "articles": ArticleSerializer(articles, many=True).data,
            "benchmarks": BenchmarkSerializer(benchmarks, many=True).data,
            "organisations": OrganisationSerializer(organisations, many=True).data,
            "aims": AimLibrarySerializer(aims, many=True).data,
            }
    return JsonResponse(data, safe=False)

class LibraryView(View):
    template_name = "library_view.html"
    def get(self, request):
        context = {}
        return render(request, self.template_name, context)





# Create your views here.
