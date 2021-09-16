from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, View
from .forms import VideoLectureNewForm
from .models import VideoLecture
import json
import requests
# Create your views here.
class VideoLectureView(View):
    template_name = "video_lecture.html"
    def get(self, request, vid_lec_id):
        video = get_object_or_404(VideoLecture, id=vid_lec_id)
        context = {'vid_lec':video}
        return render(request, self.template_name, context)
class VideoLectureNew(CreateView):
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
