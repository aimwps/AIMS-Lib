from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, CreateView, View
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Quiz, QuizQuestion, QuizAnswer
from .forms import BenchmarkNewForm
from .benchmark_serializers import QuizQuestionSerializer, QuizSerializer, QuizAnswerSerializer,GeneratedQuestionBankSerializer
from QuestionGenerator.views import search_questions
from QuestionGenerator.models import GeneratedQuestionBank
import json
import requests
from django.core.serializers.json import DjangoJSONEncoder
# Create your views here.
def quick_add_gqb_info(request):
    gqb_id = json.loads(request.body).get("gqb_id")
    gqb = get_object_or_404(GeneratedQuestionBank, id=gqb_id)
    gqb = GeneratedQuestionBankSerializer(gqb)
    return JsonResponse(gqb.data, safe=False)
def get_question_info(request):
    question_id = json.loads(request.body).get("question_id")
    question = get_object_or_404(QuizQuestion, id=question_id)
    question = QuizQuestionSerializer(question)
    return JsonResponse(question.data, safe=False)
def edit_question(request):
    if request.method=="POST":
        question = get_object_or_404(QuizQuestion, id=request.POST.get("question_id"))
        question.answer_type = request.POST.get("answer_type")
        question.question_text = request.POST.get("question_text")
        question.save()
        response = json.dumps({"complete":True})

        return HttpResponse(response)
def get_answer_info(request):
    answer_id = json.loads(request.body).get("answer_id")
    answer = get_object_or_404(QuizAnswer, id=answer_id)
    question = QuizQuestion.objects.get(answers=answer_id)
    answer = QuizAnswerSerializer(answer)
    data = {"answer": answer.data, "question": question.question_text}
    return JsonResponse(data, safe=False)
def edit_answer(request):
    if request.method=="POST":
        print(request.POST)
        answer = get_object_or_404(QuizAnswer, id=request.POST.get("answer_id"))
        answer.answer_text = request.POST.get("answer_text")
        answer_is_correct = eval(request.POST.get("is_correct").capitalize())
        answer.is_correct = answer_is_correct
        answer.save()
        response = json.dumps({"complete":True})
        return HttpResponse(response)
def get_benchmark_content(request):
    print(request.POST)
    if request.method=="POST":
        benchmark_id = json.loads(request.body).get('benchmark_id')
        questions = QuizQuestion.objects.filter(on_quiz=benchmark_id).order_by("order_by")
        q = QuizSerializer(data=questions, many=True)
        qas = QuizQuestionSerializer(questions, many=True)
        return JsonResponse(qas.data, safe=False)
    else:
        print("Oh fuck")
def create_qa_pair(request):
    print(request.POST)
    if request.method=="POST":
        question = request.POST['question']
        answer = request.POST['answer']
        if request.POST['generated_from']:
            generated_from = get_object_or_404(GeneratedQuestionBank, id=int(request.POST['generated_from']))
        else:
            generated_from = None
        has_been_modified = request.POST['has_been_modified']
        benchmark_id = get_object_or_404(Quiz, id=int(request.POST['benchmark_id']))
        next_order_by = QuizQuestion.objects.filter(on_quiz=benchmark_id).order_by('order_by')

        for i, existing_question in enumerate(next_order_by):
            existing_question.in_order = i
            existing_question.save()

        new_question = QuizQuestion(
                        on_quiz = benchmark_id,
                        question_text = question.strip(),
                        order_by = len(next_order_by),
                        generated_from=generated_from,
                        has_been_modified=has_been_modified
        )
        new_question.save()

        new_answer = QuizAnswer(
                        to_question = new_question,
                        is_correct = True,
                        answer_text = answer.strip(),
                        generated_from=generated_from,
        )
        new_answer.save()
        response = json.dumps({"complete":True})

        return HttpResponse(response)

class UserBenchmarkEditView(View):
    template_name = "user_benchmark_edit.html"
    def get(self, request, benchmark_id):
        abc = search_questions(request)
        context = {}
        benchmark = get_object_or_404(Quiz, id=benchmark_id)
        gqb_json = json.dumps(list(GeneratedQuestionBank.objects.filter(generated_by=request.user.id).values()),
                            sort_keys=True,
                            indent=1,
                            cls=DjangoJSONEncoder)
        context['benchmark'] = benchmark
        context["gqb_json"] = gqb_json
        return render(request, self.template_name, context)
class UserBenchmarksView(View):
    template_name = "user_benchmarks.html"
    def get(self, request):

        context = {}
        user_benchmarks = Quiz.objects.filter(author=request.user.id).order_by('-publish_date', '-publish_time')
        print(user_benchmarks)
        context['user_benchmarks'] = user_benchmarks
        return render(request, self.template_name, context)
class BenchmarkCreatorView(CreateView):
    model = Quiz
    form_class = BenchmarkNewForm
    template_name = "create_benchmark.html"
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
class QuizView(TemplateView):
    template_name = "quiz.html"
    def get(self, request, quiz_id):
        context = {}
        return render(request, self.template_name, context)
