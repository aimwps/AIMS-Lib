from django.urls import path
from .views import (
                    ArticleView,
                    ArticleCreate,
                    ArticleEdit,
                    UserArticlesView
)

urlpatterns = [
    path('written_lecture/<int:lit_lec_id>', ArticleView.as_view(), name="article"),
    path('article/create/', ArticleCreate.as_view(), name="create-article"),
    path('article/edit/<int:pk>/', ArticleEdit.as_view(), name="update-article"),
    path('articles/user/', UserArticlesView.as_view(), name="user-articles"),

]
