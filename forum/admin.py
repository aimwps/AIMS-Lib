from django.contrib import admin
from .models import Topic, Reply, CommentContent, VoteContent
# Register your models here.
admin.site.register(Topic) # Allows posts to be accesible via admin area
admin.site.register(Reply)
admin.site.register(CommentContent)
admin.site.register(VoteContent)
