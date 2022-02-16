from .models import Pathway, PathwayContent, PathwayParticipant, PathwayCost, PathwayPurchase
from .forms import PathwayContentCreateForm, PathwayEditForm, PathwayCreateForm, PathwayContentEditForm, PathwayCostCreateForm
from django.views.generic import TemplateView, CreateView, View, UpdateView, DetailView, ListView
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from ckeditor.fields import RichTextField
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from Organisations.models import Organisation, OrganisationContent
from WebsiteTools.models import ContentCategory
from Benchmark.models import Benchmark, Question, Answer
from WrittenLecture.models import Article
from VideoLecture.models import VideoLecture
from QuestionGenerator.models import GeneratedQuestionBank
from Members.models import MemberProfile
import json, requests
from .pathway_serializers import PathwaySerializer, PathwayContentSerializer, PathwayCostSerializer, PathwayParticipantSerializer, SinglePathwayParticipantSerializer
from Library.models import Bookmark
from Library.library_serializers import BookmarkSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def UserPathways_ajax_submit_pathway_invite(request):

    print(request.POST)
    if request.method=="POST":
        invite = PathwayParticipant.objects.get(id=request.POST.get("invite_id"))
        invite.status = request.POST.get("status")
        invite.save()
        if invite.status =="rejected":
            if invite.purchase.purchase_type == "organisation_paid":
                invite.purchase.spent_by_user = None
                invite.purchase.spent_on_user = None
                invite.purchase.status = "active"
                invite.purchase.save()
            else:
                print("type error <-------<<")
            invite.delete()
        return JsonResponse({"success":"success"}, safe=False)

def UserPathways_ajax_check_pathway_invites(request):
    if request.method == "GET":
        data = None
        if request.user.is_authenticated:
            pathway_invites = PathwayParticipant.objects.filter(Q(status="pending", author=request.user))
            data = SinglePathwayParticipantSerializer(pathway_invites, many=True).data
        return JsonResponse(data, safe=False)


def UserPathways_ajax_get_pathway_costs(request):

    if request.method == "GET":
        pathway = get_object_or_404(Pathway, id=request.GET.get("pathway"))
        pathway_costs = PathwayCost.objects.filter(pathway=pathway)
        data = PathwayCostSerializer(pathway_costs, many=True).data
        return JsonResponse(data, safe=False)


def submit_content_delete(request):
    pathway_obj = PathwayContent.objects.get(id=request.POST.get("content_id"))
    if request.POST.get("type") == "delete":
        pathway_obj.delete()
    data_info = {"message": "Success"}
    json_data_info = json.dumps(data_info)
    return JsonResponse(json_data_info, safe=False)

def submit_content_setting_changes(request):
    data_info = {
                "result": "success",
                }

    if request.POST.get("complete_to_move_on") == 'false':
        complete_to_move_on = False
    else:
        complete_to_move_on = True
    if request.POST.get("complete_anytime_overide") == 'false':
        complete_anytime_overide = False
    else:
        complete_anytime_overide = True

    json_data_info = json.dumps(data_info)
    pathway_obj = PathwayContent.objects.get(id=request.POST.get("content_id"))
    pathway_obj.complete_anytime_overide = complete_anytime_overide
    pathway_obj.complete_to_move_on = complete_to_move_on
    pathway_obj.revise_frequency = request.POST.get("revise_frequency")
    pathway_obj.save()
    return JsonResponse(json_data_info, safe=False)

def get_pathway_content_obj(request):
    pathway_obj = PathwayContent.objects.get(id=request.GET.get("content_id"))
    data = PathwayContentSerializer(pathway_obj)
    return JsonResponse(data.data, safe=False)
