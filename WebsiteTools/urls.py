from django.urls import path
from . import views
from .views import LoginRegisterRequiredView, AccessDeniedView, nav_ajax_check_pathway_invites, nav_ajax_check_organisation_invites
urlpatterns = [
        path('', views.home, name="home"),
        path('login-or-register/', LoginRegisterRequiredView.as_view(), name="login-or-register"),
        path('youshallnotpass/', AccessDeniedView.as_view(), name="access-denied"),
        path('nav_ajax_check_pathway_invites/', nav_ajax_check_pathway_invites, name="get-pathway-invites"),
        path('nav_ajax_check_organisation_invites/', nav_ajax_check_organisation_invites, name="get-pathway-invites")
        #'path('', ForumView.as_view(), name="forum")
]
