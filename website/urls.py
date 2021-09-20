from django.urls import path
from . import views
from .views import LoginRegisterRequiredView
urlpatterns = [
        path('', views.home, name="home"),
        path('login-or-register/', LoginRegisterRequiredView.as_view(), name="login-or-register")
        #'path('', ForumView.as_view(), name="forum")
]