# Get json of all associated content - json must be in order
# User edits
def edit_dev_pathway_content(request):
    print(request.POST)

    data_info = {
                "pathway_obj": request.POST.get("content_id"),
                }

    json_data_info = json.dumps(data_info)
    ## The pathwayContent that we are making changes too
    pathway_obj = PathwayContent.objects.get(id=request.POST.get("content_id"))

    ## All the pathwayContents from the same pathway
    all_pathway_obj = PathwayContent.objects.filter(on_pathway=pathway_obj.on_pathway).order_by("order_position")

    for i,p in enumerate(all_pathway_obj,1):
        p.order_position = i
        p.save()

    if request.POST.get("action_type") == "move-down":
        existing_position = pathway_obj.order_position
        new_position_obj = PathwayContent.objects.get(on_pathway=pathway_obj.on_pathway, order_position=existing_position+1)
        temp_position = all_pathway_obj.latest().order_position + 1
        pathway_obj.order_position = temp_position
        pathway_obj.save()
        new_position_obj.order_position = existing_position
        new_position_obj.save()
        pathway_obj.order_position = existing_position+1
        pathway_obj.save()
    elif request.POST.get("action_type") == "move-up":
        existing_position = pathway_obj.order_position
        new_position_obj = PathwayContent.objects.get(on_pathway=pathway_obj.on_pathway, order_position=existing_position-1)
        temp_position = all_pathway_obj.latest().order_position +1
        pathway_obj.order_position = temp_position
        pathway_obj.save()
        new_position_obj.order_position = existing_position
        new_position_obj.save()
        pathway_obj.order_position = existing_position-1
        pathway_obj.save()

    return JsonResponse(json_data_info, safe=False)

def get_dev_pathway_content(request):
    pathway = Pathway.objects.get(id=request.GET.get("pathway"))
    pathway_objs = PathwayContent.objects.filter(on_pathway=pathway).order_by("order_position")
    for i,p in enumerate(pathway_objs,1):
        p.order_position = i
        p.save()

    x = PathwaySerializer(pathway)
    y = PathwayContentSerializer(pathway_objs,many=True)


    data_info = {
                "pathway": x.data,
                "pathway_content": y.data,
                }

    return JsonResponse(data_info, safe=False)

class PathwayView(View):
    model = Pathway
    template_name = "pathway_view.html"

    def get(self, request, pathway_id):
        context = {}
        pathway = Pathway.objects.get(id=pathway_id)
        context['pathway'] = pathway
        if request.user.is_authenticated:
            is_participant = PathwayParticipant.objects.filter(on_pathway=pathway, author=request.user)

            if is_participant.exists():
                print("USER IS PARTIC")
                context['participation_status'] = True
                pathway_content_with_status = [
                                                (
                                                content,
                                                content.is_active(request.user),
                                                content.get_latest_result(request.user)
                                                ) for content in pathway.full_pathway.all()
                                            ]
                previous_content_is_locked = False
                corrected_pathway_content = []
                for pathway_content in pathway_content_with_status:
                    if previous_content_is_locked:
                        corrected_pathway_content.append((pathway_content[0], False, pathway_content[2]))
                    else:
                        if pathway_content[1] == False:
                            corrected_pathway_content.append(pathway_content)
                            previous_content_is_locked = True
                        else:
                            corrected_pathway_content.append(pathway_content)
                context['pathway_content'] = corrected_pathway_content

            else:
                context['participation_status'] = False
                pathway_content_with_status = [(    content,
                                                    False,
                                                    None,
                                                ) for content in pathway.full_pathway.all()]

                context['pathway_content'] = pathway_content_with_status
        else:
            context['participation_status'] = False
            pathway_content_with_status = [(    content,
                                                False,
                                                None,
                                            ) for content in pathway.full_pathway.all()]
            context['pathway_content'] = pathway_content_with_status

        # Get the pathway cost

        return render(request, self.template_name, context)

    def post(self, request, pathway_id):
        if "join_pathway" in request.POST:
            pathway = Pathway.objects.get(id=request.POST.get("join_pathway"))

            if pathway.single_user_cost == "free":
                new_purchase = PathwayPurchase(
                                    purchase_type="author_free",
                                    purchase_owner=request.user.id,
                                    pathway = pathway,
                                    spent_by_user = request.user,
                                    spent_on_user = request.user,
                                    status = "spent"
                )
                new_purchase.save()

            else:
                if pathway.author == request.user:
                    new_purchase = PathwayPurchase(
                                        purchase_type="author_free",
                                        purchase_owner=request.user.id,
                                        pathway = pathway,
                                        spent_by_user = request.user,
                                        spent_on_user = request.user,
                                        status = "spent"
                    )
                    new_purchase.save()
                else:
                    new_purchase = PathwayPurchase(
                                        purchase_type = "author_paid",
                                        purchase_owner = request.user.id,
                                        pathway = pathway,
                                        spent_by_user = request.user,
                                        spent_on_user = request.user,
                                        status = "spent"
                    )
                    new_purchase.save()

            new_participant = PathwayParticipant(
                                author = request.user,
                                on_pathway = pathway,
                                purchase = new_purchase )
            new_participant.save()




        if "leave_pathway" in request.POST:
            pathway = Pathway.objects.get(id=request.POST.get("leave_pathway"))
            participant = PathwayParticipant.objects.get(author=request.user, on_pathway=pathway)
            participant.delete()
        if "delete_pathway" in request.POST:
            pathway = Pathway.objects.get(id=request.POST.get("delete_pathway"))
            pathway.delete()
            return HttpResponseRedirect('/pathways/')
        if "delete_pathwayOBJ" in request.POST:
            pathway_content = PathwayContent.objects.get(id=int(request.POST.get("delete_pathwayOBJ")))
            pathway_content.delete()
        return HttpResponseRedirect(request.path)


