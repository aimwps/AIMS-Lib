from django.shortcuts import render, get_object_or_404
from Paths.models import Pathway
from Paths.pathway_serializers import PathwaySerializer
from VideoLecture.models import VideoLecture
from VideoLecture.video_serializers import VideoSerializer
from WrittenLecture.models import Article
from WrittenLecture.article_serializers import ArticleSerializer
from Benchmark.models import Benchmark
from Benchmark.benchmark_serializers import BenchmarkSerializer
from Development.models import Aim, Behaviour, StepTracker
from Development.development_serializers import AimLibrarySerializer, StepTrackerSerializer, BehaviourSerializer
from Organisations.models import Organisation
from Organisations.organisation_serializers import OrganisationSerializer
from django.views.generic import View
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from .models import Bookmark, LibraryContentType, LibraryPermission
from .library_serializers import BookmarkSerializer, LibraryPermissionSerializer
def ajax_edit_library_permissions(request):
    if request.method == "POST":
        if request.POST.get("can_be_viewed_in_library") == "true":
            can_be_viewed_in_library = True
        else:
            can_be_viewed_in_library = False

        if request.POST.get("can_be_used") == "true":
            can_be_used = True
        else:
            can_be_used = False

        if request.POST.get("author_visibility_hidden") == "true":
            author_visibility_hidden = True
        else:
            author_visibility_hidden = False

        if "permission_data" in request.POST:
            content_type, content_id = request.POST.get("permission_data").split("_")

            if content_type == "Article":

                item = Article.objects.get(id=content_id)

                new_library_permission = LibraryPermission(
                                content_type = content_type,
                                article = item,
                                can_be_viewed_in_library = can_be_viewed_in_library,
                                can_be_used = can_be_used,
                                author_visibility_hidden = author_visibility_hidden
                )
                new_library_permission.save()

            elif content_type == "Video":
                item = VideoLecture.objects.get(id=content_id)
                new_library_permission = LibraryPermission(
                                content_type = content_type,
                                video = item,
                                can_be_viewed_in_library = can_be_viewed_in_library,
                                can_be_used = can_be_used,
                                author_visibility_hidden = author_visibility_hidden
                )
                new_library_permission.save()

            elif content_type == "Benchmark":
                item = Benchmark.objects.get(id=content_id)
                new_library_permission = LibraryPermission(
                                content_type = content_type,
                                benchmark = item,
                                can_be_viewed_in_library = can_be_viewed_in_library,
                                can_be_used = can_be_used,
                                author_visibility_hidden = author_visibility_hidden
                )
                new_library_permission.save()

            elif content_type == "Pathway":
                item = Pathway.objects.get(id=content_id)
                new_library_permission = LibraryPermission(
                                content_type = content_type,
                                pathway = item,
                                can_be_viewed_in_library = can_be_viewed_in_library,
                                can_be_used = can_be_used,
                                author_visibility_hidden = author_visibility_hidden
                )
                new_library_permission.save()

            elif content_type == "StepTracker":
                item = StepTracker.objects.get(id=content_id)
                new_library_permission = LibraryPermission(
                                content_type = content_type,
                                steptracker = item,
                                can_be_viewed_in_library = can_be_viewed_in_library,
                                can_be_used = can_be_used,
                                author_visibility_hidden = author_visibility_hidden
                )
                new_library_permission.save()
            elif content_type == "Behaviour":
                item = Behaviour.objects.get(id=content_id)
                new_library_permission = LibraryPermission(
                                content_type = content_type,
                                behaviour = item,
                                can_be_viewed_in_library = can_be_viewed_in_library,
                                can_be_used = can_be_used,
                                author_visibility_hidden = author_visibility_hidden
                )
                new_library_permission.save()
            elif content_type == "Aim":
                item = Aim.objects.get(id=content_id)
                new_library_permission = LibraryPermission(
                                content_type = content_type,
                                aim = item,
                                can_be_viewed_in_library = can_be_viewed_in_library,
                                can_be_used = can_be_used,
                                author_visibility_hidden = author_visibility_hidden
                )
                new_library_permission.save()
            elif content_type == "Organisation":
                item = Organisation.objects.get(id=content_id)
                new_library_permission = LibraryPermission(
                                content_type = content_type,
                                organisation = item,
                                can_be_viewed_in_library = can_be_viewed_in_library,
                                can_be_used = can_be_used,
                                author_visibility_hidden = author_visibility_hidden
                )
                new_library_permission.save()
            else:
                print("Contetn type error librayr permission")
        elif "permission_id" in request.POST:
            library_permission = LibraryPermission.objects.get(id=request.POST.get("permission_id"))
            library_permission.can_be_used = can_be_used
            library_permission.author_visibility_hidden = author_visibility_hidden
            library_permission.can_be_viewed_in_library = can_be_viewed_in_library
            library_permission.save()
            return JsonResponse({"error": False, "data":"success"})

        else:
            print("We don't know why you're here")

    return JsonResponse({"success": "success"}, safe=False)


