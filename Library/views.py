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
from .models import Bookmark, LibraryContentType

def LibraryView_ajax_use_content(request):
    print(request.POST)
    if request.method == "POST":
        if "submitCopyAim" in request.POST:

            # get the aim to copy
            aim_to_copy = Aim.objects.get(id=request.POST.get("submitAimCopy"))

            print(f"FOUND AIM: {aim_to_copy.title}")
            print(f"{aim_to_copy.author} vs {request.user}")
            # Check user isn't copying own content
            if aim_to_copy.author == request.user:
                print("add errors to return here ")
            else:
                # Find the app users aims to get an order posiition
                user_aims = Aim.objects.filter(author=request.user)

                # Make a coopy of the aim
                aim_to_copy.pk = None
                aim_to_copy.order_position = 99999
                aim_to_copy.save()

                # Update the copy to the app users details, mark as a copy
                aim_to_copy.author = request.user
                aim_to_copy.order_position = user_aims.count()+1
                aim_to_copy.is_a_copy = True
                aim_to_copy.save()

                # Find the behaviours to update
                behaviours_to_copy = aim_to_copy.behaviours.all()

                # loop through, copy and update the aims behaviours
                for i, behaviour in enumerate(behaviours_to_copy,1):
                    behaviour.pk = None
                    behaviour.save()
                    behaviour.on_aim = aim_to_copy
                    behaviour.order_position = i
                    behaviour.is_a_copy = True
                    trackers_to_copy = behaviour.trackers.all()

                    # loop through, copy and update the behaviours trackers
                    for ii, steptracker in enumerate(trackers_to_copy):
                        step_tracker.pk = None
                        step_tracker.save()
                        step_tracker.on_behaviour = behaviour
                        step_tracker.is_a_copy = True
                        step_tracker.order_position = ii
                        step_tracker.save()
        elif "submitBookmarkAim" in request.POST:
            aim_to_bookmark = Aim.objects.get(id=request.POST.get("submitBookmarkAim"))
            if aim_to_bookmark.author == request.user:
                print("return erros for bookmarking own content")
            else:
                content_type = LibraryContentType.objects.get(content_type="Aim")
                new_bookmark = Bookmark(for_user=request.user,
                                        content_type=content_type,
                                        content_id=aim_to_bookmark.id)
                new_bookmark.save()
            print(request.user.bookmarks.all())


    return JsonResponse({"success":"success"}, safe=False)

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
    aims = Aim.objects.filter(Q(is_a_copy=False) & (Q(motivation__icontains=search_phrase) | Q(title__icontains=search_phrase))).distinct()
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
