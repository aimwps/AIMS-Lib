from django.contrib import admin
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Development.urls')),
    path('', include('Paths.urls')),
    path('', include('Benchmark.urls')),
    path('', include('VideoLecture.urls')),
    path('', include('WrittenLecture.urls')),
    path('', include('QuestionGenerator.urls')),
    path('', include("Community.urls")),
    path('', include("Organisations.urls")),
    path('', include("WebsiteTools.urls")),
    path("favicon.ico", RedirectView.as_view(url=staticfiles_storage.url("favicon.ico"))),
    path('Members/', include("django.contrib.auth.urls")),
    path('Members/', include('Members.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