def ajax_get_library_permissions(request):
    if request.method == "GET":
        content_type, content_id = request.GET.get("permission_data").split("_")
        if content_type == "Article":
            item = Article.objects.get(id=content_id)
        elif content_type == "Video":
            item = VideoLecture.objects.get(id=content_id)
        elif content_type == "Benchmark":
            item = Benchmark.objects.get(id=content_id)
        elif content_type == "Pathway":
            item = Pathway.objects.get(id=content_id)
        elif content_type == "StepTracker":
            item = StepTracker.objects.get(id=content_id)
        elif content_type == "Behaviour":
            item = Behaviour.objects.get(id=content_id)
        elif content_type == "Aim":
            item = Aim.objects.get(id=content_id)
        elif content_type == "Organisation":
            item = Organisation.objects.get(id=content_id)
        else:
            print("Contetn type error librayr permission")

        if item:
            if hasattr(item, 'permissions'):
                item_data = LibraryPermissionSerializer(item.permissions)
            else:
                item_data = LibraryPermissionSerializer()

            return JsonResponse(item_data.data, safe=False)


def LibraryView_ajax_get_bookmark_content(request):
    if request.method=="GET":
        bookmark = Bookmark.objects.get(id=request.GET.get("bookmark_id"))
        data = BookmarkSerializer(bookmark)
        return JsonResponse(data.data, safe=False)

def LibraryView_ajax_get_user_bookmarks(request):
    if request.method=="GET":
        bookmarks = request.user.bookmarks.all()
        data = BookmarkSerializer(bookmarks, many=True)
        return JsonResponse(data.data, safe=False)
    else:
        print(errors)


