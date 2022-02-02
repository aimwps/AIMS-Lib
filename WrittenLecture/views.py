from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, View, UpdateView, ListView
from .forms import ArticleCreateForm, ArticleEditForm, ArticleSessionForm
from .models import Article, ArticleSession
from Paths.models import Pathway
import json
import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

# Create your views here.
class ArticleEdit(LoginRequiredMixin, UpdateView):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    model = Article
    form_class = ArticleEditForm
    template_name = 'written_lecture_edit.html'

class ArticleCreate(LoginRequiredMixin, CreateView):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    model = Article
    form_class = ArticleCreateForm
    template_name = "written_lecture_new.html"
    success_url = reverse_lazy("user-articles")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ArticleView(View):
    template_name = "written_lecture.html"
    def get(self, request, lit_lec_id):
        literature = get_object_or_404(Article, id=lit_lec_id)
        participation_status = False


        if request.user.is_authenticated:
            article_user_pathways = Pathway.objects.filter((Q(full_pathway__article=literature) & Q(participants__author=request.user)))
            print(f"COUNT OF QUERY {article_user_pathways.count()}")
            for a in article_user_pathways:
                print(a)
                print(a.participants.all())
            if article_user_pathways.exists():
                for pathway in article_user_pathways:
                    print(pathway, pathway.title)
                    for content in pathway.full_pathway.all():

                        # The user is a member and the content is available to them
                        if content.is_active(request.user):
                            print("participation_status is True because they are a member and the content is is_active")
                            participation_status = True
                    print("\nend of content check\n")

            # The user is the author, overides allowing them to see content
            if literature.author == request.user:
                print("participation_status is True because they are the author")
                participation_status = True

        part_of_pathways = Pathway.objects.filter(Q(full_pathway__article=literature)).distinct()

        context = { "participation_status": participation_status,
                    "lit_lec": literature,
                    "form":ArticleSessionForm(),
                    "part_of_pathways": part_of_pathways}
        print(context)
        return render(request, self.template_name, context)

    def post(self, request, lit_lec_id):
        article = Article.objects.get(id=lit_lec_id)
        pathway = Pathway.objects.filter((Q(full_pathway__article=article)
        & Q(participants__author=request.user)))
        if request.method =="POST":
            new_article_session  = ArticleSession(
                                            for_user= request.user,
                                            on_article = article,
                                            status = request.POST.get("status"),
                                            completion_time = request.POST.get("completion_time"))
            new_article_session.save()

            return redirect('pathway-view', pathway_id=pathway[0].id)

    def form_valid(self, form):
        form.instance.for_user = self.request.user
        form.instance.on_article = self.request.lit_lec.id
        return super().form_valid(form)


class UserArticlesView(LoginRequiredMixin, ListView):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    model = Article
    paginate_by = 100  # if pagination is desired
    template_name = "developer_written_lectures.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    def get_queryset(self):
        return Article.objects.filter(author=self.request.user)
