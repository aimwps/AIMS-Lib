from django.urls import path
from .views import ForumView, ForumTopicView, ForumTopicNew, ForumTopicEdit, ForumTopicDelete

urlpatterns = [
    #path('', views.home, name="home"),
    path('', ForumView.as_view(), name="forum"),
    path('forum_topic/<int:pk>/', ForumTopicView.as_view(), name="forum-topic-view"), #<int:pk> references the specifc blog
    path('forum_topic/new/', ForumTopicNew.as_view(), name="forum-topic-new"),
    path('forum_topic/edit/<int:pk>', ForumTopicEdit.as_view(), name="forum-topic-edit"),
    path('forum_topic/delete/<int:pk>', ForumTopicDelete.as_view(), name="forum-topic-delete"),
]