class PathwayDevelopView(LoginRequiredMixin, View):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    template_name = "pathway_dev_view.html"
    form_class = PathwayContentEditForm()
    def get(self, request, pathway_id):
        context = {}
        pathway = Pathway.objects.filter(Q(id=pathway_id, author=request.user))
        print(pathway)
        if pathway.exists():
            context['pathway'] = pathway[0]
            context['form'] = self.form_class
            context['cost_form'] = PathwayCostCreateForm()
            return render(request, self.template_name, context)
        else:
            return redirect("access-denied")

    def post(self, request, pathway_id):
        if "join_pathway" in request.POST:
            pathway = Pathway.objects.get(id=request.POST.get("join_pathway"))
            new_participant = PathwayParticipant(author=request.user, on_pathway=pathway)
            new_participant.save()
        if "leave_pathway" in request.POST:
            pathway = Pathway.objects.get(id=request.POST.get("leave_pathway"))
            participant = PathwayParticipant.objects.get(author=request.user, on_pathway=pathway)
            participant.delete()
        if "delete_pathway" in request.POST:
            pathway = Pathway.objects.get(id=request.POST.get("delete_pathway"))
            pathway.delete()
            return HttpResponseRedirect('/pathways/')
        if "delete_pathwayOBJ" in request.POST:
            pathway_content = PathwayContent.objects.get(id=int(request.POST.get("delete_pathwayOBJ")))
            pathway_content.delete()
        if "add_pathway_cost" in request.POST:
            print(request.POST)
            print("....")
            pathway_cost_form = PathwayCostCreateForm(request.POST)
            if pathway_cost_form.is_valid():
                pathway_cost_form.cleaned_data
                pathway_cost_form.save()
            else:
                print(pathway_cost_form.errors)
                return JsonResponse({'error':True, "data": pathway_cost_form.errors})
        if "delete_pathway_cost" in request.POST:
            pathway_cost = PathwayCost.objects.get(id=request.POST.get("delete_pathway_cost"))
            pathway_cost.delete()
        return HttpResponseRedirect(request.path)


