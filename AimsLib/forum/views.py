from django.shortcuts import render, get_object_or_404
from django.views.generic import View,ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, FormView
from .models import Post, Comment, Reply
from Development.models import SkillArea
from .forms import ForumTopicNewForm, ForumTopicEditForm, ForumTopicCommentForm
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
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
    #form_class = ForumTopicNewComment
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        skill_topic_set = []
        for skill in SkillArea.objects.all():
            filtered_results = Post.objects.filter(assigned_skill_area=skill.id).order_by('-publish_date', '-publish_time')[:5]#.order_by('-publish_time')
            if filtered_results:
                skill_topic_set.append(filtered_results)
        context['skill_area_topics'] = skill_topic_set
        return context

###############################################################################################
### For viewing a topic, replying and making comments

def ForumTopicView(request, pk):
    topic = get_object_or_404(Post,id=pk)#
    comment_form = ForumTopicCommentForm(request.POST or None)#
    template_name = "forum_topic_view.html"

    if request.method == "GET":
        topic_comments = Comment.objects.filter(on_post=pk)
        topic_replies = Reply.objects.filter(on_post=pk)
        # For splitting comments into groups of 3 allowing them to be
        # displayed in seperate tabs.
        pagi_comments = []
        pagi_builder = []
        for comment in topic_comments:
            if len(pagi_builder) >= 5:
                pagi_comments.append(pagi_builder)
                pagi_builder = []
            pagi_builder.append( comment)
        pagi_comments.append(pagi_builder)

    if request.method =="POST":
        if comment_form.is_valid():
            print(comment_form.cleaned_data)
            c_body = comment_form.cleaned_data.get('content_body')
            new_comment = Comment(author = request.user, on_post=topic, body=c_body)
            new_comment.save()
            return HttpResponseRedirect(request.path)
    context = {
                "topic": topic,
                "pagi_comments": pagi_comments[:min(len(pagi_comments),6)],
                "comment_form": comment_form,
                "topic_replies": topic_replies}


    return render(request, template_name, context)









# class ForumTopicView(View):
#     template_name = "forum_topic_view.html"
#     topic = Post.objects.filter(id=self.kwargs['pk'])
#     topic_comments = Comment.objects.filter(on_post=self.kwargs['pk'])
#
#     ### Get Topic
#     if len(topic) > 0:
#         context['topic'] = topic
#
#     ### Get Comments
#     if len(topic_comments) >0:
#         pagi_comments = []
#         pagi_builder = []
#
#         for comment in topic_comments:
#             if len(pagi_builder) >= 3:
#                 pagi_comments.append(pagi_builder)
#                 pagi_builder = []
#             pagi_builder.append( comment)
#         if len(pagi_builder) > 0:
#             pagi_comments.append(pagi_builder)
#         if len(pagi_comments) > 0:
#             context['pagi_comments'] = pagi_comments
#
#     ### Get Replies & their comments
#
#     def get(self, request, *args, **kwargs):
#         return render(request, template, context)
#
#     # def get_context_data(self, **kwargs):
#     #     context = super().get_context_data(**kwargs)
#     #     topic = Post.objects.filter(id=self.kwargs['pk'])
#     #     topic_comments = Comment.objects.filter(on_post=self.kwargs['pk'])# put order by here for most gvoted in future
#     #     pagi_comments = []
#     #     pagi_builder = []
#     #     for comment in topic_comments:
#     #         if len(pagi_builder) >= 3:
#     #             pagi_comments.append(pagi_builder)
#     #             pagi_builder = []
#     #         pagi_builder.append( comment)
#     #     if len(pagi_builder) > 0:
#     #         pagi_comments.append(pagi_builder)
#     #     if len(pagi_comments) > 0:
#     #         context['pagi_comments'] = pagi_comments
#     #     context['form'] = ForumTopicNewComment
#     #     context['post'] = topic
#     #     return context
#
#     def post(self, request):
#         pass

# class ForumDevAreaTopics(ListView):
#     model = Post
#     template_name = "forum_view_dev_area.html"

# class ForumTopicView(DetailView):
#     model = Post
#     template_name = "forum_topic_view.html"
#     def get_context_data(self, **kwargs):
#         context = super(ForumTopicView, self).get_context_data(**kwargs)
#         page = self.request.GET.get('page')
#         topic_comments = self.object.comments.all() # put order by here for most gvoted in future
#         pagi_comments = []
#         pagi_builder = []
#         for comment in topic_comments:
#             if len(pagi_builder) >= 3:
#                 pagi_comments.append(pagi_builder)
#                 pagi_builder = []
#             pagi_builder.append( comment)
#         if len(pagi_builder) > 0:
#             pagi_comments.append(pagi_builder)
#         context['pagi_comments'] = pagi_comments
#
#         return context


###############################################################################################
### For viewing a topic, replying and making comments
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
