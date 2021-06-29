from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .forms import ForumTopicNewForm, ForumTopicEditForm
from django.urls import reverse_lazy

# Create your views here.
# def home(request):
#     return render(request, 'forum.html', {})


class ForumView(ListView):
    model = Post
    template_name = "forum.html"
    ordering = ['-id'] # orders by reverse ID

class ForumTopicView(DetailView):
    model = Post
    template_name = "forum_topic_view.html"

class ForumTopicNew(CreateView):
    model = Post
    form_class = ForumTopicNewForm
    template_name = "forum_topic_new.html"
    #fields = '__all__' # puts all the available fields in the model on the page
    #fields = ("list", "field", "names", "you", "want", "in", "form")

class ForumTopicEdit(UpdateView):
    model= Post
    form_class = ForumTopicEditForm
    template_name = 'forum_topic_edit.html'
    #fields = ('title', 'skill_area', 'body')

class ForumTopicDelete(DeleteView):
    model= Post
    template_name = 'forum_topic_delete.html'
    success_url = reverse_lazy('home')