class PathwayContentCreate(LoginRequiredMixin, View):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    form_class = PathwayContentCreateForm
    template_name = "pathway_new_obj.html"
    def get(self, request, pathway_id):




        article_bookmarks = Bookmark.objects.filter(content_type="Article", for_user=request.user).order_by("create_date")
        article_bookmarks_paginator = Paginator(article_bookmarks, 6)
        article_bookmark_page = request.GET.get('articleBookmarkPage')

        try:
            p_article_bookmarks = article_bookmarks_paginator.page(article_bookmark_page)
        except PageNotAnInteger:
            p_article_bookmarks = article_bookmarks_paginator.page(1)
        except EmptyPage:
            p_article_bookmarks = article_bookmarks_paginator.page(article_bookmarks_paginator.num_pages)


        articles = Article.objects.filter(author=request.user)
        article_paginator = Paginator(articles, 6)
        article_page = request.GET.get('articlePage')
        try:
            p_articles = article_paginator.page(article_page)
        except PageNotAnInteger:
            p_articles = article_paginator.page(1)
        except EmptyPage:
            p_articles = article_paginator.page(article_paginator.num_pages)

        video_bookmarks = Bookmark.objects.filter(content_type="VideoLecture", for_user=request.user).order_by("create_date")
        video_bookmarks_paginator = Paginator(video_bookmarks, 6)
        video_bookmark_page = request.GET.get('videoBookmarkPage')
        try:
            p_video_bookmarks = video_bookmarks_paginator.page(video_bookmark_page)
        except PageNotAnInteger:
            p_video_bookmarks = video_bookmarks_paginator.page(1)
        except EmptyPage:
            p_video_bookmarks = video_bookmarks_paginator.page(video_bookmarks_paginator.num_pages)


        videos = VideoLecture.objects.filter(author=request.user)
        videos_paginator = Paginator(videos, 6)
        video_page = request.GET.get('videoBookmarkPage')
        try:
            p_videos = videos_paginator.page(video_page)
        except PageNotAnInteger:
            p_videos =  videos_paginator.page(1)
        except EmptyPage:
            p_videos = videos_paginator.page(videos_paginator.num_pages)


        benchmark_bookmarks = Bookmark.objects.filter(content_type="Benchmark", for_user=request.user).order_by("create_date")
        benchmark_bookmarks_paginator = Paginator(benchmark_bookmarks, 6)
        benchmark_bookmarks_page = request.GET.get('benchmarkBookmarkPage')
        try:
            p_benchmark_bookmarks = benchmark_bookmarks_paginator.page(benchmark_bookmarks_page)
        except PageNotAnInteger:
            p_benchmark_bookmarks =  benchmark_bookmarks_paginator.page(1)
        except EmptyPage:
            p_benchmark_bookmarks = benchmark_bookmarks_paginator.page(benchmark_bookmarks_paginator.num_pages)


        benchmarks = Benchmark.objects.filter(author=request.user)
        benchmarks_paginator = Paginator(benchmarks, 6)
        benchmark_page = request.GET.get('benchmarkPage')
        try:
            p_benchmarks = benchmarks_paginator.page(benchmark_page)
        except PageNotAnInteger:
            p_benchmarks =  benchmarks_paginator.page(1)
        except EmptyPage:
            p_benchmarks = benchmarks_paginator.page(benchmarks_paginator.num_pages)




        context = {
            "on_pathway": Pathway.objects.get(id=pathway_id),
            "article_bookmarks": p_article_bookmarks,
            "articles": p_articles,
            "video_bookmarks": p_video_bookmarks,
            "videos": p_videos,
            "benchmark_bookmarks": p_benchmark_bookmarks,
            "benchmarks":p_benchmarks,
            "form": PathwayContentCreateForm()}
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    def form_valid(self, form):
        print(form)
        form.instance.on_pathway = Pathway.objects.get(id=self.kwargs['pathway_id'])
        return super().form_valid(form)

    def post(self, request, pathway_id):
        print(request.POST)
        relevant_pathway = Pathway.objects.get(id=pathway_id)
        new = PathwayContentCreateForm(request.POST)
        if new.is_valid():
            new.save()
        else:
            print(new.errors)
        #
        # print(request.POST)
        # if "complete_to_move_on" in request.POST:
        #     cp = True
        # else:
        #     cp = False
        # if "complete_anytime_overide" in request.POST:
        #     rc = True
        # else:
        #     rc = False
        # if "add-content" in request.POST:
        #     new_path_obj = PathwayContent(request.POST)
        #     new_path_obj.save()


        # if "lit-submit" in request.POST:
        #     new_path_obj = PathwayContent(
        #                         on_pathway = get_object_or_404(Pathway, id=pathway_id),
        #                         content_type = "article",
        #                         video = None,
        #                         article = Article.objects.get(id=request.POST.get("article")),
        #                         benchmark = None,
        #                         order_position= new_order_position,
        #                         complete_to_move_on = cp,
        #                         complete_anytime_overide = rc)
        #     new_path_obj.save()
        #
        # elif "vid-submit" in request.POST:
        #     new_path_obj = PathwayContent(
        #                         on_pathway = get_object_or_404(Pathway, id=pathway_id),
        #                         content_type = "video",
        #                         video = VideoLecture.objects.get(id=request.POST.get("video")),
        #                         article = None,
        #                         benchmark = None,
        #                         order_position= new_order_position,
        #                         complete_to_move_on = cp,
        #                         complete_anytime_overide = rc)
        #     new_path_obj.save()
        #
        # elif "benchmark-submit" in request.POST:
        #     new_path_obj = PathwayContent(
        #                         on_pathway = get_object_or_404(Pathway, id=pathway_id),
        #                         content_type = "benchmark",
        #                         video = None,
        #                         article = None,
        #                         benchmark = Benchmark.objects.get(id=request.POST.get('benchmark')),
        #                         order_position= new_order_position,
        #                         complete_to_move_on = cp,
        #                         complete_anytime_overide = rc)
        #     new_path_obj.save()
        # else:
        #     print("FORM TYPE NOT RECOGNISED")

        return HttpResponseRedirect(reverse('pathway-develop', args=(pathway_id,)))

