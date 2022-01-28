from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import (
                    UserBenchmarksView,
                    BenchmarkCreateView,
                    BenchmarkEditView,
                    BenchmarkView,
                    BenchmarkView_ajax_get_new_session,
                    BenchmarkView_ajax_get_session_question,
                    BenchmarkView_ajax_submit_answer,
                    BenchmarkView_ajax_get_session_status,
                    benchmarkCreateQApair,
                    getBenchmarkData,
                    getQaBankData,
                    quickAddGQB,
                    submitAnswer,
                    getQuestionData,
                    submitQuestionEdit,
                    getAnswerData,
                    getBenchmarkSettings,
                    submitCrudBenchmark
)

urlpatterns = [
    path('benchmark/<int:benchmark_id>', BenchmarkView.as_view(), name="benchmark"),
    path("BenchmarkView_ajax_get_new_session/", BenchmarkView_ajax_get_new_session, name="gbmd"),
    path("BenchmarkView_ajax_get_session_question/", BenchmarkView_ajax_get_session_question,name="get-session-question"),
    path("BenchmarkView_ajax_submit_answer/", BenchmarkView_ajax_submit_answer, name="post-session-answer"),
    path("BenchmarkView_ajax_get_session_status/", BenchmarkView_ajax_get_session_status, name="get-session-status"),
    path('create_benchmark/', BenchmarkCreateView.as_view(), name="create-benchmark"),
    path('user_benchmarks/edit/<int:benchmark_id>', BenchmarkEditView.as_view(), name="edit-benchmark"),
    path("ajax_create_question_answer/", benchmarkCreateQApair, name="create-qa-pair"),
    path("ajax_get_benchmark_qa_data/", getBenchmarkData, name="display-benchmark-dev"),
    path("ajax_search_qa_bank/", getQaBankData, name="display-qa-bank-data"),
    path("ajax_add_gqb_to_benchmark/", quickAddGQB, name="quick-add-gqb"),
    # path("ajax_get_gqb/", getGQB, name="get-gqb"),
    path("ajax_submit_answer_crud/", submitAnswer, name="submit-answer"),
    path("ajax_get_question_data/", getQuestionData, name="get-question"),
    path("ajax_submit_question_update/", submitQuestionEdit, name="edit-question"),
    path("ajax_get_answer_data/", getAnswerData, name="get-answer"),
    path("ajax_get_benchmark_settings/", getBenchmarkSettings, name="get-benchmark-settings"),
    path("ajax_submit_benchmark_crud/", submitCrudBenchmark, name="submit-crud-benchmark"),
    path('benchmarks/', UserBenchmarksView.as_view(), name="user-benchmarks"),




]
