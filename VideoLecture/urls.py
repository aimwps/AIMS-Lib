from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import (
                    VideoLectureView,
                    VideoLectureNew,
)

urlpatterns = [
    path('create_videolecture/', VideoLectureNew.as_view(), name="new-video-lecture"),
    path('video_lecture/<int:vid_lec_id>', VideoLectureView.as_view(), name="video-lecture"),

]
