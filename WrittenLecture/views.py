from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, View, UpdateView, ListView
from .forms import WrittenLectureNewForm, WrittenLectureEditForm
from .models import WrittenLecture
import json
import requests
# Create your views here.
class WrittenLectureEdit(UpdateView):
    model= WrittenLecture
    form_class = WrittenLectureEditForm
    template_name = 'written_lecture_edit.html'
class WrittenLectureNew(CreateView):
    model = WrittenLecture
    form_class = WrittenLectureNewForm
    template_name = "written_lecture_new.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['aim_for_lever'] = Aim.objects.get(id=self.kwargs['aim_id'])
        return context
class WrittenLectureView(View):
    template_name = "written_lecture.html"
    def get(self, request, lit_lec_id):
        literature = get_object_or_404(WrittenLecture, id=lit_lec_id)
        context = {"lit_lec": literature}

        return render(request, self.template_name, context)


class WrittenLectureUserView(ListView):
    model = WrittenLecture
    paginate_by = 100  # if pagination is desired
    template_name = "developer_written_lectures.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    def get_queryset(self):
        return WrittenLecture.objects.filter(author=self.request.user)
