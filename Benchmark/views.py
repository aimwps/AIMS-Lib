from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, CreateView, View, ListView
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Benchmark, Question, Answer, BenchmarkSession, BenchmarkSessionQuestion
from WrittenLecture.models import Article
from VideoLecture.models import VideoLecture
from .forms import BenchmarkForm, BenchmarkNewForm, BenchmarkAnswerForm, BenchmarkEditQuestionForm, BenchmarkEditAnswerForm
from .benchmark_serializers import QuestionSerializer, BenchmarkSerializer, AnswerSerializer,GeneratedQuestionBankSerializer, BenchmarkSessionSerializer, BenchmarkSessionQuestionSerializer
from QuestionGenerator.views import search_questions
from QuestionGenerator.models import GeneratedQuestionBank
import json
import requests
import random
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime

def BenchmarkView_ajax_get_session_status(request):
    if request.method == "GET":
        benchmark = get_object_or_404(Benchmark, id=request.GET.get("benchmark_id"))
        session_history = BenchmarkSession.objects.filter(Q(for_user=request.user), Q(completed=True))
        session_history_data = BenchmarkSessionSerializer(session_history, many=True).data

        sessions = BenchmarkSession.objects.filter(Q(for_user=request.user), Q(on_benchmark= benchmark), Q(completed=False))

        if sessions:
            data = {
                "uncomplete_session": sessions[0].id,
                "complete_session": session_history_data
                }
        else:
            data = {
                "uncomplete_session": None,
                "complete_session": session_history_data
                }
        return JsonResponse(data, safe=False)


def BenchmarkView_ajax_submit_answer(request):
    print(request.POST)
    if request.method =="POST":
        session_question = get_object_or_404(BenchmarkSessionQuestion, id=request.POST.get("session_question_id"))
        question_status = request.POST.get("question_status")
        if question_status == "skipped":
            session_question.question_status = "b_skipped"
            session_question.remaining_time_to_answer = request.POST.get("remaining_time")
        elif question_status == "abandoned":
            session_question.question_status = "d_abandoned"
            session_question.answered_correctly = False
        elif question_status == "complete":
            session_question.question_status = "c_complete"
            possible_answers = session_question.question.answers.all()
            default_answer = session_question.question.answers.filter(is_default=True)

            if default_answer:
                default_answer = default_answer[0]
            else:
                next_default = session_question.question.answers.filter(is_correct=True)
                if next_default:
                    default_answer = next_default[0]
                else:
                    print("errors")

            if session_question.question.answer_type == "text-entry-exact":
                session_question.given_answer = request.POST.get("text_entry_value")

                for possible_answer in possible_answers:
                    if possible_answer.answer_text == session_question.given_answer:
                        print("This ones correct")
                        session_question.answered_correctly = True
                    else:
                        print("You got this one wrong")
                        print(possible_answer.answer_text, session_question.given_answer)
                        session_question.answered_correctly = False


            elif session_question.question.answer_type == "text-entry-nearest":
                session_question.given_answer = request.POST.get("text_entry_value")

                for possible_answer in possible_answers:

                    if possible_answer.answer_text.strip().lower() == session_question.given_answer.strip().lower():
                        print("This ones correct")
                        session_question.answered_correctly = True
                        # print(f"proposed_answer: {possible_answer.answer_text.strip().lower()}, selected_value: {session_question.given_answer.strip().lower()}")
                    else:
                        print("You got this one wrong")
                        # print(session_question.given_answer)
                        session_question.answered_correctly = False


            elif session_question.question.answer_type == "multiple-choice":
                mcv =   request.POST.getlist('multiple_choice_value[]')
                print(f"DFA: {default_answer.id } |||| MCV {mcv[0]}")
                if default_answer.id == int(mcv[0]):
                    session_question.answered_correctly = True
                    print("This ones correct")

                else:
                    session_question.answered_correctly = False
                    print("You got this one wrong")


            elif session_question.question.answer_type == "multiple-correct-choice":
                answer_ids = request.POST.getlist("multiple_correct_choice_values[]")
                correct_answers = session_question.question.answers.filter(is_correct=True)
                all_correct = True
                for answer_id in answer_ids:
                    if int(answer_id) not in list(correct_answers.values_list("id", flat=True)):
                        all_correct = False
                session_question.answered_correctly = all_correct

                if all_correct:
                    print("This ones correct")

                else:
                    session_question.answered_correctly = False
                    print("You got this one wrong")

            else:
                print("question type error")
        else:
            session_question.remaining_time_to_answer = request.POST.get("remaining_time")
        session_question.save()
        data = {"session_id": session_question.benchmark_session.id}
        return JsonResponse(data, safe=False)

