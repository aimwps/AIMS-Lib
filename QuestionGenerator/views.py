from django.shortcuts import render, get_object_or_404, redirect
from .models import GeneratedQuestionBank
from WrittenLecture.models import WrittenLecture
from VideoLecture.models import VideoLecture
from Benchmark.models import Quiz, QuizQuestion, QuizAnswer
from .sserializers import GeneratedQuestionBankSerializer
from django.views.generic import CreateView, View, TemplateView
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
import requests
from .tasks import textpreperation_qag, getqag

# Create your views here.
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
        benchmark_qs = QuizQuestion.objects.filter(on_quiz=json.loads(request.body).get('on_benchmark'))

        new_data = []
        for q in gqb:
            new_data.append(
            {"question":GeneratedQuestionBankSerializer(q).data,
            "benchmark_status":benchmark_qs.filter(generated_from=q.id).exists()})
        print(new_data)
        return JsonResponse(new_data, safe=False)

class QuestionGeneratorView(View):
    template_name="question_generator.html"
    def get(self, request, source_type, source_id):
        if source_type == 'literature':
            source_doc = get_object_or_404(WrittenLecture, id=source_id).body
        elif source_type == 'transcript':
            source_doc = get_object_or_404(VideoLecture, id=source_id).transcript
        else:
            print("big errors")
            source_doc = ""
        clean_text = textpreperation_qag(source_doc, source_type)
        getqag.delay(clean_text, source_type, source_id, request.user.id)
        return redirect('generator-pending',source_type=source_type, source_id=source_id)



    # def post(self, request,source_type, source_id):
    #     if "proofed_questions" in request.POST:
    #         for i in range(int(request.POST.get('proofed_questions'))):
    #             if f'proof_{i}' in request.POST:
    #                 user_proof = request.POST.get(f'proof_{i}')
    #             else:
    #                 user_proof = "unknown"
    #             new_question = request.POST.get(f"q_{i}")
    #             new_answer = request.POST.get(f"a_{i}")
    #             existing_gqb = list(GeneratedQuestionBank.objects.filter(question=new_question, answer=new_answer))
    #             if len(existing_gqb) > 0:
    #                 already_exists = True
    #             else:
    #                 already_exists = False
    #             if not already_exists:
    #                 gen_question = GeneratedQuestionBank(
    #                         generated_by = self.request.user,
    #                         source_type = source_type,
    #                         source_id = source_id,
    #                         question = new_question,
    #                         answer = new_answer,
    #                         user_proof = user_proof
    #                         )
    #                 gen_question.save()
    #             else:
    #                 print("duplicate found! not saving")
    #
    #     return HttpResponseRedirect('/create_benchmark/#begin')


class QuestionGeneratorProof(View):
    pass

class QuestionGeneratorPending(View):
    template_name = "generator_pending.html"
    def get(self, request, source_type, source_id):
        context = {}
        context['source_type'] = source_type
        context['source_id'] = source_id
        return render(request, self.template_name, context)
