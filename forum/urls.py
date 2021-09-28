from django.urls import path
from .views import CommunityHomeView, CommunityTopicCategory, TopicView, TopicCreate, TopicCreateInCat, TopicEdit, TopicDelete, ReplyCreate, TopicCreateInCat

urlpatterns = [
    path('community/', CommunityHomeView.as_view(), name="community-home"),
    path('community/category/<int:cat_id>', CommunityTopicCategory, name="community-category"),
    path('topic/view/<int:pk>', TopicView, name="topic-view"),
    path('topic/new/', TopicCreate.as_view(), name="topic-create"),
    path('topic/new/<int:cat_id>/', TopicCreateInCat.as_view(), name="topic-create-in-cat"),
    path('topic/edit/<int:pk>', TopicEdit.as_view(), name="topic-edit"),
    path('topic/delete/<int:pk>', TopicDelete.as_view(), name="topic-delete"),
    path('topic/view/<int:pk>/reply/', TopicReply.as_view(), name="topic-reply"),

]