def BenchmarkView_ajax_get_session_question(request):
    if request.method =="GET":
        benchmark_session = get_object_or_404(BenchmarkSession, id=request.GET.get("session_id"))
        next_question_set = benchmark_session.session_questions.filter(
                                                                    Q(answered_correctly=None),
                                                                    ).order_by("question_status","id")

        if next_question_set.count() > 0:
            data = {
                    "data":BenchmarkSessionQuestionSerializer(next_question_set[0]).data,
                    "question_num": min(benchmark_session.on_benchmark.questions.count(), benchmark_session.on_benchmark.max_num_questions) - next_question_set.count()+1,
                    "completion_status": False
                    }
            return JsonResponse(data, safe=False)

        else:
            benchmark_session.completed = True
            benchmark_session.completion_date = datetime.now()
            benchmark_session.completion_time = datetime.now()
            benchmark_session.save()
            data = {"completion_status": True }
            return JsonResponse(data, safe=False)

def BenchmarkView_ajax_get_new_session(request):
    benchmark = get_object_or_404(Benchmark, id=request.GET.get("benchmark_id"))
    new_session = BenchmarkSession(
                                    for_user = request.user,
                                    on_benchmark = benchmark,
                                    completion_type = "submission",
                                    completed = False,
                                    )
    new_session.save()
    total_available_questions = len(benchmark.questions.all())

    # Shorten the length of available questions to the total in benchmark, randomize or select
    # the first x amount based on benchmark settings
    if benchmark.max_num_questions < total_available_questions:
        if benchmark.randomize_questions:
            random_sample = random.sample(range(0, total_available_questions), benchmark.max_num_questions)
            question_set = [benchmark.questions.all()[i] for i in random_sample]
        else:
            question_set = benchmark.questions.all().order_by("order_position")[:benchmark.max_num_questions]
    else:
        question_set = benchmark.questions.all()

    #Add question set to new session

    for question in question_set:
        new_session_question = BenchmarkSessionQuestion(
                                benchmark_session = new_session,
                                question=question,
                                answered_correctly=None,
                                given_answer= None,
                                )
        new_session_question.save()


    data = {"session_id": new_session.id}

    return JsonResponse(data, safe=False)





def submitCrudBenchmark(request):

    if request.method =="POST":
        benchmark = get_object_or_404(Benchmark, id=request.POST.get("benchmark_id"))
        crud_type = request.POST.get("crud_type")
        if crud_type == "update":
            benchmark.title =  request.POST.get("title")
            benchmark.description = request.POST.get("description")
            if request.POST.get("max_num_questions"):
                benchmark.max_num_questions = request.POST.get("max_num_questions")
            if request.POST.get("randomize_questions"):
                benchmark.randomize_questions =  request.POST.get("randomize_questions")
            if request.POST.get("default_answer_seconds"):
                benchmark.default_answer_seconds = request.POST.get("default_answer_seconds")
            if request.POST.get("override_time_with_default"):
                benchmark.override_time_with_default = request.POST.get("override_time_with_default")
            benchmark.save()
            forward = f"/user_benchmarks/edit/{benchmark.id}"


        elif crud_type == "delete":
            forward = f"benchmarks/"
            benchmark.delete()
            return redirect("user-benchmarks")
        else:
            print("crud type error")

        return JsonResponse(json.dumps({"success":"success"}), safe=False)

def getBenchmarkSettings(request):
    if request.method =="GET":
        benchmark = get_object_or_404(Benchmark, id=request.GET.get("benchmark_id"))
        data = BenchmarkSerializer(benchmark)
        return JsonResponse(data.data, safe=False)

def getAnswerData(request):
    if request.method =="GET":
        answer = get_object_or_404(Answer, id=request.GET.get("answer_id"))
        data = AnswerSerializer(answer)
        return JsonResponse(data.data, safe=False)

def submitAnswer(request):

    response_messages = {
                        "success" : [],
                        "failure" : [],
                        }
    if request.method == "POST":
        crud_type = request.POST.get("crud_type")

        # Process form data and create a new answer
        if crud_type == "create":

            # Find the question we are creating an aswer for
            question = get_object_or_404(Question, id=request.POST.get("on_question"))


            if request.POST.get("generator_source") == "":
                generator_source = None
            else:
                generator_source = get_object_or_404(GeneratedQuestionBank, id=request.POST.get("generator_source"))

            if request.POST.get("source_was_modified") == "":
                source_was_modified = False
            else:
                source_was_modified = True

            if request.POST.get("is_default"):
                all_answers = question.answers.all()
                for answer in all_answers:
                    answer.is_default = False
                    answer.save()

            new_answer = Answer(
                            on_question = question,
                            generator_source = generator_source,
                            source_was_modified = source_was_modified,
                            answer_text = request.POST.get("answer_text"),
                            is_correct = request.POST.get("is_correct"),
                            is_default = request.POST.get("is_default"),
                            order_position = len(question.answers.all()),
                            )
            new_answer.save()

        # Else we are addding a new answer
        elif crud_type == "update":
            edit_answer = get_object_or_404(Answer, id=request.POST.get("answer_id"))

            if request.POST.get("is_default"):
                all_answers = edit_answer.on_question.answers.all()
                for answer in all_answers:
                    answer.is_default = False
                    answer.save()

            edit_answer.answer_text = request.POST.get("answer_text")
            edit_answer.is_correct = request.POST.get("is_correct")
            edit_answer.is_default = request.POST.get("is_default")
            edit_answer.save()

        elif crud_type == "delete":
            answer = get_object_or_404(Answer, id=request.POST.get("answer_id"))
            answer.delete()

        else:
            print("crud type error")
        return JsonResponse(json.dumps({"success":"success"}), safe=False)

