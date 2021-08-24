from django.urls import path
from .views import MemberRegisterView, MemberEditView, MemberEditPasswordView, MemberProfileView, MemberProfileCreate, MemberProfileEdit
#from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', MemberRegisterView.as_view(), name='member-register'),
    path('member_edit/', MemberEditView.as_view(), name='member-edit'),
    path('password/', MemberEditPasswordView.as_view()),
    path('<int:pk>/profile/', MemberProfileView.as_view(), name='member-profile'),
    path('create_profile/', MemberProfileCreate.as_view(), name='member-profile-create'),
    path('edit_profile/<int:pk>', MemberProfileEdit.as_view(), name='member-profile-edit')
    #path('password/', auth_views.PasswordChangeView.as_view(template_name='registration/change_password.html')),

    #path('login/', MemberRegisterView.as_view(), name='member-login')
]
