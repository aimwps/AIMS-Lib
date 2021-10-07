from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import (
                    BenchmarkView,
                    BenchmarkCreatorView,
                    #UserBenchmarksView,
                    UserBenchmarkEditView,
                    create_qa_pair,
                    get_benchmark_content,
                    get_answer_info,
                    edit_answer,
                    get_question_info,
                    edit_question,
                    quick_add_gqb_info,
                    BenchmarkUserView
)

urlpatterns = [
    path('benchmark/<int:benchmark_id>', BenchmarkView.as_view(), name="benchmark"),
    path('create_benchmark/', BenchmarkCreatorView.as_view(), name="create-benchmark"),
    #path('user_benchmarks/', UserBenchmarksView.as_view(), name="user-benchmarks"),
    path('user_benchmarks/edit/<int:benchmark_id>', UserBenchmarkEditView.as_view(), name="edit-benchmark"),
    path("create-question-answer/", create_qa_pair, name="create-qa-pair"),
    path("display-benchmark-dev/", csrf_exempt(get_benchmark_content), name="display-benchmark-dev"),
    path("answer-info/", csrf_exempt(get_answer_info), name="answer-info"),
    path("answer-edit/", edit_answer, name="answer-edit"),
    path("question-info/", csrf_exempt(get_question_info), name="question-info"),
    path("question-edit/", edit_question, name="question-edit"),
    path("create-gqb-question-answer/",create_qa_pair, name="quick-add-gqb"),
    path("quick-add-gqb-info/",csrf_exempt(quick_add_gqb_info), name="quick-add-gqb-info"),
    path('developer/benchmarks/', BenchmarkUserView.as_view(), name="user-dev-benchmarks"),




]
