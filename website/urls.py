from django.urls import path
from . import views
#from .views import ForumView
urlpatterns = [
        path('', views.home, name="home"),
        #'path('', ForumView.as_view(), name="forum")
]
