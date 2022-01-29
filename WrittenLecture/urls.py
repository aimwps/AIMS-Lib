from django.urls import path
from .views import (
                    ArticleView,
                    ArticleCreate,
                    ArticleEdit,
                    UserArticlesView
)

urlpatterns = [
    path('written_lecture/<int:lit_lec_id>', ArticleView.as_view(), name="written-lecture"),
    path('create_writtenlecture/', ArticleCreate.as_view(), name="create-article"),
    path('edit_literature/<int:pk>/', ArticleEdit.as_view(), name="edit-literature"),
    path('developer/written_articles/', UserArticlesView.as_view(), name="user-articles"),

]
