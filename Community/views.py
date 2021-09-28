from django.shortcuts import render, get_object_or_404
from django.views.generic import View,ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, FormView
from .models import Topic, Reply
from Interactions.models import VoteContent, CommentContent
from Development.models import ContentCategory
from .forms import TopicCreateForm, TopicEditForm, TopicCommentForm, ReplyCreateForm, TopicCreateInCatForm, ReplyEditForm
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

def get_category_path(cat, current_path=""):
    if cat.parent_category:
        new_path = " > "
        new_path += str(cat.title)
        new_path += current_path
        return get_category_path(cat.parent_category, current_path=new_path)

    else:
        new_path = str(cat.title)
        new_path += current_path
        return new_path


def TopicCategoryView(request, cat_id):
    category = ContentCategory.objects.get(id=cat_id)
    skill_area_topics = Topic.objects.filter(category=cat_id)
    paginator = Paginator(skill_area_topics, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'community_view_category.html', {"category": category,
                                                        "skill_area_topics": page_obj})

class CommunityHomeView(TemplateView):
    template_name = "community_home.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        skill_topic_set = {}
        for category in ContentCategory.objects.filter(global_standard=True):
            filtered_results = (get_category_path(category), list(Topic.objects.filter(category=category.id).order_by('-publish_date', '-publish_time')[:5]))
            skill_topic_set[category] = filtered_results
        x = sorted(skill_topic_set.items(), key=lambda x: x[1][0])

        context["category_topics"] = {k:v for k,v in x}
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


def TopicView(request, pk):

    topic = get_object_or_404(Topic,id=pk)#

    topic_comment_form = TopicCommentForm(request.POST or None)#
    reply_comment_form = TopicCommentForm(request.POST or None)#
    template_name = "topic_view.html"
    topic_comment_split_list = []
    reply_comment_split_list = []
    all_replies_and_comments = []
    topic_votes = []
    if request.method == "GET":
    ### FOR TOPIC COMMENTS
        topic_comments = CommentContent.objects.filter_by_instance(topic)
        topic_votes = VoteContent.objects.filter_by_instance_vote_counts(topic)
        if topic_comments:
            topic_comments_votes = []
            for comment in topic_comments:
                comment_votes = VoteContent.objects.filter_by_instance_vote_counts(comment)
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
                reply_votes = VoteContent.objects.filter_by_instance_vote_counts(topic_reply)

                reply_comments = CommentContentContent.objects.filter_by_instance(topic_reply)
                reply_comments_votes = []
                if reply_comments:
                    for comment in reply_comments:

                        comment_votes = VoteContent.objects.filter_by_instance_vote_counts(comment)
                        reply_comments_votes.append((comment, comment_votes))

                    reply_comment_split_list = create_comment_lists_by_len(reply_comments_votes, 5)
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
                new_comment = CommentContent(author=request.user, content_type=ContentType.objects.get_for_model(Topic),body=c_body, object_id=topic.id)
                new_comment.save()
                return HttpResponseRedirect(request.path)
            else:
                print("form isnt valid")
        else:

            messages.info(request, 'You must be logged in to commment')

            return HttpResponseRedirect(request.path)
#### reply
    if request.method =="POST" and 'commentforreply' in request.POST:
        if request.user:
            if reply_comment_form.is_valid():
                c_body = reply_comment_form.cleaned_data.get('content_body')
                new_comment = CommentContent(author=request.user, content_type=ContentType.objects.get_for_model(Reply),body=c_body, object_id=request.POST['object_id'])
                new_comment.save()
                return HttpResponseRedirect(request.path)
            else:
                print("form isnt valid")
        else:
            messages.info(request, 'You must be logged in to commment')
            return HttpResponseRedirect(request.path)

####################################################################################################
#### TOPIC VOTING

#### UP
    if request.method =="POST" and 'topic_vote_up' in request.POST:
        past_vote = VoteContent.objects.filter_by_instance(topic)
        if request.user:
            user_votes = past_vote.filter(votee=request.user)
            if user_votes:
                messages.info(request, 'You have already voted')
                return HttpResponseRedirect(f"{request.path}/1")
            new_vote = VoteContent(votee=request.user, content_type=ContentType.objects.get_for_model(Topic), object_id=topic.id, is_up_vote=True)
            new_vote.save()
            messages.success(request, 'Thankyou for your opinion - it might help others find what they need!')

            return HttpResponseRedirect(request.path)
        else:
            messages.info(request, 'You must be logged in to vote')
            return HttpResponseRedirect(request.path)

#### DOWN
    if request.method =="POST" and 'topic_vote_down' in request.POST:
        past_vote = VoteContent.objects.filter_by_instance(topic)
        if request.user:
            user_votes = past_vote.filter(votee=request.user)
            if user_votes:
                messages.info(request, 'You have already voted')
                return HttpResponseRedirect(request.path)
            else:
                new_vote = VoteContent(votee=request.user, content_type=ContentType.objects.get_for_model(Topic), object_id=topic.id, is_up_vote=False)
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
        comment_instance = CommentContent.objects.get(id=obj_id)
        past_vote = VoteContent.objects.filter_by_instance(comment_instance)
        if request.user:
            user_votes = past_vote.filter(votee=request.user)
            if user_votes:
                messages.info(request, 'You have already voted')
                return HttpResponseRedirect(request.path)
            else:
                new_vote = VoteContent(votee=request.user, content_type=ContentType.objects.get_for_model(CommentContent), object_id=obj_id, is_up_vote=True)
                new_vote.save()
                messages.success(request, 'Thankyou for your opinion - it might help others find what they need!')
                return HttpResponseRedirect(request.path)
        else:
            messages.info(request, 'You must be logged in to vote')
            return HttpResponseRedirect(request.path)

