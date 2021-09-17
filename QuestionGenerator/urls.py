from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import (search_questions, QuestionGenerator, QuestionGeneratorPending, check_gqb_status, VerifyGqbView, get_gqb_to_verify, submit_status_change
)

urlpatterns = [
    path("search-generated-questions/", csrf_exempt(search_questions), name="search-gqb"),
    path('pathway/develop/generate_questions/<str:source_type>/<int:source_id>', QuestionGenerator.as_view(), name="generate-qas"),
    path('pathway/develop/generate_questions_pending/<str:source_type>/<int:source_id>', QuestionGeneratorPending.as_view(), name="generator-pending"),
    path('check-gqb-status/', check_gqb_status, name="check-gqb-status"),
    path('verify-gqb/', VerifyGqbView.as_view(), name="verify-gqb"),
    path('get-gqb-to-verify/', get_gqb_to_verify, name="get-verify-gqb"),
    path("submit-gqb-verification/", submit_status_change, name="submit-gqb-verification"),
]
