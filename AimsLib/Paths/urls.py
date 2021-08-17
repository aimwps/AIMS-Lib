from django.urls import path
from .views import PathsHomeView, VideoLectureView, WrittenLectureView, QuizView
# from .views import

urlpatterns = [
    path('skill_paths/', PathsHomeView.as_view(), name="skill-paths"),
    path('video_lecture/<int:vid_lec_id>', VideoLectureView.as_view(), name="video-lecture"),
    path('written_lecture/<int:lit_lec_id>', WrittenLectureView.as_view(), name="written-lecture"),
    path('knowledge_incrementer/<int:quiz_id>', QuizView.as_view(), name="quiz-app"),
]
