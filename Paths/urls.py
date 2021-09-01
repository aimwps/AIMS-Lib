from django.urls import path
from .views import PathsHomeView, VideoLectureView, WrittenLectureView, QuizView, WrittenLectureNew, VideoLectureNew, PathwayNew, PathwayObjNew, PathwayView, QuestionGeneratorView, BenchmarkCreatorView
# from .views import

urlpatterns = [
    path('pathway/', PathsHomeView.as_view(), name="skill-paths"),
    path('video_lecture/<int:vid_lec_id>', VideoLectureView.as_view(), name="video-lecture"),
    path('written_lecture/<int:lit_lec_id>', WrittenLectureView.as_view(), name="written-lecture"),
    path('knowledge_incrementer/<int:quiz_id>', QuizView.as_view(), name="quiz-app"),
    path('create_videolecture/', VideoLectureNew.as_view(), name="new-video-lecture"),
    path('create_writtenlecture/', WrittenLectureNew.as_view(), name="new-written-lecture"),
    path('create_pathway/', PathwayNew.as_view(), name="new-pathway"),
    path('create_pathway_obj/<int:pathway_id>/', PathwayObjNew.as_view(), name="new-pathway-obj"),
    path('create_benchmark/', BenchmarkCreatorView.as_view(), name="create-benchmark"),
    path('pathway/<int:pathway_id>', PathwayView.as_view(), name="view-pathway"),
    #path('pathway/develop/generate_benchmark/<str:content_type>/<int:obj_id>', GenerateBenchmark.as_view(), name="generate-benchmark"),
    path('pathway/develop/generate_questions/<str:source_type>/<int:source_id>', QuestionGeneratorView.as_view(), name="generate-qas"),

]
