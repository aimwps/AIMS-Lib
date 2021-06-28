from django.urls import path
from .views import ForumView, ForumTopicView

urlpatterns = [
    #path('', views.home, name="home"),
    path('', ForumView.as_view(), name="forum"),
    path('forum_topic/<int:pk>/', ForumTopicView.as_view(), name="forum-topic"), #<int:pk> references the specifc blog

]
