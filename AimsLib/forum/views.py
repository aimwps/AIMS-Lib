from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Post
# Create your views here.
# def home(request):
#     return render(request, 'forum.html', {})


class ForumView(ListView):
    model = Post
    template_name = "forum.html"

class ForumTopicView(DetailView):
    model = Post
    template_name = "forum_topic_view.html"

class ForumTopicNew(CreateView):
    model = Post
    template_name = "forum_topic_add.html"
