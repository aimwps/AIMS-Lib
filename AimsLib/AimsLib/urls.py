from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),
    path('', include('forum.urls')),
    path('', include('Development.urls')),
    path('Members/', include("django.contrib.auth.urls")),
    path('Members/', include('Members.urls')),
]
