from django.shortcuts import render, get_object_or_404
from django.views.generic import View,ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, FormView
from .models import Post, Comment, Reply, VoteUpDown
from Development.models import SkillArea
from .forms import ForumTopicNewForm, ForumTopicEditForm, ForumTopicCommentForm
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
# Create your views here.
# def home(request):
#     return render(request, 'forum.html', {})

#ForumViewHome,ForumDevAreaTopics, ForumTopicView, ForumTopicNew, ForumTopicEdit, ForumTopicDelete





def ForumDevAreaTopics(request, dev_area_name):

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

def create_comment_lists_by_len(qs, l_len):

    pagi_comments = []
    pagi_builder = []
    for comment in qs:
        if len(pagi_builder) >= l_len:
            pagi_comments.append(pagi_builder)
            pagi_builder = []
        pagi_builder.append(comment)
    pagi_comments.append(pagi_builder)

    return pagi_comments


def ForumTopicView(request, pk):
    topic = get_object_or_404(Post,id=pk)#
    topic_comment_form = ForumTopicCommentForm(request.POST or None)#
    reply_comment_form = ForumTopicCommentForm(request.POST or None)#
    template_name = "forum_topic_view.html"
    topic_comment_split_list = []
    reply_comment_split_list = []
    all_replies_and_comments = []
    topic_votes = []
    if request.method == "GET":
    ### FOR TOPIC COMMENTS
        topic_comments = Comment.objects.filter_by_instance(topic)
        topic_votes = VoteUpDown.objects.filter_by_instance_vote_counts(topic)
        if topic_comments:
            topic_comments_votes = []
            for comment in topic_comments:
                comment_votes = VoteUpDown.objects.filter_by_instance_vote_counts(comment)
                topic_comments_votes.append((comment, comment_votes))
            topic_comment_split_list = create_comment_lists_by_len(topic_comments_votes, 5)

    ### FOR TOPIC REPLIES
        #### Check is there are replies
        topic_replies = Reply.objects.filter(on_post=pk)
        if topic_replies:
        ### Loop through the replies
            for topic_reply in topic_replies:
####################################################################################################
#### GETS REPLIES, THERE COMMENTS, AND THE COMMENTS VOTE COUNTS
            #### Find any comments replated to an individual reply
                reply_votes = VoteUpDown.objects.filter_by_instance_vote_counts(topic_reply)

                reply_comments = Comment.objects.filter_by_instance(topic_reply)
                reply_comments_votes = []
                if reply_comments:
                    for comment in reply_comments:

                        comment_votes = VoteUpDown.objects.filter_by_instance_vote_counts(comment)
                        reply_comments_votes.append((comment, comment_votes))

                    reply_comment_split_list = create_comment_lists_by_len(reply_comments_votes, 5)
                    print(reply_comment_split_list)
                    for i in reply_comment_split_list:
                        print(i)
                        print("reply over ___")

            ### Save a single reply and all its comments as a tuple to a list of every reply and comment
                    all_replies_and_comments.append(((topic_reply, reply_votes),reply_comment_split_list))

                else:
                    all_replies_and_comments.append((
                                                    (topic_reply,reply_votes),
                                                    ))

####################################################################################################
#### COMMENT POSTING

#### topic
    if request.method =="POST" and 'commentfortopic' in request.POST:
        if request.user:
            if topic_comment_form.is_valid():

                c_body = topic_comment_form.cleaned_data.get('content_body')
                new_comment = Comment(author=request.user, content_type=ContentType.objects.get_for_model(Post),body=c_body, object_id=topic.id)
                new_comment.save()
                return HttpResponseRedirect(request.path)
        else:
            messages.info(request, 'You must be logged in to commment')
            return HttpResponseRedirect(request.path)
