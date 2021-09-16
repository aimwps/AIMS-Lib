from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import (search_questions,
)

urlpatterns = [
    path("search-generated-questions/", csrf_exempt(search_questions), name="search-gqb"),

]
