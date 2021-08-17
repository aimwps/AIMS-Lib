from django.contrib import admin
from .models import Pathway, Quiz, QuizQuestion, QuizAnswer, VideoLecture, WrittenLecture, PathwayContentSetting

admin.site.register(Pathway) # Allows posts to be accesible via admin area
admin.site.register(Quiz)
admin.site.register(QuizQuestion)
admin.site.register(QuizAnswer)
admin.site.register(VideoLecture,)
admin.site.register(WrittenLecture)
admin.site.register(PathwayContentSetting)
