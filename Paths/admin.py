from django.contrib import admin
from .models import Pathway, VideoLecture, WrittenLecture, PathwayContentSetting

admin.site.register(Pathway) # Allows posts to be accesible via admin area

admin.site.register(VideoLecture)
admin.site.register(WrittenLecture)
admin.site.register(PathwayContentSetting)
