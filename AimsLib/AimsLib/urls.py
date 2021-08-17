from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),
    path('', include('forum.urls')),
    path('', include('Development.urls')),
    path('', include('Paths.urls')),
    path('Members/', include("django.contrib.auth.urls")),
    path('Members/', include('Members.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
