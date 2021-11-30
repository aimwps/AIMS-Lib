from .models import Pathway, PathwayContent, PathwayParticipant
from .forms import PathwayContentCreateForm, PathwayEditForm, PathwayCreateForm
from django.views.generic import TemplateView, CreateView, View, UpdateView, DetailView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404
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

class PathwayView(View):
    model = Pathway
    template_name = "pathway_view.html"

    def get(self, request, pathway_id):
        context = {}
        pathway = Pathway.objects.get(id=pathway_id)
        is_participant = PathwayParticipant.objects.filter(on_pathway=pathway, author=request.user)
        if is_participant:
            context['participation_status'] = True
        else:
            context['participation_status'] = False
        context['pathway'] = pathway
        return render(request, self.template_name, context)

    def post(self, request, pathway_id):
        print(request.POST)
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
        return HttpResponseRedirect(request.path)


class PathwayDevelopView(LoginRequiredMixin, View):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    template_name = "pathway_dev_view.html"

    def get(self, request, pathway_id):
        context = {}
        pathway = Pathway.objects.get(id=pathway_id)
        is_participant = PathwayParticipant.objects.filter(on_pathway=pathway, author=request.user)
        if is_participant:
            context['participation_status'] = True
        else:
            context['participation_status'] = False
        context['pathway'] = pathway
        return render(request, self.template_name, context)

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
        return HttpResponseRedirect(request.path)

class PathwayContentCreate(LoginRequiredMixin, View):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    form_class = PathwayContentCreateForm
    template_name = "pathway_new_obj.html"
    def get(self, request, pathway_id):
        context = {
        "on_pathway": Pathway.objects.get(id=pathway_id),
        "form": PathwayContentCreateForm()}
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    def form_valid(self, form):
        form.instance.on_pathway = Pathway.objects.get(id=self.kwargs['pathway_id'])
        return super().form_valid(form)

    def post(self, request, pathway_id):
        relevant_pathway = PathwayContent.objects.filter(on_pathway=pathway_id)
        if relevant_pathway:
            new_order_position=  relevant_pathway.latest().order_position+ 1
        else:
            new_order_position= 1
        print(request.POST)
        if "complete_previous" in request.POST:
            cp = True
        else:
            cp = False
        if "revise_continuous" in request.POST:
            rc = True
        else:
            rc = False

        if "lit-submit" in request.POST:
            new_path_obj = PathwayContent(
                                on_pathway = get_object_or_404(Pathway, id=pathway_id),
                                content_type = "written-lecture",
                                video = None,
                                article = Article.objects.get(id=request.POST.get("article")),
                                benchmark = None,
                                order_position= new_order_position,
                                complete_previous = cp,
                                revise_continuous = rc)
            new_path_obj.save()

        elif "vid-submit" in request.POST:
            new_path_obj = PathwayContent(
                                on_pathway = get_object_or_404(Pathway, id=pathway_id),
                                content_type = "video-lecture",
                                video = VideoLecture.objects.get(id=request.POST.get("video")),
                                article = None,
                                benchmark = None,
                                order_position= new_order_position,
                                complete_previous = cp,
                                revise_continuous = rc)
            new_path_obj.save()

        elif "benchmark-submit" in request.POST:
            new_path_obj = PathwayContent(
                                on_pathway = get_object_or_404(Pathway, id=pathway_id),
                                content_type = "benchmark",
                                video = None,
                                article = None,
                                benchmark = Benchmark.objects.get(id=request.POST.get('benchmark')),
                                order_position= new_order_position,
                                complete_previous = cp,
                                revise_continuous = rc)
            new_path_obj.save()
        else:
            print("FORM TYPE NOT RECOGNISED")

        return HttpResponseRedirect(f'/pathways/')

class PathwayEdit(LoginRequiredMixin, UpdateView):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    model= Pathway
    form_class = PathwayEditForm
    template_name = 'pathway_edit.html'

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
        return reverse("pathway-content-create", kwargs={'pathway_id' : self.object.pk})

class PathsHomeView(LoginRequiredMixin, View):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    template_name = "paths.html"
    def get(self, request):

        context = {}
        user_pathway_data = {}
        if self.request.user.is_authenticated:
            if hasattr(self.request.user, 'profile'):
                context['user_profile'] = MemberProfile.objects.get(author=self.request.user.id)
                context['has_user_profile'] = True
            else:
                context['has_user_profile'] = False

            user_pathways = PathwayParticipant.objects.filter(author=self.request.user).values_list("on_pathway", flat=True)
            pathways = [get_object_or_404(Pathway, id=i) for i in user_pathways]
            context['user_pathways'] = pathways
            developer_pathway_data = {}
            developer_pathways = Pathway.objects.filter(author=self.request.user)
            for dev_pathway in developer_pathways:
                pathway_objs = list(PathwayContent.objects.filter(on_pathway=dev_pathway).order_by('order_position'))
                developer_pathway_data[dev_pathway] = pathway_objs
            context['developer_pathways'] = developer_pathway_data

            # user_groups = UserCreatedGroup.objects.filter(members=self.request.user.id)
            # context["user_groups"] = user_groups
            #

        return render(request, self.template_name, context)

    def post(self, request):
        if "delete_pathway" in request.POST:
            Pathway.objects.filter(id=request.POST.get("delete_pathway")).delete()
            messages.success(request, 'the pathway was deleted successfully. BYE!')
        if "delete_pathwayOBJ" in request.POST:
            PathwayContent.objects.filter(id=request.POST.get("delete_pathwayOBJ")).delete()
            messages.success(request, 'the item was deleted successfully. BYE!')
        return HttpResponseRedirect(request.path)
