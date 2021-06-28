from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post
# Create your views here.
# def home(request):
#     return render(request, 'forum.html', {})


class ForumView(ListView):
    model = Post
    template_name = "forum.html"

class ForumTopicView(DetailView):
    model = Post
    template_name = "forum_topic.html"