def LibraryView_ajax_use_content(request):
    print(request.POST)
    if request.method == "POST":
        content_type = request.POST.get("content_type")
        content_id = request.POST.get("content_id")
        if request.POST.get("submit_type") == "copy":
            bookmarked_object = Aim.objects.get(id=content_id)
            if isinstance(bookmarked_object, Aim):
                # get the aim to copy
                aim_to_copy = bookmarked_object

                # Check user isn't copying own content
                if aim_to_copy.author == request.user:
                    print("add errors to return here ")
                else:
                    # Find the app users aims to get an order posiition
                    user_aims = Aim.objects.filter(author=request.user)

                    # Make a coopy of the aim
                    aim_to_copy.pk = None

                    # Update the copy to the app users details, mark as a copy
                    aim_to_copy.author = request.user
                    aim_to_copy.order_position = user_aims.count()+1
                    aim_to_copy.is_a_copy = True
                    aim_to_copy.save()

                    # Locate the orginal behaviours
                    orginal_aim = Aim.objects.get(id=content_id)
                    behaviours_to_copy = orginal_aim.behaviours.all()

                    # loop through, copy and update the aims behaviours
                    for i, behaviour in enumerate(behaviours_to_copy,1):
                        behaviour_id = behaviour.id
                        behaviour.pk = None
                        behaviour.on_aim = aim_to_copy
                        behaviour.order_position = i
                        behaviour.is_a_copy = True
                        behaviour.save()
                        original_behaviour = Behaviour.objects.get(id=behaviour_id)
                        trackers_to_copy = original_behaviour.trackers.all()

                        # loop through, copy and update the behaviours trackers
                        for ii, step_tracker in enumerate(trackers_to_copy):
                            step_tracker.pk = None
                            step_tracker.on_behaviour = behaviour
                            step_tracker.is_a_copy = True
                            step_tracker.order_position = ii
                            step_tracker.save()
            else:
                print("We shouldnt be allowing copies of anything but aims yet")

        elif request.POST.get("submit_type") == "bookmark":
            if content_type == "Article":
                bookmarked_object = Article.objects.get(id=content_id)
                existing_bookmark = Bookmark.objects.filter(for_user=request.user, article=bookmarked_object)
                if existing_bookmark.exists():
                    print("duplicating bookmark error")
                else:
                    new_bookmark = Bookmark(for_user=request.user,
                                            content_type="Article",
                                            article=bookmarked_object)
                    new_bookmark.save()

            elif content_type == "VideoLecture":
                bookmarked_object = VideoLecture.objects.get(id=content_id)
                existing_bookmark = Bookmark.objects.filter(for_user=request.user, video=bookmarked_object)
                if existing_bookmark.exists():
                    print("duplicating bookmark error")
                else:
                    new_bookmark = Bookmark(for_user=request.user,
                                            content_type="VideoLecture",
                                            video=bookmarked_object)
                    new_bookmark.save()

            elif content_type == "Benchmark":
                bookmarked_object = Benchmark.objects.get(id=content_id)
                existing_bookmark = Bookmark.objects.filter(for_user=request.user, benchmark=bookmarked_object)
                if existing_bookmark.exists():
                    print("duplicating bookmark error")
                else:
                    new_bookmark = Bookmark(for_user=request.user,
                                            content_type="Benchmark",
                                            benchmark=bookmarked_object)
                    new_bookmark.save()

            elif content_type == "Pathway":
                bookmarked_object = Pathway.objects.get(id=content_id)
                existing_bookmark = Bookmark.objects.filter(for_user=request.user, pathway=bookmarked_object)
                if existing_bookmark.exists():
                    print("duplicating bookmark error")
                else:
                    new_bookmark = Bookmark(for_user=request.user,
                                            content_type="Pathway",
                                            pathway=bookmarked_object)
                    new_bookmark.save()

            elif content_type == "Organisation":
                bookmarked_object = Organisation.objects.get(id=content_id)
                existing_bookmark = Bookmark.objects.filter(for_user=request.user,organisation=bookmarked_object)
                if existing_bookmark.exists():
                    print("duplicating bookmark error")
                else:
                    new_bookmark = Bookmark(for_user=request.user,
                                            content_type="Organisation",
                                            organisation=bookmarked_object)
                    new_bookmark.save()

            elif content_type == "Aim":
                bookmarked_object = Aim.objects.get(id=content_id)
                existing_bookmark = Bookmark.objects.filter(for_user=request.user, aim=bookmarked_object)
                if existing_bookmark.exists():
                    print("duplicating bookmark error")
                else:
                    new_bookmark = Bookmark(for_user=request.user,
                                            content_type="Aim",
                                            aim=bookmarked_object)
                    new_bookmark.save()


            elif content_type == "Behaviour":
                bookmarked_object = Behaviour.objects.get(id=content_id)
                existing_bookmark = Bookmark.objects.filter(for_user=request.user, behaviour=bookmarked_object)
                if existing_bookmark.exists():
                    print("duplicating bookmark error")
                    print("for behaviour")
                    print(existing_bookmark)
                else:
                    new_bookmark = Bookmark(for_user=request.user,
                                            content_type="Behaviour",
                                            behaviour=bookmarked_object)
                    new_bookmark.save()


            elif content_type == "StepTracker":
                bookmarked_object = StepTracker.objects.get(id=content_id)
                existing_bookmark = Bookmark.objects.filter(for_user=request.user, steptracker=bookmarked_object)
                if existing_bookmark.exists():
                    print("duplicating bookmark error")
                else:
                    new_bookmark = Bookmark(for_user=request.user,
                                            content_type="StepTracker",
                                            steptracker=bookmarked_object)
                    new_bookmark.save()
            else:
                print("return an Content type error")
        elif request.POST.get("submit_type") == "delete":
            bookmark = Bookmark.objects.get(id=content_id)
            bookmark.delete()
        else:
            print("unrecognised submit type")

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
                            "StepTracker": StepTracker,
                            "Behaviour": Behaviour,
                            }
    result = get_object_or_404(content_type_converter[content_type], id=content_id)
    if isinstance(result, VideoLecture):
        content = VideoSerializer(result).data
        existing_bookmark = Bookmark.objects.filter(for_user=request.user, video=result)
        if existing_bookmark.exists():
            bookmark = BookmarkSerializer(existing_bookmark[0]).data
        else:
            bookmark = None
    elif isinstance(result, Article):
        content = ArticleSerializer(result).data
        existing_bookmark = Bookmark.objects.filter(for_user=request.user, article=result)
        if existing_bookmark.exists():
            bookmark = BookmarkSerializer(existing_bookmark[0]).data
        else:
            bookmark = None
    elif isinstance(result, Benchmark):
        content = BenchmarkSerializer(result).data
        existing_bookmark = Bookmark.objects.filter(for_user=request.user, benchmark=result)
        if existing_bookmark.exists():
            bookmark = BookmarkSerializer(existing_bookmark[0]).data
        else:
            bookmark = None
    elif isinstance(result, Pathway):
        content = PathwaySerializer(result).data
        existing_bookmark = Bookmark.objects.filter(for_user=request.user, pathway=result)
        if existing_bookmark.exists():
            bookmark = BookmarkSerializer(existing_bookmark[0]).data
        else:
            bookmark = None
    elif isinstance(result, Organisation):
        content = OrganisationSerializer(result).data
        existing_bookmark = Bookmark.objects.filter(for_user=request.user, organisation=result)
        if existing_bookmark.exists():
            bookmark = BookmarkSerializer(existing_bookmark[0]).data
        else:
            bookmark = None
    elif isinstance(result, Aim):
        content = AimLibrarySerializer(result).data
        existing_bookmark = Bookmark.objects.filter(for_user=request.user, aim=result)
        if existing_bookmark.exists():
            bookmark = BookmarkSerializer(existing_bookmark[0]).data
        else:
            bookmark = None
    elif isinstance(result, Behaviour):
        content = BehaviourSerializer(result).data
        existing_bookmark = Bookmark.objects.filter(for_user=request.user, behaviour=result)
        if existing_bookmark.exists():
            bookmark = BookmarkSerializer(existing_bookmark[0]).data
        else:
            bookmark = None
    elif isinstance(result, StepTracker):
        content = StepTrackerSerializer(result).data
        existing_bookmark = Bookmark.objects.filter(for_user=request.user, steptracker=result)
        if existing_bookmark.exists():
            bookmark = BookmarkSerializer(existing_bookmark[0]).data
        else:
            bookmark = None
    else:
        print("DATA TYPE ERROR FOR SERIALIZATION")

    data = {"content": content,
            "bookmark": bookmark }
    return JsonResponse(data, safe=False)