#### DOWN
    if request.method =="POST" and 'comment_vote_down' in request.POST:
        obj_id = request.POST["topic_comment_id_to_vote_down"]
        comment_instance = CommentContent.objects.get(id=obj_id)
        past_vote = VoteContent.objects.filter_by_instance(comment_instance)
        if request.user:
            user_votes = past_vote.filter(votee=request.user)
            if user_votes:
                messages.info(request, 'You have already voted')
                return HttpResponseRedirect(request.path)
            else:
                x =request.POST["reply_id_to_vote"]
                new_vote = VoteContent(votee=request.user, content_type=ContentType.objects.get_for_model(CommentContent), object_id=obj_id, is_up_vote=False)
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
        past_vote = VoteContent.objects.filter_by_instance(reply_instance)
        if request.user:
            user_votes = past_vote.filter(votee=request.user)
            if user_votes:
                messages.info(request, 'You have already voted')
                return HttpResponseRedirect(request.path)
            else:
                new_vote = VoteContent(votee=request.user, content_type=ContentType.objects.get_for_model(Reply), object_id=obj_id, is_up_vote=True)
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
        past_vote = VoteContent.objects.filter_by_instance(reply_instance)
        if request.user:
            user_votes = past_vote.filter(votee=request.user)
            if user_votes:
                messages.info(request, 'You have already voted')
                return HttpResponseRedirect(request.path)
            else:
                new_vote = VoteContent(votee=request.user, content_type=ContentType.objects.get_for_model(Reply), object_id=obj_id, is_up_vote=False)
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
        reply_comment_instance = CommentContent.objects.get(id=obj_id)
        past_vote = VoteContent.objects.filter_by_instance(reply_comment_instance)
        if request.user:
            user_votes = past_vote.filter(votee=request.user)
            if user_votes:
                messages.info(request, 'You have already voted')
                return HttpResponseRedirect(request.path)
            else:
                new_vote = VoteContent(votee=request.user, content_type=ContentType.objects.get_for_model(CommentContent), object_id=obj_id, is_up_vote=True)
                new_vote.save()
                messages.success(request, 'Thankyou for your opinion - it might help others find what they need!')
                return HttpResponseRedirect(request.path)
        else:
            messages.info(request, 'You must be logged in to vote')
            return HttpResponseRedirect(request.path)



#### Down
    if request.method =="POST" and 'reply_comment_vote_down' in request.POST:
        obj_id = request.POST["reply_comment_id_to_vote_down"]
        reply_comment_instance = CommentContent.objects.get(id=obj_id)
        past_vote = VoteContent.objects.filter_by_instance(reply_comment_instance)
        if request.user:
            user_votes = past_vote.filter(votee=request.user)
            if user_votes:
                messages.info(request, 'You have already voted')
                return HttpResponseRedirect(request.path)
            else:
                new_vote = VoteContent(votee=request.user, content_type=ContentType.objects.get_for_model(CommentContent), object_id=obj_id, is_up_vote=False)
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

    return render(request, template_name, context)

class ReplyEdit(LoginRequiredMixin,UpdateView):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    model = Reply
    form_class = ReplyEditForm
    template_name = "reply_edit.html"
###############################################################################################
### For viewing a topic, replying and making comments
class TopicCreate(LoginRequiredMixin,CreateView):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    model = Topic
    form_class = TopicCreateForm
    template_name = "topic_create.html"

class ReplyCreate(LoginRequiredMixin,CreateView):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    model = Reply
    form_class = ReplyCreateForm
    template_name = "reply_create.html"
    def get_success_url(self, **kwargs):
        return reverse_lazy('topic-view', args=(self.kwargs['pk'],))

    def get_context_data(self, **kwargs):
        self.reply_to = get_object_or_404(Topic, id=self.kwargs['pk'])
        kwargs['topic'] = self.reply_to
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        reply_to = get_object_or_404(Topic, id=self.kwargs['pk'])
        obj = form.save(commit=False)
        form.instance.author = self.request.user
        form.instance.on_post = reply_to
        messages.success(self.request, 'Your reply has been posted successfully')
        return super().form_valid(form)

class TopicCreateInCat(LoginRequiredMixin,CreateView):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    model = Topic
    form_class = TopicCreateInCatForm
    template_name = "topic_create_in_cat.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('community-home')

    def get_context_data(self, **kwargs):
        on_cat = ContentCategory.objects.get(id=self.kwargs['cat_id'])
        kwargs['category'] = on_cat
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.category = ContentCategory.objects.get(id=self.kwargs['cat_id'])
        form.instance.author = self.request.user
        messages.success(self.request, 'Your Topic has been posted successfully')
        return super().form_valid(form)

class TopicEdit(LoginRequiredMixin,UpdateView):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    model= Topic
    form_class = TopicEditForm
    template_name = 'topic_edit.html'

class TopicDelete(LoginRequiredMixin,DeleteView):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    model= Topic
    template_name = 'topic_delete.html'
    success_url = reverse_lazy('home')
