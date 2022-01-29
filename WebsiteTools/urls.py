from django.urls import path
from . import views
from .views import LoginRegisterRequiredView, AccessDeniedView
urlpatterns = [
        path('', views.home, name="home"),
        path('login-or-register/', LoginRegisterRequiredView.as_view(), name="login-or-register"),
        path('youshallnotpass/', AccessDeniedView.as_view(), name="access-denied")
        #'path('', ForumView.as_view(), name="forum")
]
