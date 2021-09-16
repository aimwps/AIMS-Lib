from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import (
                    WrittenLectureView,
                    WrittenLectureNew,
                    WrittenLectureEdit,
)

urlpatterns = [
    path('written_lecture/<int:lit_lec_id>', WrittenLectureView.as_view(), name="written-lecture"),
    path('create_writtenlecture/', WrittenLectureNew.as_view(), name="new-written-lecture"),
    path('edit_literature/<int:pk>/', WrittenLectureEdit.as_view(), name="edit-literature"),

]
