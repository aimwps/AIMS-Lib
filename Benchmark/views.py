from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, CreateView, View, ListView
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .models import Benchmark, Question, Answer
from WrittenLecture.models import Article
from VideoLecture.models import VideoLecture
from .forms import BenchmarkNewForm
from .benchmark_serializers import QuestionSerializer, BenchmarkSerializer, AnswerSerializer,GeneratedQuestionBankSerializer
from QuestionGenerator.views import search_questions
from QuestionGenerator.models import GeneratedQuestionBank
import json
import requests
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.mixins import LoginRequiredMixin


def getGQB(request):
    pass

def quickAddGQB(request):
    if request.method == "POST":
        gqb = get_object_or_404(GeneratedQuestionBank, id=request.POST.get("gqb_id"))
        on_benchmark = get_object_or_404(Benchmark, id=request.POST.get("benchmark_id"))
        new_question = Question(on_benchmark=on_benchmark,
                                generator_source =  gqb,
                                source_was_modified=False,
                                question_text=gqb.question,
                                order_position = len(on_benchmark.questions.all()))
        new_question.save()
        new_answer = Answer(on_question=new_question,
                            generator_source = gqb,
                            source_was_modified=False,
                            answer_text=gqb.answer,
                            is_correct=True,
                            is_default=True,
                            order_position=len(new_question.answers.all()))
        new_answer.save()
        return JsonResponse(json.dumps({"success":"success"}), safe=False)


def getQaBankData(request):
    search_phrase = request.GET.get("search_phrase")
    benchmark = get_object_or_404(Benchmark,id=request.GET.get("benchmark_id"))

    # Find all the titles containing the search phrase
    written_lecture = Article.objects.filter(title__icontains=search_phrase, author=request.user.id)
    video_lecture = VideoLecture.objects.filter(title__icontains=search_phrase, author=request.user.id)

    # Filter GQB by the content found containging the title phrase and owned by the user
    gqb = GeneratedQuestionBank.objects.filter(
            source_id__in=written_lecture, author = request.user.id) | GeneratedQuestionBank.objects.filter(
            source_id__in=written_lecture, author = request.user.id) | GeneratedQuestionBank.objects.filter(
            question__icontains=search_phrase, author = request.user.id) | GeneratedQuestionBank.objects.filter(
            answer__icontains=search_phrase, author = request.user.id)

    gqb_data = GeneratedQuestionBankSerializer(gqb, many=True)

    return JsonResponse(gqb_data.data, safe=False)



class BenchmarkUserView(LoginRequiredMixin, ListView):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    model = Benchmark
    paginate_by = 100  # if pagination is desired
    template_name = "developer_benchmarks.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    def get_queryset(self):
        return Benchmark.objects.filter(author=self.request.user).order_by('-create_date', '-create_time')



# Create your views here.
def quick_add_gqb_info(request):
    gqb_id = json.loads(request.body).get("gqb_id")
    gqb = get_object_or_404(GeneratedQuestionBank, id=gqb_id)
    gqb = GeneratedQuestionBankSerializer(gqb)
    return JsonResponse(gqb.data, safe=False)

def get_question_info(request):
    question_id = json.loads(request.body).get("question_id")
    question = get_object_or_404(Question, id=question_id)
    question = QuestionSerializer(question)
    return JsonResponse(question.data, safe=False)

def edit_question(request):
    if request.method=="POST":
        question = get_object_or_404(Question, id=request.POST.get("question_id"))
        question.answer_type = request.POST.get("answer_type")
        question.question_text = request.POST.get("question_text")
        question.save()
        response = json.dumps({"complete":True})

        return HttpResponse(response)

def get_answer_info(request):
    answer_id = json.loads(request.body).get("answer_id")
    answer = get_object_or_404(Answer, id=answer_id)
    question = Question.objects.get(answers=answer_id)
    answer = AnswerSerializer(answer)
    data = {"answer": answer.data, "question": question.question_text}
    return JsonResponse(data, safe=False)

def edit_answer(request):
    if request.method=="POST":
        answer = get_object_or_404(Answer, id=request.POST.get("answer_id"))
        answer.answer_text = request.POST.get("answer_text")
        answer_is_correct = eval(request.POST.get("is_correct").capitalize())
        answer.is_correct = answer_is_correct
        answer.save()
        response = json.dumps({"complete":True})
        return HttpResponse(response)

def getBenchmarkData(request):

    if request.method=="GET":
        benchmark_id = request.GET.get('benchmark_id')
        benchmark = get_object_or_404(Benchmark, id=benchmark_id)
        data = BenchmarkSerializer(benchmark)
        return JsonResponse(data.data, safe=False)

def create_qa_pair(request):
    print(request.POST)
    if request.method=="POST":
        question = request.POST['question']
        answer = request.POST['answer']
        if request.POST['generator_source']:
            generator_source = get_object_or_404(GeneratedQuestionBank, id=int(request.POST['generator_source']))
        else:
            generator_source = None
        has_been_modified = request.POST['source_was_modified']
        benchmark_id = get_object_or_404(Benchmark, id=int(request.POST['benchmark_id']))
        next_order_by = Question.objects.filter(on_benchmark=benchmark_id).order_by('order_position')

        for i, existing_question in enumerate(next_order_by):
            existing_question.order_position = i
            existing_question.save()

        new_question = Question(
                        on_benchmark = benchmark_id,
                        question_text = question.strip(),
                        order_position = len(next_order_by),
                        generator_source=generator_source,
                        source_was_modified=has_been_modified
        )
        new_question.save()
        get_answer_order_postion = Answer.objects.filter(on_question=new_question).order_by("order_position")
        for i, answer in enumerate(get_answer_order_postion):
            answer.order_position = i
            answer.save()

        new_answer = Answer(
                        on_question = new_question,
                        is_correct = True,
                        answer_text = answer.strip(),
                        generator_source=generator_source,
                        is_default=True,
                        order_position = len(get_answer_order_postion)
        )
        new_answer.save()
        response = json.dumps({"complete":True})

        return HttpResponse(response)

class UserBenchmarkEditView(LoginRequiredMixin,View):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    template_name = "user_benchmark_edit.html"
    def get(self, request, benchmark_id):
        abc = search_questions(request)
        context = {}
        benchmark = get_object_or_404(Benchmark, id=benchmark_id)
        gqb_json = json.dumps(list(GeneratedQuestionBank.objects.filter(author=request.user.id).values()),
                            sort_keys=True,
                            indent=1,
                            cls=DjangoJSONEncoder)
        context['benchmark'] = benchmark
        context["gqb_json"] = gqb_json
        return render(request, self.template_name, context)

class BenchmarkCreatorView(LoginRequiredMixin, CreateView):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    model = Benchmark
    form_class = BenchmarkNewForm
    template_name = "create_benchmark.html"
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse("pathways")

class BenchmarkView(View):
    template_name = "benchmark_view.html"
    def get(self, request, benchmark_id):
        context = {}
        benchmark_data = get_object_or_404(Benchmark, id=benchmark_id)
        pure_data = BenchmarkSerializer(benchmark_data).data

        print(pure_data)
        context['benchmark_data'] = pure_data
        return render(request, self.template_name, context)