#### reply
    if request.method =="POST" and 'commentforreply' in request.POST:
        if request.user:
            if reply_comment_form.is_valid():
                c_body = reply_comment_form.cleaned_data.get('content_body')
                new_comment = Comment(author=request.user, content_type=ContentType.objects.get_for_model(Reply),body=c_body, object_id=request.POST['object_id'])
                new_comment.save()
                print(new_comment)
                return HttpResponseRedirect(request.path)
        else:
            messages.info(request, 'You must be logged in to commment')
            return HttpResponseRedirect(request.path)

####################################################################################################
#### TOPIC VOTING

#### UP
    if request.method =="POST" and 'topic_vote_up' in request.POST:
        past_vote = VoteUpDown.objects.filter_by_instance(topic)
        if request.user:
            user_votes = past_vote.filter(votee=request.user)
            if user_votes:
                messages.info(request, 'You have already voted')
                return HttpResponseRedirect(request.path)
            new_vote = VoteUpDown(votee=request.user, content_type=ContentType.objects.get_for_model(Post), object_id=topic.id, is_up_vote=True)
            new_vote.save()
            messages.success(request, 'Thankyou for your opinion - it might help others find what they need!')
            return HttpResponseRedirect(request.path)
        else:
            messages.info(request, 'You must be logged in to vote')
            return HttpResponseRedirect(request.path)

#### DOWN
    if request.method =="POST" and 'topic_vote_down' in request.POST:
        past_vote = VoteUpDown.objects.filter_by_instance(topic)
        if request.user:
            user_votes = past_vote.filter(votee=request.user)
            if user_votes:
                messages.info(request, 'You have already voted')
                return HttpResponseRedirect(request.path)
            else:
                new_vote = VoteUpDown(votee=request.user, content_type=ContentType.objects.get_for_model(Post), object_id=topic.id, is_up_vote=False)
                new_vote.save()
                messages.success(request, 'Thankyou for your opinion - it might help others find what they need!')
                return HttpResponseRedirect(request.path)
        else:
            messages.info(request, 'You must be logged in to vote')
            return HttpResponseRedirect(request.path)


####################################################################################################
#### Comment voting

#### UP
    if request.method =="POST" and 'comment_vote_up' in request.POST:
        obj_id = request.POST["topic_comment_id_to_vote_up"]
        comment_instance = Comment.objects.get(id=obj_id)
        past_vote = VoteUpDown.objects.filter_by_instance(comment_instance)
        if request.user:
            user_votes = past_vote.filter(votee=request.user)
            if user_votes:
                messages.info(request, 'You have already voted')
                return HttpResponseRedirect(request.path)
            else:
                new_vote = VoteUpDown(votee=request.user, content_type=ContentType.objects.get_for_model(Comment), object_id=obj_id, is_up_vote=True)
                new_vote.save()
                messages.success(request, 'Thankyou for your opinion - it might help others find what they need!')
                return HttpResponseRedirect(request.path)
        else:
            messages.info(request, 'You must be logged in to vote')
            return HttpResponseRedirect(request.path)

#### DOWN
    if request.method =="POST" and 'comment_vote_down' in request.POST:
        obj_id = request.POST["topic_comment_id_to_vote_down"]
        comment_instance = Comment.objects.get(id=obj_id)
        past_vote = VoteUpDown.objects.filter_by_instance(comment_instance)
        if request.user:
            user_votes = past_vote.filter(votee=request.user)
            if user_votes:
                messages.info(request, 'You have already voted')
                return HttpResponseRedirect(request.path)
            else:
                x =request.POST["reply_id_to_vote"]
                new_vote = VoteUpDown(votee=request.user, content_type=ContentType.objects.get_for_model(Comment), object_id=obj_id, is_up_vote=False)
                new_vote.save()
                messages.success(request, 'Thankyou for your opinion - it might help others find what they need!')
                return HttpResponseRedirect(request.path)
        else:
            messages.info(request, 'You must be logged in to vote')
            return HttpResponseRedirect(request.path)




####################################################################################################
#### Reply voting

