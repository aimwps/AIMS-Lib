from django.urls import path
from .views import PathsHomeView
# from .views import

urlpatterns = [
    path('skill_paths/', PathsHomeView.as_view(), name="skill-paths"),
]
