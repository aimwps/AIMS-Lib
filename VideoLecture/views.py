from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, View, ListView, UpdateView
from .forms import VideoLectureNewForm, VideoLectureEditForm, VideoLectureSessionForm
from .models import VideoLecture, VideoLectureSession
from Paths.models import Pathway
import json
import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

# Create your views here.
class VideoLectureView(View):
    template_name = "video_lecture.html"
    def get(self, request, vid_lec_id):
        video = get_object_or_404(VideoLecture, id=vid_lec_id)
        participation_status = False


        if request.user.is_authenticated:
            video_user_pathways = Pathway.objects.filter(Q(full_pathway__video=video) & Q(participants__author=request.user))
            if video_user_pathways.exists():
                for pathway in video_user_pathways:
                    for content in pathway.full_pathway.all():
                        if content.is_active:
                            participation_status = True
            if video.author == request.user:
                participation_status = True

        part_of_pathways = Pathway.objects.filter(Q(full_pathway__video=video)).distinct()

        context = { "participation_status": participation_status,
                    'vid_lec':video,
                    "form": VideoLectureSessionForm(),
                    "part_of_pathways":part_of_pathways }
        return render(request, self.template_name, context)

    def post(self, request, vid_lec_id):

        video = VideoLecture.objects.get(id=vid_lec_id)
        pathway = Pathway.objects.filter((Q(full_pathway__video=video)
        & Q(participants__author=request.user)))
        print(request.POST)
        if request.method =="POST":
            new_video_session  = VideoLectureSession(
                                            for_user= request.user,
                                            on_video = video,
                                            status = request.POST.get("status"),
                                            completion_time = request.POST.get("completion_time"))
            new_video_session.save()

            return redirect('pathway-view', pathway_id=pathway[0].id)

class VideoLectureNew(LoginRequiredMixin, CreateView):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    model = VideoLecture
    form_class = VideoLectureNewForm
    template_name = "video_lecture_new.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['aim_for_lever'] = Aim.objects.get(id=self.kwargs['aim_id'])
        return context
class VideoLectureUserView(LoginRequiredMixin, ListView):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    model = VideoLecture
    paginate_by = 100  # if pagination is desired
    template_name = "developer_video_lectures.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    def get_queryset(self):
        return VideoLecture.objects.filter(author=self.request.user)

class VideoLectureEdit(LoginRequiredMixin, UpdateView):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    model = VideoLecture
    form_class = VideoLectureEditForm
    paginate_by = 100  # if pagination is desired
    template_name = "video_lecture_edit.html"
