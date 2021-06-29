from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),
    path('forum/', include('forum.urls')),
    path('skilldev/', include('Development.urls')),
]