class PathwayEdit(LoginRequiredMixin, UpdateView):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    model= Pathway
    form_class = PathwayEditForm
    template_name = 'pathway_edit.html'
    def get_success_url(self):
        return reverse("pathway-develop", kwargs={'pathway_id' : self.object.pk})

class PathwayCreate(LoginRequiredMixin, CreateView):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    model = Pathway
    form_class = PathwayCreateForm
    template_name = "pathway_new.html"
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    def get_success_url(self):
        return reverse("pathways")

class PathsHomeView(LoginRequiredMixin, ListView):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    model = Pathway

    template_name = "pathways_dash.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):

        return Pathway.objects.filter(Q(author=self.request.user) | (~Q(author=self.request.user) & Q(participants__author=self.request.user))).distinct()

    # login_url = '/login-or-register/'
    # redirect_field_name = 'redirect_to'
    # template_name = "pathways_dash.html"#"paths.html"
    # def get(self, request):
    #
    #     context = {}
    #     user_pathway_data = {}
    #     if self.request.user.is_authenticated:
    #         if hasattr(self.request.user, 'profile'):
    #             context['user_profile'] = MemberProfile.objects.get(author=self.request.user.id)
    #             context['has_user_profile'] = True
    #         else:
    #             context['has_user_profile'] = False
    #
    #         user_pathways = PathwayParticipant.objects.filter(author=self.request.user).values_list("on_pathway", flat=True)
    #         pathways = [get_object_or_404(Pathway, id=i) for i in user_pathways]
    #         context['user_pathways'] = pathways
    #         developer_pathway_data = {}
    #         developer_pathways = Pathway.objects.filter(author=self.request.user)
    #         for dev_pathway in developer_pathways:
    #             pathway_objs = list(PathwayContent.objects.filter(on_pathway=dev_pathway).order_by('order_position'))
    #             developer_pathway_data[dev_pathway] = pathway_objs
    #         context['developer_pathways'] = developer_pathway_data
    #
    #         # user_groups = UserCreatedGroup.objects.filter(members=self.request.user.id)
    #         # context["user_groups"] = user_groups
    #         #
    #
    #     return render(request, self.template_name, context)

    def post(self, request):
        if "delete_pathway" in request.POST:
            Pathway.objects.filter(id=request.POST.get("delete_pathway")).delete()
            messages.success(request, 'the pathway was deleted successfully. BYE!')
        if "delete_pathwayOBJ" in request.POST:
            PathwayContent.objects.filter(id=request.POST.get("delete_pathwayOBJ")).delete()
            messages.success(request, 'the item was deleted successfully. BYE!')
        return HttpResponseRedirect(request.path)