def LibraryView_ajax_search_library(request):
    search_phrase = request.GET.get("search_phrase")
    pathways = Pathway.objects.filter(Q(title__icontains=search_phrase)| Q(description__icontains=search_phrase)).distinct()
    videos = VideoLecture.objects.filter(Q(title__icontains=search_phrase)| Q(description__icontains=search_phrase)).distinct()
    articles = Article.objects.filter(Q(title__icontains=search_phrase)| Q(description__icontains=search_phrase)).distinct()
    benchmarks = Benchmark.objects.filter(Q(title__icontains=search_phrase)| Q(description__icontains=search_phrase)).distinct()
    organisations = Organisation.objects.filter(Q(parent_organisation=None) & (Q(title__icontains=search_phrase)| Q(description__icontains=search_phrase))).distinct()
    aims = Aim.objects.filter(Q(is_a_copy=False) & (Q(motivation__icontains=search_phrase) | Q(title__icontains=search_phrase))).distinct()
    behaviours = Behaviour.objects.filter(Q(is_a_copy=False) & Q(title__icontains=search_phrase))
    steptrackers = StepTracker.objects.filter(Q(is_a_copy=False) & (Q(metric_tracker_type__icontains=search_phrase) | Q(minimum_show_description__icontains=search_phrase) | Q(metric_unit__icontains=search_phrase) | Q(metric_action__icontains=search_phrase)) )
    data =  {
            "pathways": PathwaySerializer(pathways, many=True).data ,
            "videos": VideoSerializer(videos, many=True).data,
            "articles": ArticleSerializer(articles, many=True).data,
            "benchmarks": BenchmarkSerializer(benchmarks, many=True).data,
            "organisations": OrganisationSerializer(organisations, many=True).data,
            "aims": AimLibrarySerializer(aims, many=True).data,
            "behaviours": BehaviourSerializer(behaviours, many=True).data,
            "steptrackers": StepTrackerSerializer(steptrackers, many=True).data,
            }
    return JsonResponse(data, safe=False)

class LibraryView(View):
    template_name = "library_view.html"
    def get(self, request):
        context = {}
        return render(request, self.template_name, context)





# Create your views here.
