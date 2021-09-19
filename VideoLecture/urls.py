from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import (
                    VideoLectureView,
                    VideoLectureNew,
                    VideoLectureUserView
)

urlpatterns = [
    path('create_videolecture/', VideoLectureNew.as_view(), name="new-video-lecture"),
    path('video_lecture/<int:vid_lec_id>', VideoLectureView.as_view(), name="video-lecture"),
    path('developer/video_lectures/', VideoLectureUserView.as_view(), name="user-dev-videos"),

]
