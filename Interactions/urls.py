from django.urls import path
from .views import (
                Vote_ajax_submit,
                Vote_ajax_get

)

urlpatterns = [
    path("Vote_ajax_submit/", Vote_ajax_submit, name="vote-submit"),
    path("Vote_ajax_get_results/", Vote_ajax_get, name="vote-get"),


]
