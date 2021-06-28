from django.contrib import admin
from .models import Post
# Register your models here.
admin.site.register(Post) # Allows posts to be accesible via admin area