#### UP
    if request.method =="POST" and "reply_vote_up" in request.POST:
        obj_id = request.POST["reply_id_to_vote_up"]
        reply_instance = Reply.objects.get(id=obj_id)
        past_vote = VoteUpDown.objects.filter_by_instance(reply_instance)
        if request.user:
            user_votes = past_vote.filter(votee=request.user)
            if user_votes:
                messages.info(request, 'You have already voted')
                return HttpResponseRedirect(request.path)
            else:
                new_vote = VoteUpDown(votee=request.user, content_type=ContentType.objects.get_for_model(Reply), object_id=obj_id, is_up_vote=True)
                new_vote.save()
                messages.success(request, 'Thankyou for your opinion - it might help others find what they need!')
                return HttpResponseRedirect(request.path)
        else:
            messages.info(request, 'You must be logged in to vote')
            return HttpResponseRedirect(request.path)



#### Down
    if request.method =="POST" and 'reply_vote_down' in request.POST:
        obj_id = request.POST["reply_id_to_vote_down"]
        reply_instance = Reply.objects.get(id=obj_id)
        past_vote = VoteUpDown.objects.filter_by_instance(reply_instance)
        if request.user:
            user_votes = past_vote.filter(votee=request.user)
            if user_votes:
                messages.info(request, 'You have already voted')
                return HttpResponseRedirect(request.path)
            else:
                new_vote = VoteUpDown(votee=request.user, content_type=ContentType.objects.get_for_model(Reply), object_id=obj_id, is_up_vote=False)
                new_vote.save()
                messages.success(request, 'Thankyou for your opinion - it might help others find what they need!')
                return HttpResponseRedirect(request.path)
        else:
            messages.info(request, 'You must be logged in to vote')
            return HttpResponseRedirect(request.path)
####################################################################################################

####################################################################################################
#### Reply comment voting

#### UP
    if request.method =="POST" and "reply_comment_vote_up" in request.POST:
        obj_id = request.POST["reply_comment_id_to_vote_up"]
        reply_comment_instance = Comment.objects.get(id=obj_id)
        past_vote = VoteUpDown.objects.filter_by_instance(reply_comment_instance)
        if request.user:
            user_votes = past_vote.filter(votee=request.user)
            if user_votes:
                messages.info(request, 'You have already voted')
                return HttpResponseRedirect(request.path)
            else:
                new_vote = VoteUpDown(votee=request.user, content_type=ContentType.objects.get_for_model(Comment), object_id=obj_id, is_up_vote=True)
                new_vote.save()
                messages.success(request, 'Thankyou for your opinion - it might help others find what they need!')
                return HttpResponseRedirect(request.path)
        else:
            messages.info(request, 'You must be logged in to vote')
            return HttpResponseRedirect(request.path)



#### Down
    if request.method =="POST" and 'reply_comment_vote_down' in request.POST:
        obj_id = request.POST["reply_comment_id_to_vote_down"]
        reply_comment_instance = Comment.objects.get(id=obj_id)
        past_vote = VoteUpDown.objects.filter_by_instance(reply_comment_instance)
        if request.user:
            user_votes = past_vote.filter(votee=request.user)
            if user_votes:
                messages.info(request, 'You have already voted')
                return HttpResponseRedirect(request.path)
            else:
                new_vote = VoteUpDown(votee=request.user, content_type=ContentType.objects.get_for_model(Comment), object_id=obj_id, is_up_vote=False)
                new_vote.save()
                messages.success(request, 'Thankyou for your opinion - it might help others find what they need!')
                return HttpResponseRedirect(request.path)
        else:
            messages.info(request, 'You must be logged in to vote')
            return HttpResponseRedirect(request.path)
####################################################################################################


    context = {
                "topic": topic,
                "pagi_comments": topic_comment_split_list[:min(len(topic_comment_split_list), 6)],
                "topic_comment_form": topic_comment_form,
                "topic_replies": all_replies_and_comments,
                "reply_comment_form": reply_comment_form,
                "topic_votes": topic_votes,
                }


        # for comment_list in reply[1]:
        #     print("\n")
        #     print(comment_list)
        #     for comment in comment_list:
        #         print("\n")
        #         print(comment)
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
