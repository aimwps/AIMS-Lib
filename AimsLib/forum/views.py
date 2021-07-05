from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Post
from Development.models import SkillArea
from Development.models import SkillArea
from .forms import ForumTopicNewForm, ForumTopicEditForm
from django.urls import reverse_lazy
from django.core.paginator import Paginator
# Create your views here.
# def home(request):
#     return render(request, 'forum.html', {})

#ForumViewHome,ForumDevAreaTopics, ForumTopicView, ForumTopicNew, ForumTopicEdit, ForumTopicDelete

def ForumDevAreaTopics(request, dev_area_name):
    #print(SkillArea.objects.filter(skill_area_name=dev_area_name)[0])
    skill_area_pk = SkillArea.objects.filter(skill_area_name=dev_area_name)[0]
    skill_area_topics = Post.objects.filter(assigned_skill_area = skill_area_pk)
    paginator = Paginator(skill_area_topics, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'forum_view_dev_area.html', {"dev_area": dev_area_name,
                                                        "skill_area_topics": page_obj})


class ForumViewHome(TemplateView):
    template_name = "forum_home.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        skill_topic_set = []
        for skill in SkillArea.objects.all():
            filtered_results = Post.objects.filter(assigned_skill_area=skill.id).order_by('-publish_date', '-publish_time')[:5]#.order_by('-publish_time')
            if filtered_results:
                skill_topic_set.append(filtered_results)
        context['skill_area_topics'] = skill_topic_set
        return context

# class ForumDevAreaTopics(ListView):
#     model = Post
#     template_name = "forum_view_dev_area.html"

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
