from django.shortcuts import render, get_object_or_404
from django.views.generic import View,ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, FormView
from .models import Post, Comment, Reply, VoteUpDown
from Development.models import SkillArea
from .forms import ForumTopicNewForm, ForumTopicEditForm, ForumTopicCommentForm
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
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
    topic_comment_form = ForumTopicCommentForm(request.POST or None)#
    reply_comment_form = ForumTopicCommentForm(request.POST or None)#
    template_name = "forum_topic_view.html"
    pagi_comments = []
    all_replies_and_comments =[]
    if request.method == "GET":
    ### FOR TOPIC COMMENTS
        topic_comments = Comment.objects.filter_by_instance(topic)
        topic_votes = VoteUpDown.objects.filter_by_instance_vote_counts(topic)
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

    ### FOR TOPIC REPLIES
        #### Check is there are replies
        all_replies_and_comments =[]
        topic_replies = Reply.objects.filter(on_post=pk)
        if topic_replies:

        ### Loop through the replies
            for topic_reply in topic_replies:

            #### Find any comments replated to an individual reply
                reply_comments = Comment.objects.filter_by_instance(topic_reply)
                if reply_comments:
                    comment_replies_list = []
                    comment_replies_list_builder = []
                    for comment in reply_comments:
                        if len(comment_replies_list_builder) >= 5:
                            comment_replies_list.append(comment_replies_list_builder)
                            comment_replies_list_builder = []
                        comment_replies_list_builder.append( comment)
                    comment_replies_list.append(comment_replies_list_builder)

            ### Save a single reply and all its comments as a tuple to a list of every reply and comment
                    all_replies_and_comments.append((topic_reply, comment_replies_list))
                else:
                    all_replies_and_comments.append((topic_reply,))





    if request.method =="POST" and 'commentfortopic' in request.POST:
        if topic_comment_form.is_valid():
            print(topic_comment_form.cleaned_data)
            c_body = topic_comment_form.cleaned_data.get('content_body')
            new_comment = Comment(author=request.user, content_type=ContentType.objects.get_for_model(Post),body=c_body, object_id=topic.id)
            new_comment.save()
            return HttpResponseRedirect(request.path)


    if request.method =="POST" and 'commentforreply' in request.POST:
        if reply_comment_form.is_valid():
            print(reply_comment_form.cleaned_data)
            c_body = reply_comment_form.cleaned_data.get('content_body')
            new_comment = Comment(author=request.user, content_type=ContentType.objects.get_for_model(Reply),body=c_body, object_id=request.POST['object_id'])
            new_comment.save()
            return HttpResponseRedirect(request.path)




    if request.method =="POST" and 'topic_vote_up' in request.POST:
        past_vote = VoteUpDown.objects.filter_by_instance(topic)
        user_votes = past_vote.filter(votee=request.user)
        if user_votes:
            print("Already voted")
            return HttpResponseRedirect(request.path)
        new_vote = VoteUpDown(votee=request.user, content_type=ContentType.objects.get_for_model(Post), object_id=topic.id, is_up_vote=True)
        new_vote.save()
        return HttpResponseRedirect(request.path)

    if request.method =="POST" and 'topic_vote_down' in request.POST:
        past_vote = VoteUpDown.objects.filter_by_instance(topic)
        user_votes = past_vote.filter(votee=request.user)
        if user_votes:
            print("Already voted")
            return HttpResponseRedirect(request.path)
        else:
            new_vote = VoteUpDown(votee=request.user, content_type=ContentType.objects.get_for_model(Post), object_id=topic.id, is_up_vote=False)
            new_vote.save()
            return HttpResponseRedirect(request.path)

    context = {
                "topic": topic,
                "pagi_comments": pagi_comments[:min(len(pagi_comments),6)],
                "topic_comment_form": topic_comment_form,
                "topic_replies": all_replies_and_comments,
                "reply_comment_form": reply_comment_form,
                "topic_votes": topic_votes,
                }
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
