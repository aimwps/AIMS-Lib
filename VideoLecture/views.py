from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, View, ListView
from .forms import VideoLectureNewForm
from .models import VideoLecture
import json
import requests
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class VideoLectureView(View):
    template_name = "video_lecture.html"
    def get(self, request, vid_lec_id):
        video = get_object_or_404(VideoLecture, id=vid_lec_id)
        context = {'vid_lec':video}
        return render(request, self.template_name, context)
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
