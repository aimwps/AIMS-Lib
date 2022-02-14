from django.contrib import admin
from .models import LibraryContentType, Bookmark
# Register your models here.
admin.site.register(LibraryContentType)
admin.site.register(Bookmark)
