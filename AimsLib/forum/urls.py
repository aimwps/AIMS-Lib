from django.urls import path
from .views import ForumViewHome,ForumDevAreaTopics, ForumTopicView, ForumTopicNew, ForumTopicEdit, ForumTopicDelete

urlpatterns = [
    path('forum/', ForumViewHome.as_view(), name="forum-home"),
    path('forum/DevArea/<str:dev_area_name>', ForumDevAreaTopics, name="forum-dev-area"),
    path('forum_topic/<int:pk>/', ForumTopicView.as_view(), name="forum-topic-view"), #<int:pk> references the specifc blog
    path('forum_topic/new/', ForumTopicNew.as_view(), name="forum-topic-new"),
    path('forum_topic/edit/<int:pk>', ForumTopicEdit.as_view(), name="forum-topic-edit"),
    path('forum_topic/delete/<int:pk>', ForumTopicDelete.as_view(), name="forum-topic-delete"),
]
