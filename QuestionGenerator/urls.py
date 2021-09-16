from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import (search_questions, QuestionGeneratorView, QuestionGeneratorPending
)

urlpatterns = [
    path("search-generated-questions/", csrf_exempt(search_questions), name="search-gqb"),
    path('pathway/develop/generate_questions/<str:source_type>/<int:source_id>', QuestionGeneratorView.as_view(), name="generate-qas"),
    path('pathway/develop/generate_questions_pending/<str:source_type>/<int:source_id>', QuestionGeneratorPending.as_view(), name="generator-pending")
]
