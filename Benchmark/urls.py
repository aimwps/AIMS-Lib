from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import (
                    BenchmarkView,
                    BenchmarkCreatorView,
                    #UserBenchmarksView,
                    UserBenchmarkEditView,
                    create_qa_pair,
                    getBenchmarkData,
                    get_answer_info,
                    edit_answer,
                    get_question_info,
                    edit_question,
                    quick_add_gqb_info,
                    BenchmarkUserView,
                    getQaBankData,
                    quickAddGQB,
                    getGQB,
                    addAnswer
)

urlpatterns = [
    path('benchmark/<int:benchmark_id>', BenchmarkView.as_view(), name="benchmark"),
    path('create_benchmark/', BenchmarkCreatorView.as_view(), name="create-benchmark"),
    path('user_benchmarks/edit/<int:benchmark_id>', UserBenchmarkEditView.as_view(), name="edit-benchmark"),
    path("ajax_create_question_answer/", create_qa_pair, name="create-qa-pair"),
    path("ajax_get_benchmark_qa_data/", getBenchmarkData, name="display-benchmark-dev"),
    path("ajax_search_qa_bank/", getQaBankData, name="display-qa-bank-data"),
    path("ajax_add_gqb_to_benchmark/", quickAddGQB, name="quick-add-gqb"),
    path("ajax_get_gqb/", getGQB, name="get-gqb"),
    path("ajax_add_answer/", addAnswer, name="add-answer"),
    # path("answer-info/", csrf_exempt(get_answer_info), name="answer-info"),
    # path("answer-edit/", edit_answer, name="answer-edit"),
    # path("question-info/", csrf_exempt(get_question_info), name="question-info"),
    # path("question-edit/", edit_question, name="question-edit"),
    # path("create-gqb-question-answer/",create_qa_pair, name="quick-add-gqb"),
    # path("quick-add-gqb-info/",csrf_exempt(quick_add_gqb_info), name="quick-add-gqb-info"),
    path('developer/benchmarks/', BenchmarkUserView.as_view(), name="user-dev-benchmarks"),




]
