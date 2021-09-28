from django.shortcuts import render, get_object_or_404, redirect
from .models import GeneratedQuestionBank
from WrittenLecture.models import Article
from VideoLecture.models import VideoLecture
from Benchmark.models import Benchmark, Question, Answer
from .sserializers import GeneratedQuestionBankSerializer
from django.views.generic import CreateView, View, TemplateView
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
import requests
from .tasks import textpreperation_qag, getqag
from django.db.models import Q

from django.contrib.auth.mixins import LoginRequiredMixin

def submit_status_change(request):
    if request.method=="POST":
        gqb = get_object_or_404(GeneratedQuestionBank, id=request.POST.get('submit_id'))
        gqb.user_proof = request.POST.get('submit_status')
        gqb.save()
        return JsonResponse({"Success":"success"})
class VerifyGqbView(LoginRequiredMixin, View):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    template_name = "verify_gqb.html"
    def get(self, request):
        context = {}
        return render(request, self.template_name, context)

def get_gqb_to_verify(request):
    if request.method=="GET":
        outstanding_gqb = GeneratedQuestionBank.objects.filter(generated_by=request.user.id, user_proof="unknown")
        gqb_serialized = GeneratedQuestionBankSerializer(outstanding_gqb, many=True)
        return JsonResponse(gqb_serialized.data, safe=False)

def check_gqb_status(request):
    if request.method=="GET":
        outstanding_gqb = GeneratedQuestionBank.objects.filter(generated_by=request.user.id, user_proof="unknown")
        data = {"gqb_quantity": len(outstanding_gqb)}
    return JsonResponse(data, safe=False)

def search_questions(request):
    if request.method=="POST":
        search_str = json.loads(request.body).get('searchText')
        written_lecture = WrittenLecture.objects.filter(title__icontains=search_str, author=request.user.id)
        video_lecture = VideoLecture.objects.filter(title__icontains=search_str, author=request.user.id)
        gqb = GeneratedQuestionBank.objects.filter(
                source_id__in=written_lecture, generated_by = request.user.id) | GeneratedQuestionBank.objects.filter(
                source_id__in=written_lecture, generated_by = request.user.id) | GeneratedQuestionBank.objects.filter(
                question__icontains=search_str, generated_by = request.user.id)| GeneratedQuestionBank.objects.filter(
                answer__icontains=search_str, generated_by = request.user.id)
        benchmark_qs = Question.objects.filter(on_quiz=json.loads(request.body).get('on_benchmark'))

        new_data = []
        for q in gqb:
            new_data.append(
            {"question":GeneratedQuestionBankSerializer(q).data,
            "benchmark_status":benchmark_qs.filter(generated_from=q.id).exists()})

        return JsonResponse(new_data, safe=False)

class QuestionGenerator(LoginRequiredMixin, View):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    def get(self, request, source_type, source_id):
        if source_type == 'literature':
            source_doc = get_object_or_404(WrittenLecture, id=source_id).body
        elif source_type == 'transcript':
            source_doc = get_object_or_404(VideoLecture, id=source_id).transcript
        else:
            print("big errors")
            source_doc = ""
        clean_text = textpreperation_qag(source_doc, source_type)
        for passage in clean_text:
            getqag.delay(passage, source_type, source_id, request.user.id)
        return redirect('generator-pending',source_type=source_type, source_id=source_id)




class QuestionGeneratorPending(View):
    template_name = "generator_pending.html"
    def get(self, request, source_type, source_id):
        context = {}
        context['source_type'] = source_type
        context['source_id'] = source_id
        if source_type == "literature":
            object = get_object_or_404(WrittenLecture, id=source_id)
        else:
            object = get_object_or_404(VideoLecture, id=source_id)
        context['source_object'] = object
        return render(request, self.template_name, context)
