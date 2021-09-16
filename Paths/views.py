from .models import Pathway, PathwayContentSetting, PathwayContentSetting
from Benchmark.models import Quiz, QuizQuestion, QuizAnswer
from QuestionGenerator.models import GeneratedQuestionBank
from .forms import PathwayObjNewForm, PathwayEditForm, PathwayNewForm
from Members.models import MemberProfile
from django.views.generic import TemplateView, CreateView, View, UpdateView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from ckeditor.fields import RichTextField
from django.contrib import messages
from NLP.question_generation.pipelines import pipeline
import json
import requests




class PathwayView(View):
    template_name = "pathway_view.html"

    def get(self, request, pathway_id):
        context = {}
        pathway = Pathway.objects.get(id=pathway_id)
        pathway_objs = PathwayContentSetting.objects.filter(pathway=pathway).order_by("order_by")
        if request.user in pathway.participants.all():
            context['participation_status'] = True
        else:
            context['participation_status'] = False
        context['pathway'] = {pathway:pathway_objs}
        return render(request, self.template_name, context)

    def post(self, request, pathway_id):
        print(request.POST)
        if "join_pathway" in request.POST:
            pathway = Pathway.objects.get(id=request.POST.get("join_pathway"))
            pathway.participants.add(request.user)
            pathway.save()

        if "leave_pathway" in request.POST:
            pathway = Pathway.objects.get(id=request.POST.get("leave_pathway"))
            pathway.participants.remove(request.user)
            pathway.save()
        if "delete_pathway" in request.POST:
            pathway = Pathway.objects.get(id=request.POST.get("delete_pathway"))
        next = request.POST.get('next','/')
        return HttpResponseRedirect(next)

class PathwayObjNew(View):
    form_class = PathwayObjNewForm
    template_name = "pathway_new_obj.html"
    def get(self, request, pathway_id):
        context = {
        "on_pathway": Pathway.objects.get(id=pathway_id),
        "form": PathwayObjNewForm(user=request.user)}
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    def form_valid(self, form):
        form.instance.pathway = Pathway.objects.get(id=self.kwargs['pathway_id'])
        return super().form_valid(form)

    def post(self, request, pathway_id):
        relevant_pathway = PathwayContentSetting.objects.filter(pathway=pathway_id)
        if relevant_pathway:
            new_order_by =  relevant_pathway.latest().order_by + 1
        else:
            new_order_by = 1

        new_path_obj_form = PathwayObjNewForm(request.user, request.POST)
        if new_path_obj_form.is_valid():
            if "lit-submit" in request.POST:
                new_path_obj = PathwayContentSetting(
                                    pathway = get_object_or_404(Pathway, id=pathway_id),
                                    content_type = "written-lecture",
                                    video_lecture = None,
                                    written_lecture = new_path_obj_form.cleaned_data['written_lecture'],
                                    quiz = None,
                                    order_by = new_order_by ,
                                    must_complete_previous = new_path_obj_form.cleaned_data['must_complete_previous'],
                                    must_revise_continous = new_path_obj_form.cleaned_data['must_revise_continous'])
                new_path_obj.save()

            elif "vid-submit" in request.POST:
                new_path_obj = PathwayContentSetting(
                                    pathway = get_object_or_404(Pathway, id=pathway_id),
                                    content_type = "video-lecture",
                                    video_lecture = new_path_obj_form.cleaned_data['video_lecture'],
                                    written_lecture = None,
                                    quiz = None,
                                    order_by = new_order_by ,
                                    must_complete_previous = new_path_obj_form.cleaned_data['must_complete_previous'],
                                    must_revise_continous = new_path_obj_form.cleaned_data['must_revise_continous'])
                new_path_obj.save()

            elif "quiz-submit" in request.POST:
                new_path_obj = PathwayContentSetting(
                                    pathway = get_object_or_404(Pathway, id=pathway_id),
                                    content_type = "benchmark",
                                    video_lecture = None,
                                    written_lecture = None,
                                    quiz = new_path_obj_form.cleaned_data['quiz'],
                                    order_by = new_order_by,
                                    must_complete_previous = new_path_obj_form.cleaned_data['must_complete_previous'],
                                    must_revise_continous = new_path_obj_form.cleaned_data['must_revise_continous'])
                new_path_obj.save()
            else:
                print("FORM TYPE NOT RECOGNISED")

        return HttpResponseRedirect('/pathway/')

class EditPathwayView(UpdateView):
    model= Pathway
    form_class = PathwayEditForm
    template_name = 'pathway_edit.html'

class PathwayNew(CreateView):
    model = Pathway
    form_class = PathwayNewForm
    template_name = "pathway_new.html"
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class PathsHomeView(View):
    template_name = "paths.html"
    def get(self, request):
        context = {}
        user_pathway_data = {}
        if self.request.user.is_authenticated:
            if hasattr(self.request.user, 'profile'):
                context['user_profile'] = MemberProfile.objects.get(user_profile=self.request.user.id)
                context['has_user_profile'] = True
            else:
                context['has_user_profile'] = False
            user_pathways = Pathway.objects.filter(participants=self.request.user)
            for pathway in user_pathways:
                content_settings = list(PathwayContentSetting.objects.filter(pathway=pathway).order_by('order_by'))
                user_pathway_data[pathway] = content_settings
            context['user_pathways'] = user_pathway_data
            developer_pathway_data = {}
            developer_pathways = Pathway.objects.filter(author=self.request.user)
            for dev_pathway in developer_pathways:
                pathway_objs = list(PathwayContentSetting.objects.filter(pathway=dev_pathway).order_by('order_by'))
                developer_pathway_data[dev_pathway] = pathway_objs
            context['developer_pathways'] = developer_pathway_data
        return render(request, self.template_name, context)

    def post(self, request):
        if "delete_pathway" in request.POST:
            Pathway.objects.filter(id=request.POST.get("delete_pathway")).delete()
            messages.success(request, 'the pathway was deleted successfully. BYE!')
        if "delete_pathwayOBJ" in request.POST:
            PathwayContentSetting.objects.filter(id=request.POST.get("delete_pathwayOBJ")).delete()
            messages.success(request, 'the item was deleted successfully. BYE!')
        return HttpResponseRedirect(request.path)
