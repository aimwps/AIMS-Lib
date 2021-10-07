from django.urls import path
from .views import CommunityHomeView, TopicCategoryView, TopicView, TopicCreate, TopicCreateInCat, TopicEdit, TopicDelete, ReplyCreate, ReplyEdit

urlpatterns = [
    path('community/', CommunityHomeView.as_view(), name="community-home"),
    path('community/topic/category/<int:cat_id>/', TopicCategoryView, name="topic-category-view"),
    path('community/topic/<int:pk>/', TopicView, name="topic-view"),
    path('community/topic/create/', TopicCreate.as_view(), name="topic-create"),
    path('community/topic/category/create/<int:cat_id>/', TopicCreateInCat.as_view(), name="topic-create-in-cat"),
    path('community/topic/edit/<int:pk>/', TopicEdit.as_view(), name="community-topic-edit"),
    path('community/topic/delete/<int:pk>/', TopicDelete.as_view(), name="topic-delete"),
    path('community/topic/<int:pk>/reply/', ReplyCreate.as_view(), name="reply-create"),
    path('community/reply/<int:pk>/edit/', ReplyEdit.as_view(), name="reply-edit"),

]
