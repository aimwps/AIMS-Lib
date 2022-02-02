from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import (
                    VideoLectureView,
                    VideoLectureNew,
                    VideoLectureUserView,
                    VideoLectureEdit
)

urlpatterns = [
    path('video/create/', VideoLectureNew.as_view(), name="create-video"),
    path('video/<int:vid_lec_id>/', VideoLectureView.as_view(), name="video-lecture"),
    path('videos/user', VideoLectureUserView.as_view(), name="user-videos"),
    path('video/update/<int:pk>/', VideoLectureEdit.as_view(), name="edit-video"),

]
