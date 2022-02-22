from django.contrib import admin
from .models import LibraryContentType, Bookmark, LibraryPermission
# Register your models here.
admin.site.register(LibraryContentType)
admin.site.register(Bookmark)
admin.site.register(LibraryPermission)