def submitQuestionEdit(request):

    if request.method =="POST":
        question = get_object_or_404(Question, id=request.POST.get("question_id"))

        #Check if updating order position is necessary
        requested_order_position = int(request.POST.get("order_position"))

        if question.order_position != requested_order_position:
            all_questions = question.on_benchmark.questions.all().order_by("order_position")
            for i,q in enumerate(all_questions):
                q.order_position = i
                q.save()
            #Check the requested position is viable
            if requested_order_position in range(0, len(all_questions)):

                # reverse through questions adding 1 to there positon allowing place for new position.
                for i in range(len(all_questions)-1, requested_order_position-1,-1) :
                    all_questions[i].order_position += 1
                    all_questions[i].save()

                # Update the question to its new order position
                question.order_position = requested_order_position
                question.save()

                # re-order all questions to close empty positions
                all_questions = question.on_benchmark.questions.all().order_by("order_position")
                for i, q in enumerate(all_questions):
                    q.order_position = i
                    q.save()
            else:
                print("tHIS IS WHWERE A FORM ERROR SHOULD BE GENERATED")

        else:
            print("we came here")

        # Check is updating text is necessary
        edited_text = request.POST.get("question_text")
        if question.question_text != edited_text:
            if len(edited_text) > 0:
                question.question_text = edited_text
                question.save()
            else:
                print("THIS IS A FORM ERROR")

        # Check if question type change is necessary
        answer_type = request.POST.get("answer_type")
        if question.answer_type != answer_type:
            question.answer_type = answer_type
            question.save()

    data = json.dumps({"success": "success"})
    return JsonResponse(data, safe=False)

def getQuestionData(request):
    if request.method == "GET":
        question = get_object_or_404(Question, id=request.GET.get("question_id"))
        data = QuestionSerializer(question)

        return JsonResponse(data.data, safe=False)

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

class UserBenchmarksView(LoginRequiredMixin, ListView):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    model = Benchmark
    paginate_by = 100  # if pagination is desired
    template_name = "user_benchmarks_view.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    def get_queryset(self):
        return Benchmark.objects.filter(author=self.request.user).order_by('-create_date', '-create_time')

def getBenchmarkData(request):
    if request.method=="GET":
        benchmark_id = request.GET.get('benchmark_id')
        benchmark = get_object_or_404(Benchmark, id=benchmark_id)
        data = BenchmarkSerializer(benchmark)
        return JsonResponse(data.data, safe=False)

def benchmarkCreateQApair(request):
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

class BenchmarkEditView(LoginRequiredMixin,View):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    template_name = "benchmark_edit.html"
    def get(self, request, benchmark_id):
        context = {}
        benchmark = get_object_or_404(Benchmark, id=benchmark_id)
        context['benchmark'] = benchmark
        context['benchmark_form'] = BenchmarkForm()
        context["answer_form"] = BenchmarkAnswerForm()
        context["edit_question_form"] = BenchmarkEditQuestionForm()
        return render(request, self.template_name, context)

class BenchmarkCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    model = Benchmark
    form_class = BenchmarkForm
    template_name = "create_benchmark.html"
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse("user-benchmarks")

class BenchmarkView(View):
    template_name = "benchmark_view.html"
    def get(self, request, benchmark_id):
        context = {}
        benchmark = get_object_or_404(Benchmark, id=benchmark_id)
        context["benchmark"] = benchmark
        return render(request, self.template_name, context)

def BenchmarkView_ajax_get_benchmark_data(request):
    if request.method == "GET":
        benchmark_id = request.GET.get("benchmark_id")
        benchmark = get_object_or_404(Benchmark, id=benchmark_id)
        bencmark_data = BenchmarkSerializer(benchmark)
        user_sessions = BenchmarkSessions.objects.filter(for_user=request.user, on_benchmark=benchmark)

        uncomplete_sessions = user_sessions.objects.filter(completed=False)

        if uncomplete_sessions:
            context["uncomplete_session_id"] = uncomplete_sessions[0].id
        context["benchmark"] = benchmark_data.data


        return JsonResponse(context, safe=False)
