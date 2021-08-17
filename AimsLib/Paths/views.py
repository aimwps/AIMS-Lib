from django.shortcuts import render, get_object_or_404
from .models import Pathway, PathwayContentSetting, VideoLecture
from Members.models import MemberProfile
from django.views.generic import TemplateView, CreateView, View
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from ckeditor.fields import RichTextField


class PathsHomeView(View):
    template_name = "paths.html"
    def get(self, request):
        user_pathway_data = {}
        pathways = Pathway.objects.filter(participants=self.request.user)
        for pathway in pathways:
            content_settings = list(PathwayContentSetting.objects.filter(pathway=pathway).order_by('order_by'))
            user_pathway_data[pathway] = content_settings
            for c in  content_settings:
                print(c)
                print(c.content_type)


        context = {'user_pathways':user_pathway_data}
        return render(request, self.template_name, context)

class VideoLectureView(View):
    template_name = "video_lecture.html"
    def get(self, request, vid_lec_id):
        video = get_object_or_404(VideoLecture, id=vid_lec_id)
        print(video)
        context = {'vid_lec':video}
        return render(request, self.template_name, context)

class WrittenLectureView(View):
    template_name = "written_lecture.html"
    def get(self, request, lit_lec_id):
        context = {}
        return render(request, self.template_name, context)

class QuizView(TemplateView):
    template_name = "quiz.html"
    def get(self, request, quiz_id):
        context = {}
        return render(request, self.template_name, context)
