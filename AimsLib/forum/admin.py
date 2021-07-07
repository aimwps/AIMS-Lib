from django.contrib import admin
from .models import Post, Reply, Comment, VoteUpDown
# Register your models here.
admin.site.register(Post) # Allows posts to be accesible via admin area
admin.site.register(Reply)
admin.site.register(Comment)
#admin.site.register(VoteUpDown)
